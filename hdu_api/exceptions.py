# -*- coding: utf-8 -*-

"""
hdu_api.exceptions
------------------


"""


class AccountErrorException(Exception):
    """账户错误异常."""


class LoginFailException(Exception):
    """登录失败异常."""


class SessionInvalidationException(Exception):
    """session 失效异常."""
