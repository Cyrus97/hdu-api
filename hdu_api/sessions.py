# -*- coding: utf-8 -*-

"""
hdu_api.sessions
----------------


This module implement the management of session for hdu_api.
"""

from __future__ import unicode_literals

import re
from threading import Thread

from bs4 import BeautifulSoup
from requests import Session

from hdu_api._internal_utils import encrypt
from hdu_api.config import CAS_LOGIN_HEADERS, TEACHING_HEADERS, STUDENT_HEADERS, CARD_HEADERS, IHDU_HEADERS, \
    IHDU_PHONE_HEADERS
from hdu_api.config import HOME_URLS, CAS_LOGIN_URLS, CARD_ERROR_URL
from hdu_api.exceptions import LoginFailException

# 登录重试次数
RETRY = 3

CARD_SESSION_NAME = 'card'
TEACHING_SEESION_NAME = 'teaching'
STUDENT_SESSION_NAME = 'student'
IHDU_SESSION_NAME = 'ihdu'
IHDU_PHONE_SESSION_NAME = 'ihdu_phone'


class BaseSession(Session):
    """基本 session, 继承自 requests.Session"""


class BaseSessionLoginMixin(BaseSession):
    """混合登录功能"""

    def __init__(self, username, password):
        super(BaseSessionLoginMixin, self).__init__()
        self.username = username
        self.password = password
        self.realname = None
        self.home_url = None

    def login(self, headers):
        retry = 0
        while retry < RETRY:
            retry += 1
            self._do_login()

            # headers['referer'] = self.home_url
            self.headers.update(headers)  # 更新 headers

            if self._check_sess_vaild():
                return True
            else:
                self.cookies.clear()  # 直接清除 cookie 有点问题
                self.headers.clear()

                if retry == RETRY:
                    raise LoginFailException('登录失败.')

        return False

    def _do_login(self):
        raise NotImplementedError

    def _get_payload(self, url):
        rsp = self.get(url)
        if rsp.status_code != 200:
            return None
        soup = BeautifulSoup(rsp.text, 'lxml').find('script', id='password_template')
        soup = BeautifulSoup(soup.contents[0], 'lxml')
        lt = soup.find('input', id='lt')['value']
        execution = soup.find('input', attrs={'name': 'execution'})['value']
        _eventId = soup.find('input', attrs={'name': '_eventId'})['value']
        rsa = encrypt(self.username + self.password + lt, '1', '2', '3')
        payload = {
            'rsa': rsa,
            'ul': len(self.username),
            'pl': len(self.password),
            'lt': lt,
            'execution': execution,
            '_eventId': _eventId,
        }

        return payload

    def _check_sess_vaild(self):
        raise NotImplementedError

    @staticmethod
    def is_valid_url(self, url):
        reg = r'^http[s]*://.+$'
        return re.match(reg, url)

    def refresh(self):
        """
        刷新 seesion

        :rtype: bool
        """
        rsp = self.get(self.home_url, allow_redirects=False)
        if rsp.status_code == 200:
            return True

        return False


class TeachingSessionLoginMixin(BaseSessionLoginMixin):
    """
    混合教务管理系统(http://jxgl.hdu.edu.cn)的登录功能.
    """

    def __init__(self, username, password):
        super(TeachingSessionLoginMixin, self).__init__(username, password)
        self.home_url = HOME_URLS['teaching'].format(username=username)

    def login(self, headers=TEACHING_HEADERS):
        return super(TeachingSessionLoginMixin, self).login(headers)

    def _do_login(self):
        """登录数字杭电，然后转跳到教务系统。"""
        payload = self._get_payload(CAS_LOGIN_URLS['teaching'])

        # 通过智慧杭电认证

        rsp = self.post(CAS_LOGIN_URLS['teaching'], data=payload, headers=CAS_LOGIN_HEADERS, allow_redirects=False)

        # 选课系统转跳
        next_url = rsp.headers['Location']
        rsp = self.get(next_url, allow_redirects=False)

    def _check_sess_vaild(self):
        cookies_keys = list(self.cookies.get_dict().keys())
        if 'ASP.NET_SessionId' in cookies_keys and 'route' in cookies_keys:
            rsp = self.get(self.home_url, allow_redirects=False)
            if 'Object moved' not in rsp.text:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    self.realname = soup.find('form').find('div', class_='info').find('span',
                                                                                      id='xhxm').get_text().replace(
                        '同学', '')
                except:
                    return False
                return True

        return False


