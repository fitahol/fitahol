# -*- coding: utf-8 -*-


class NeedParamError(Exception):
    """
    构造参数提供不全异常
    """
    pass


class ParseError(Exception):
    """
    解析微信服务器数据异常
    """
    pass


class NeedParseError(Exception):
    """
    尚未解析微信服务器请求数据异常
    """
    pass


class OfficialAPIError(Exception):
    """
    微信官方API请求出错异常
    """
    pass


class UnOfficialAPIError(Exception):
    """
    微信非官方API请求出错异常
    """
    pass


class NeedLoginError(UnOfficialAPIError):
    """
    微信非官方API请求出错异常 - 需要登录
    """
    pass


class LoginError(UnOfficialAPIError):
    """
    微信非官方API请求出错异常 - 登录出错
    """
    pass


class LoginVerifyCodeError(LoginError):
    """
    微信非官方API请求出错异常 - 登录出错 - 验证码错误
    """
    pass

WXBizMsgCrypt_OK = 0
WXBizMsgCrypt_ValidateSignature_Error = -40001
WXBizMsgCrypt_ParseXml_Error = -40002
WXBizMsgCrypt_ComputeSignature_Error = -40003
WXBizMsgCrypt_IllegalAesKey = -40004
WXBizMsgCrypt_ValidateAppid_Error = -40005
WXBizMsgCrypt_EncryptAES_Error = -40006
WXBizMsgCrypt_DecryptAES_Error = -40007
WXBizMsgCrypt_IllegalBuffer = -40008
WXBizMsgCrypt_EncodeBase64_Error = -40009
WXBizMsgCrypt_DecodeBase64_Error = -40010
WXBizMsgCrypt_GenReturnXml_Error = -40011
