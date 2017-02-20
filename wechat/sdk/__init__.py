# -*- coding: utf-8 -*-

__all__ = ['WechatBasic', 'WechatExt']

try:
    from wechat.sdk.basic import WechatBasic
    from wechat.sdk.ext import WechatExt
except ImportError:
    pass