class CardSessionLoginMixin(BaseSessionLoginMixin):
    """
    混合一卡通系统(http://ykt.hdu.edu.cn/zytk32portal/Cardholder/Cardholder.aspx)的登录功能.
    """

    def __init__(self, username, password):
        super(CardSessionLoginMixin, self).__init__(username, password)
        self.home_url = HOME_URLS['card']

    def login(self, headers=CARD_HEADERS):
        return super(CardSessionLoginMixin, self).login(headers)

    def _do_login(self):
        payload = self._get_payload(CAS_LOGIN_URLS['card'])

        try:
            rsp = self.post(CAS_LOGIN_URLS['card'], data=payload, headers=CAS_LOGIN_HEADERS,
                            allow_redirects=False)
            next_url = rsp.headers['Location']
            rsp = self.get(next_url, allow_redirects=False)
            next_url = rsp.headers['Location']
            rsp = self.get(next_url, allow_redirects=False)
            next_url = rsp.headers['Location']
            rsp = self.get(next_url, allow_redirects=False)

            # next_url = rsp.headers['Location']
            # next_url = "http://ykt.hdu.edu.cn" + next_url
            # self.home_url = next_url
            # rsp = self.session.get(self.home_url, allow_redirects=False)
            # print(rsp.headers['Location'])
        except:
            return

    def _check_sess_vaild(self):
        cookies_keys = list(self.cookies.get_dict().keys())
        if 'ASP.NET_SessionId' in cookies_keys:
            rsp = self.get(self.home_url, allow_redirects=False)
            if rsp.status_code == 302 and rsp.headers['location'] in CARD_ERROR_URL and 'Object moved' in rsp.text:
                return False
            else:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    self.realname = soup.find('span', id='lblInName').get_text()
                    return True
                except:
                    return False

        return False


class StudentSessionLoginMixin(BaseSessionLoginMixin):
    """
    混合学生管理系统(http://xgxt.hdu.edu.cn/login)的登录功能.
    """

    def __init__(self, username, password):
        super(StudentSessionLoginMixin, self).__init__(username, password)
        self.home_url = HOME_URLS['student']

    def login(self, headers=STUDENT_HEADERS):
        return super(StudentSessionLoginMixin, self).login(headers)

    def _do_login(self):
        payload = self._get_payload(CAS_LOGIN_URLS['student'])

        try:
            rsp = self.post(CAS_LOGIN_URLS['student'], data=payload, headers=CAS_LOGIN_HEADERS,
                            allow_redirects=False)
            next_url = rsp.headers['location']
            rsp = self.get(next_url, allow_redirects=False)
            next_url = rsp.headers['location']

            self.home_url = next_url
        except:
            pass

    def _check_sess_vaild(self):
        cookies_keys = list(self.cookies.get_dict().keys())
        if 'route' in cookies_keys and 'JSESSIONID' in cookies_keys:
            rsp = self.get(self.home_url, allow_redirects=False)
            if 'Object moved' in rsp.text:
                return False
            else:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    self.realname = soup.find('span', id='login-username').get_text().strip().split()[0]
                    return True
                except:
                    return False

        return False


class IHDUSessionLoginMixin(BaseSessionLoginMixin):
    """
    混合 ihdu(https://i.hdu.edu.cn/tp_up/view?m=up) 的登录功能.
    """

    def __init__(self, username, password):
        super(IHDUSessionLoginMixin, self).__init__(username, password)
        self.home_url = HOME_URLS['ihdu']

    def login(self, headers=IHDU_HEADERS):
        return super(IHDUSessionLoginMixin, self).login(headers)

    def _do_login(self):
        payload = self._get_payload(CAS_LOGIN_URLS['ihdu'])

        try:
            rsp = self.post(CAS_LOGIN_URLS['ihdu'], data=payload, headers=CAS_LOGIN_HEADERS,
                            allow_redirects=False)
            next_url = rsp.headers['location']
            rsp = self.get(next_url, allow_redirects=False)
        except:
            pass

    def _check_sess_vaild(self):
        cookies_keys = list(self.cookies.get_dict().keys())
        if 'tp_up' in cookies_keys:
            rsp = self.get(self.home_url, allow_redirects=False)
            if rsp.status_code != 200 or 'Object moved' in rsp.text:
                return False
            else:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    self.realname = soup.find('div', id='user-con').find('span', class_='tit').get_text().strip()
                    return True
                except:
                    return False

        return False


