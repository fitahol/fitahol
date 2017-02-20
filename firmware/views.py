# coding=utf-8
import random

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.views.generic import TemplateView, CreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from account.processing import get_username
from firmware.models import Feedback, ClientVersion
from firmware.serializers import FeedbackSerializer
from utils.handle_msg import send_email_msg, valid_code_content, \
    send_register_sms, send_auth_valid_sms
from utils.tools import seconds_until_midnight


class HomeView(TemplateView):
    template_name = "home.html"


class FeedbackView(CreateView):
    model = Feedback
    fields = ['nickname', "contact", "content"]
    success_url = '/'


class FeedbackViewSet(ListCreateAPIView):
    model = Feedback
    serializer_class = FeedbackSerializer


class ValidCodeView(APIView):
    def get(self, request, *args, **kwargs):
        account = self.request.query_params["account"]
        v_type = self.request.query_params.get("v_type", "register")
        valid_limit = cache.get("valid_limit") or 0
        if valid_limit > 10:
            return Response({"detail": "达到每日发送上限"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        User = get_user_model()
        valid_code = random.randint(1000, 9999)
        u_type, username = get_username(account)
        try:
            user_obj = User.objects.get(username=username)
            if u_type == "register":
                return Response({"detail": "帐户已存在, 请直接登陆"},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            if u_type == "reset_pwd":
                return Response({"detail": "用户帐户不存在"},
                                status=status.HTTP_404_NOT_FOUND)
        cache_key = "code_%s_%s" % (v_type, account)
        cache.set(cache_key, valid_code, 240)
        if u_type == "phone":
            # 手机号查找
            msg = "请求成功,请注意接收短信"
            msg_func_cfg = {"reset_phone": send_auth_valid_sms,
                            "reset_pwd": send_auth_valid_sms,
                            "register": send_register_sms}
            msg_func_cfg.get(v_type)(valid_code, account)
        else:
            # 邮箱查找
            msg = "请求成功,请注意查收邮件"
            subject_cfg = {"register": "Fitahol-注册验证码",
                           "reset_pwd": "Fitahol-重置密码验证",
                           "reset_phone": "Fitahol-重置手机验证"}
            subject = subject_cfg.get(v_type, "Fitahol-验证码确认")
            content = valid_code_content.format(valid_code=valid_code)
            send_email_msg(subject, content, account)
        cache.set("valid_limit", valid_limit+1, seconds_until_midnight())
        return Response({"detail": msg})


class ClientVersionView(APIView):
    def get(self, request, *args, **kwargs):
        platform_str = self.kwargs.get("platform")
        version = self.request.query_params.get("version")
        platform = 1 if platform_str == "ios" else 0
        version_queryset = ClientVersion.objects.filter(
            platform=platform, start_version__lte=version,
            end_version__gte=version)
        result = {}
        if version_queryset:
            version_obj = version_queryset[0]
            url = version_obj.ios_url if platform == 1 else version_obj.android_url
            result = {"id": version_obj.id, "desc": version_obj.desc,
                      "version": version.version, "url": url,
                      "is_force": version_obj.is_force}
        return Response(result)
