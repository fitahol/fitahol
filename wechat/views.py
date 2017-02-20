# coding=utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import WechatInfo, Profile, Coach, Member, CoachMemberRef
from account.serializers import CoachSerializer
from account.tasks import init_new_user
from .sdk.basic import WechatBasic


class WechatLoginView(APIView):
    permission_classes = ()

    def get_openid(self, code, u_type=1):
        if u_type == 1:
            wechat = WechatBasic(token=settings.WECHAT_TOKEN,
                                 appid=settings.WECHAT_APP_ID,
                                 appsecret=settings.WECHAT_APP_SECRET)
        else:
            wechat = WechatBasic(token=settings.WECHAT_TOKEN,
                                 appid=settings.WECHAT_MEMBER_APP_ID,
                                 appsecret=settings.WECHAT_MEMBER_APP_SECRET)
        resp = wechat.get_session_key(code)
        if resp.get("errcode"):
            return None
        return resp["openid"]
    
    def create_fit_info(self, u_type, user_obj):
        # 创建用户信息
        if u_type == 1:
            _, new_coach = Coach.objects.get_or_create(user=user_obj, )
        elif u_type == 0:
            _, new_member = Member.objects.get_or_create(user=user_obj)
        else:
            pass
    
    def add_coach_info(self, user_obj, result):
        ref_queryset = CoachMemberRef.objects.filter(
            primary=True, member__user=user_obj)
        if ref_queryset:
            serializer = CoachSerializer(ref_queryset[0].coach)
            result.update({"coach": serializer.data})
            
    def update_gym_info(self, user_obj, result):
        serializer = CoachSerializer(user_obj.coach)
        data = serializer.data
        del data["id"]
        result.update(data)
    
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        code = request_data["code"]
        u_type = int(self.request.data.get("u_type", 1))
        openid = self.get_openid(code, u_type)
        try:
            wechat_bind = WechatInfo.objects.get(openid=openid)
            token, _ = Token.objects.get_or_create(user=wechat_bind.user)
            result = {"token": token.key,
                      "user_id": wechat_bind.user_id,
                      "u_type": wechat_bind.user.profile.u_type}
            self.create_fit_info(u_type, wechat_bind.user)
            if u_type == 0:
                self.add_coach_info(wechat_bind.user, result)
            else:
                self.update_gym_info(wechat_bind.user, result)
            return Response(result)
        except WechatInfo.DoesNotExist:
            nickname = request_data["nickName"]
            headimgurl = request_data["avatarUrl"]
            gender = request_data["gender"]
            province = request_data["province"]
            city = request_data["city"]
            country = request_data["country"]
            
            User = get_user_model()
            user_obj, _ = User.objects.get_or_create(username=openid,
                                                     password=make_password(
                                                         "atm7777777"))
            wechat_bind = WechatInfo(user=user_obj, nickname=nickname,
                                     headimgurl=headimgurl,
                                     openid=openid,
                                     sex=gender, province=province, city=city,
                                     country=country)
            wechat_bind.save()
            self.create_fit_info(u_type, wechat_bind.user)
            profile_obj = Profile(user=user_obj, u_type=u_type,
                                  nickname=nickname)
            profile_obj.save()
            token, _ = Token.objects.get_or_create(user=wechat_bind.user)
            init_new_user.delay(user_id=user_obj.id)
            result = {"token": token.key,
                      "user_id": wechat_bind.user_id,
                      "u_type": wechat_bind.user.profile.u_type}
            if u_type == 0:
                self.add_coach_info(wechat_bind.user, result)
            else:
                self.update_gym_info(wechat_bind.user, result)
            return Response(result)