class IHDUPhoneSessionLoginMixin(BaseSessionLoginMixin):
    """
    混合 ihdu手机版(http://once.hdu.edu.cn/dcp/xphone/m.jsp)的登录功能.
    """

    def __init__(self, username, password):
        super(IHDUPhoneSessionLoginMixin, self).__init__(username, password)
        self.home_url = HOME_URLS['ihdu_phone']

    def login(self, headers=IHDU_PHONE_HEADERS):
        return super(IHDUPhoneSessionLoginMixin, self).login(headers)

    def _do_login(self):
        payload = self._get_payload(CAS_LOGIN_URLS['ihdu_phone'])

        try:
            rsp = self.post(CAS_LOGIN_URLS['ihdu_phone'], data=payload, headers=CAS_LOGIN_HEADERS,
                            allow_redirects=False)
            next_url = rsp.headers['location']
            rsp = self.get(next_url, allow_redirects=False)
        except:
            pass

    def _check_sess_vaild(self):
        cookies_keys = list(self.cookies.get_dict().keys())
        if 'route' in cookies_keys and 'key_dcp_v5' in cookies_keys:
            rsp = self.get(self.home_url, allow_redirects=False)
            if rsp.status_code != 200 or 'Object moved' in rsp.text:
                return False
            else:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    uls = soup.find('div', class_='webkitbox').find_all('ul')
                    if len(uls) == 3:
                        return True
                except:
                    return False

        return False


class TeachingSession(TeachingSessionLoginMixin):
    """教务管理系统(http://jxgl.hdu.edu.cn)的 session"""


class CardSession(CardSessionLoginMixin):
    """一卡通系统(http://ykt.hdu.edu.cn/zytk32portal/Cardholder/Cardholder.aspx)的 session"""


class StudentSession(StudentSessionLoginMixin):
    """学生管理系统(http://xgxt.hdu.edu.cn/login)的 session"""


class IHDUSession(IHDUSessionLoginMixin):
    """ihdu(https://i.hdu.edu.cn/tp_up/view?m=up)的 session"""


class IHDUPhoneSession(IHDUPhoneSessionLoginMixin):
    """ihdu 手机版(http://once.hdu.edu.cn/dcp/xphone/m.jsp) 的 session"""


class SessionManager(object):
    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password
        self.sessions = dict()

    def create(self, multi=True):
        """
        create and return a new and usable session dict.
        """

        card_sess = CardSession(self.username, self.password)
        teaching_sess = TeachingSession(self.username, self.password)
        student_sess = StudentSession(self.username, self.password)
        ihdu_phone_sess = IHDUPhoneSession(self.username, self.password)
        ihdu_sess = IHDUSession(self.username, self.password)

        if multi:
            threads = [
                Thread(target=card_sess.login),
                Thread(target=teaching_sess.login),
                Thread(target=student_sess.login),
                Thread(target=ihdu_phone_sess.login),
                Thread(target=ihdu_sess.login),
            ]

            for t in threads:
                t.start()

            for t in threads:
                t.join()

        else:
            card_sess.login()
            teaching_sess.login()
            student_sess.login()
            ihdu_phone_sess.login()
            ihdu_sess.login()

        self.sessions.update({
            CARD_SESSION_NAME: card_sess,
            TEACHING_SEESION_NAME: teaching_sess,
            STUDENT_SESSION_NAME: student_sess,
            IHDU_SESSION_NAME: ihdu_sess,
            IHDU_PHONE_SESSION_NAME: ihdu_phone_sess,
        })

        return self.sessions

    def get_teaching_session(self):
        return self.sessions.get(TEACHING_SEESION_NAME)

    def get_card_session(self):
        return self.sessions.get(CARD_SESSION_NAME)

    def get_student_session(self):
        return self.sessions.get(STUDENT_SESSION_NAME)

    def get_ihdu_session(self):
        return self.sessions.get(IHDU_SESSION_NAME)

    def get_ihdu_phone_session(self):
        return self.sessions.get(IHDU_PHONE_SESSION_NAME)
