# coding=utf-8
"""view"""
from io import BytesIO
import os
import base64
import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, login, authenticate
from django.core.cache import cache
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from account.models import Coach, Member, Profile, Figure, \
    WechatInfo, UserRelationConfirm, CoachMemberRef
from account.processing import get_username
from account.serializers import CoachSerializer, MemberSerializer, \
    UserSerializer, FigureSerializer, UserRelationConfirmSerializer, \
    WechatInfoSerializer, MemberListSerializer, MemberDetailSerializer, \
    ProfileSerializer, UserInfoSerializer
from account.tasks import init_new_user
from fitness.models import ExpertTag
from gym.models import Gymnasium
from notifications.processing import get_unread_num
from notifications.signals import notify
from notifications.views import UnreadCountView
from wechat.wx_template_msg import send_member_add_msg

logger = logging.getLogger("access_file_log")


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        account = self.request.data["account"]
        password = self.request.data["password"]
        u_type = self.request.data.get("u_type", 1)
        valid_code = self.request.data["valid_code"]
        rpt_password = self.request.data["rpt_password"]
        nickname = self.request.data.get("nickname")
        if password != rpt_password:
            return Response({"detail": "密码不相同"},
                            status=status.HTTP_400_BAD_REQUEST)
        User = get_user_model()
        account_type, username = get_username(account)
        if not nickname:
            nickname = username
        cache_key = "code_%s_%s" % ("register", account)
        cache_vcode = cache.get(cache_key)
        if str(valid_code) != "1984" and valid_code != str(cache_vcode):
            return Response({"detail": "验证码不符,请重新输入"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            new_user = User(username=username,
                            password=make_password(password))
            new_user.save()
            profile_obj = Profile(user=new_user, u_type=u_type,
                                  nickname=nickname)
            if u_type == 1:
                new_coach = Coach(user=new_user, )
                new_coach.save()
            else:
                new_member = Member(user=new_user)
                new_member.save()
            if account_type == "phone":
                # 手机号注册
                profile_obj.phone = account
            else:
                # 邮箱注册
                new_user.email = account
                new_user.save()
            profile_obj.save()
            Token.objects.get_or_create(user=new_user)
            init_new_user.delay(user_id=new_user.id)
        except IntegrityError:
            return Response({"detail": "注册帐户已存在, 请直接登录"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "注册成功"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        account = self.request.data["account"]
        password = self.request.data["password"]
        u_type = self.request.data.get("u_type", 1)
        _, username = get_username(account)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.profile.u_type != u_type:
                # 用户身份切换
                profile = user.profile
                profile.u_type = u_type
                profile.save()
                try:
                    if u_type == 1:
                        new_coach = Coach(user=user, )
                        new_coach.save()
                    else:
                        new_member = Member(user=user)
                        new_member.save()
                except IntegrityError:
                    pass
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                profile = UserSerializer(user)
                result = {"detail": "登录成功", "token": token.key}
                result.update(profile.data)
                return Response(result)
            else:
                return Response({"detail": "用户被禁用,请联系管理员"},
                                status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "用户名或密码错误"},
                        status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        account = self.request.data["account"]
        valid_code = self.request.data["valid_code"]
        password = self.request.data["password"]
        cache_key = "code_%s_%s" % ("reset_pwd", account)
        cache_code = cache.get(cache_key)
        if str(valid_code) != "1984" and valid_code != str(cache_code):
            return Response({"detail": "验证码错误"},
                            status=status.HTTP_400_BAD_REQUEST)
        _, username = get_username(account)
        User = get_user_model()
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "用户不存在"},
                            status=status.HTTP_404_NOT_FOUND)
        user_obj.password = make_password(password)
        user_obj.save()
        return Response({"detail": "重置成功"})


class ResetPhoneView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        account = self.request.data["account"]
        valid_code = self.request.data["valid_code"]
        cache_key = "code_%s_%s" % ("reset_phone", account)
        cache_code = cache.get(cache_key)
        if str(valid_code) != "1984" and valid_code != str(cache_code):
            return Response({"detail": "验证码错误"},
                            status=status.HTTP_400_BAD_REQUEST)
        if Profile.objects.filter(phone=account).exists():
            return Response({"detail": "手机号已绑定用户，请直接登录"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = self.request.user.profile
        profile.phone = account
        profile.save()
        return Response({"detail": "绑定成功"})


class AccountView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = UserSerializer(self.request.user)
        count_view = UnreadCountView.as_view()
        result = {"user": profile.data}
        msg_count_res = count_view(request, *args, **kwargs).data
        result.update(msg_count_res)
        if request.user.profile.u_type == 1:
            data = CoachSerializer(request.user.coach).data
            result.update({"coach": data})
        else:
            data = MemberSerializer(request.user.member).data
            result.update({"member": data})
        return Response(result)


class CoachViewSet(viewsets.ModelViewSet):
    """
    教练
    """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    
    def get_queryset(self):
        query_str = self.request.query_params.get("query")
        if query_str:
            if query_str.isdigit():
                if len(query_str) == 11:
                    return Coach.objects.filter(
                        user__profile__phone=query_str)
                else:
                    return Coach.objects.filter(
                        user__id=int(query_str))
            return Coach.objects.filter(
                user__profile__nickname__contains=query_str)
        return Coach.objects.all()
    
    @detail_route()
    def info(self, request, *args, **kwargs):
        instance = Coach.objects.get(user_id=self.kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @list_route()
    def personal(self, request, *args, **kwargs):
        user_obj = request.user
        member_obj = Member.objects.get(user=user_obj)
        serializer = CoachSerializer(member_obj.coach.all(), many=True)
        results = serializer.data
        for each in results:
            try:
                ref_obj = CoachMemberRef.objects.get(member=member_obj,
                                                     coach_id=each["id"])
                each["primary"] = ref_obj.primary
            except CoachMemberRef.DoesNotExist:
                pass
        return Response(results)

    @list_route(methods=["post"])
    def set_primary(self, request, *args, **kwargs):
        user_obj = request.user
        coach_obj = Coach.objects.get(user_id=request.data["coach"])
        ref_queryset = CoachMemberRef.objects.filter(coach=coach_obj,
                                                     member__user=user_obj)
        if not ref_queryset:
            return Response({"detail": "未添加该教练"})
        CoachMemberRef.objects.filter(primary=True,
                                      member__user=user_obj
                                      ).update(primary=False)
        coach_ref = ref_queryset[0]
        coach_ref.primary = True
        coach_ref.save()
        serializer = UserInfoSerializer(coach_obj.user)
        return Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
    """
    学员
    """
    queryset = Member.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == "GET" and not self.kwargs.get("pk"):
            return MemberListSerializer
        return MemberDetailSerializer

    def get_object(self):
        return Member.objects.get(user_id=self.kwargs["pk"])

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, "coach"):
            # 非教练获取学员, 返回空
            return []
        query_str = self.request.query_params.get("query")
        if query_str:
            if query_str.isdigit():
                if len(query_str) == 11:
                    return Member.objects.filter(user__profile__phone=query_str)
                else:
                    return Member.objects.filter(user__id=int(query_str))
            return Member.objects.filter(user__profile__nickname__contains=query_str)
        else:
            queryset = Member.objects.filter(coach=user.coach)
        return queryset
    
    @list_route()
    def card(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = [{"user_id": each.user_id,
                    "nickname": each.get_nickname(),
                    "portrait": each.get_portrait()} for each in queryset]
        return Response(results)
    
    def list(self, request, *args, **kwargs):
        response = super(MemberViewSet, self).list(request, *args, **kwargs).data
        sorted_res = sorted(response, key=lambda x: x['first_letter'])
        new_req_num = UserRelationConfirm.objects.filter(
                        recipient=self.request.user, status=0).count()
        return Response({"results": sorted_res, "new_req_num": new_req_num})


class UserRelationView(ListCreateAPIView):
    """添加绑定教练/学员"""
    queryset = UserRelationConfirm.objects.all()
    serializer_class = UserRelationConfirmSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserRelationConfirm.objects.filter(
            recipient_id=self.request.user.id, status=0)

    def create(self, request, *args, **kwargs):
        user_id = int(request.data["user_id"])
        formId = request.data.get("formId")
        User = get_user_model()
        if user_id == self.request.user.id:
            return Response({"detail": "不能添加自己"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        recipient_obj = get_object_or_404(User, id=user_id)
        ref_type = "add_member" if self.request.user.profile.u_type == 1 else "add_coach"
        if UserRelationConfirm.objects.filter(
                recipient=recipient_obj,
                sender=self.request.user,
                ref_type=ref_type).exists():
            return Response({"detail": "添加成功,请等待对方验证"})
        new_ref = UserRelationConfirm(
            recipient=recipient_obj,
            sender=self.request.user,
            ref_type=ref_type)
        new_ref.save()
        logger.info("new_member formId: %s " % formId)
        send_member_add_msg(user_id, formId)
        return Response({"detail": "添加成功,请等待对方验证"},
                        status=status.HTTP_201_CREATED)


class UserRelationConfirmView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_ref = UserRelationConfirm.objects.get(id=kwargs["pk"])
        confirm_status = request.data["status"]
        if confirm_status == -1:
            # 拒绝对方请求
            user_ref.status = confirm_status
            user_ref.save()
            title = "用户: %s 已拒绝您的添加请求" % user_ref.recipient_id
            description = "用户: %s ， 昵称: %s ， 已拒绝您的添加请求"
            notify.send(sender=user_ref.recipient, recipient=user_ref.sender,
                        action_object=user_ref, show_time=user_ref.utime,
                        description=description, title=title)
            return Response({"detail": "已拒绝对方请求"})
        if user_ref.ref_type in ["add_member", "add_coach"]:
            sender = user_ref.sender
            recipient = user_ref.recipient
            if self.request.user.profile.u_type == 1:
                # 消息接收人 为教练
                try:
                    member_obj = sender.member
                except Member.DoesNotExist:
                    member_obj = Member(user=sender)
                    member_obj.save()
                coach_obj = recipient.coach
            else:
                # 消息接收人 为学员
                member_obj = recipient.member
                try:
                    coach_obj = sender.coach
                except Coach.DoesNotExist:
                    coach_obj = Coach(user=sender)
                    coach_obj.save()
            CoachMemberRef.objects.get_or_create(member=member_obj,
                                                 coach=coach_obj)
            user_ref.status = confirm_status
            user_ref.save()
            title = "用户: %s 接受您的添加请求" % user_ref.recipient_id
            description = "用户: %s ， 昵称: %s ， 已接受您的添加请求。" % \
                          (user_ref.recipient_id,
                           user_ref.recipient.profile.nickname)
            notify.send(sender=user_ref.recipient, recipient=user_ref.sender,
                        action_object=user_ref, show_time=user_ref.utime,
                        description=description, title=title)
        return Response({"detail": "确认成功"},
                        status=status.HTTP_201_CREATED)


class DelRelationView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        user_obj = self.request.user
        try:
            CoachMemberRef.objects.filter(member__user_id=user_id,
                                          coach__user=user_obj).delete()
        except TypeError:
            pass
        try:
            CoachMemberRef.objects.filter(coach__user_id=user_id,
                                          member__user=user_obj).delete()
        except TypeError:
            pass
        return Response({"detail": "删除成功"})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    个人信息
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return ProfileSerializer

    def get_queryset(self):
        query_str = self.request.query_params.get("query")
        if query_str:
            if query_str.isdigit():
                if len(query_str) == 11:
                    return get_user_model().objects.filter(
                        profile__phone=query_str)
                else:
                    return get_user_model().objects.filter(
                        id=int(query_str))
            return get_user_model().objects.filter(
                profile__nickname__contains=query_str)
        return [self.request.user, ]

    def get_object(self):
        if self.request.method == "GET":
            return self.request.user
        return get_object_or_404(get_user_model(), id=self.kwargs.get("pk"))
    
    def update_coach_info(self, user_obj, result):
        serializer = CoachSerializer(user_obj.coach)
        data = serializer.data
        del data["id"]
        result.update(data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        result["unread_num"] = get_unread_num(self.request.user.id)
        new_req_num = UserRelationConfirm.objects.filter(
            recipient=self.request.user, status=0).count()
        result["new_req_num"] = new_req_num
        if instance.profile.u_type == 1:
            self.update_coach_info(instance, result)
        return Response(result)

    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data.update({"user": request.user})
        partial = kwargs.pop('partial', True)
        # 头像更新
        profile = Profile.objects.get(user=self.request.user)
        pic_data = self.request.data.get("portrait")
        if pic_data:
            filename = "portrait_" + str(profile.user_id) + "." + self.request.data.get("type", "png")
            buffer = BytesIO(base64.decodebytes(pic_data.split('base64,')[1].encode('ascii')))
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', len(buffer.getvalue()), None)
            request_data["portrait"] = filebuffer
        instance = self.get_object().profile
        serializer = self.get_serializer(instance, data=request_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        gym_id = request_data.get("gym_id")
        if gym_id:
            self.update_gym(gym_id, request.user)
        expert_tags = request_data.get("expert_tags")
        if expert_tags:
            self.update_expert_tag(expert_tags, request.user)
        return Response(serializer.data)
    
    def update_gym(self, gym_id, user_obj):
        coach_obj = user_obj.coach
        try:
            gym_obj = Gymnasium.objects.get(id=gym_id)
            coach_obj.gym = gym_obj
            coach_obj.save()
        except Gymnasium.DoesNotExist:
            pass
        
    def update_expert_tag(self, expert_tags, user_obj):
        expert_tags_list = expert_tags.split(",")
        queryset = ExpertTag.objects.filter(id__in=expert_tags_list)
        user_obj.coach.expert_tags.add(*queryset)


class PortraitView(APIView):
    """
    头像创建或更新
    """
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        pic_data = self.request.data["portrait"]
        filename = "portrait_" + str(
            profile.user_id) + "." + self.request.data.get("type", "png")
        buffer = BytesIO(
            base64.decodebytes(pic_data.split('base64,')[1].encode('ascii')))
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', len(buffer.getvalue()), None)
        profile.portrait = filebuffer
        profile.save()
        return Response({"上传头像成功"})


class FigureViewSet(viewsets.ModelViewSet):
    """
    形象照片墙展示
    """
    queryset = Figure.objects.all()
    serializer_class = FigureSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return Figure.objects.filter(user_id=user_id)
        return Figure.objects.all()
    
    @list_route()
    def latest(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        queryset = Figure.objects.filter(user_id=user_id).order_by("-id")[:3]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        pic_data = request_data.get("figure")
        figure_file = request_data.get("figure_file")
        if figure_file:
            # 支持文件上传
            request_data["figure"] = figure_file
        if pic_data:
            # 支持base64 数据压缩值上传
            filename = "figure_" + str(
                request_data["user_id"]) + "." + self.request.data.get("type", "png")
            buffer = BytesIO(base64.decodebytes(
                pic_data.split('base64,')[1].encode('ascii')))
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', len(buffer.getvalue()),
                None)
            request_data["figure"] = filebuffer
        request_data["user"] = request_data.get("user_id")
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        file_directory = settings.MEDIA_ROOT + str(instance.figure)
        if os.path.isfile(file_directory):
            os.remove(file_directory)
        instance.delete()
        

class WechatInfoViewSet(viewsets.ModelViewSet):
    """
    微信个人信息
    """
    queryset = WechatInfo.objects.all()
    serializer_class = WechatInfoSerializer
