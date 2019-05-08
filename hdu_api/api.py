# -*- coding: utf-8 -*-

"""
hdu_api.api
-----------

This module implements the hdu_api API.
"""

from hdu_api.models import Card, Exam, Person, Course, Public
from hdu_api.sessions import SessionManager, IHDUSession


class HDU(object):
    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password

    def __str__(self):
        return "<HDU [username={}]>".format(self.username)

    def create(self, multi=True, *args):
        """Create a client to use API."""
        sess_mgr = SessionManager(self.username, self.password)
        sess_mgr.create(multi)
        return HduClient(sess_mgr)

    @staticmethod
    def verify(username, password) -> bool:
        return IHDUSession(username, password).login()


class HduClient(object):
    """
    Use a HduClient to access all APIs.
    """

    def __init__(self, sess_mgr, **kwargs):
        if isinstance(sess_mgr, SessionManager):
            self.sess_mgr = sess_mgr
            self.username = sess_mgr.username
            self.card = Card(sess_mgr.get_card_session())
            self.exam = Exam(sess_mgr.get_teaching_session())
            self.person = Person(sess_mgr.get_student_session())
            self.course = Course(sess_mgr.get_teaching_session())
            self.public = Public(sess_mgr.get_ihdu_phone_session())

        else:
            raise ValueError('sess_mgr must be SessionManager.')

    def __str__(self):
        return "<Client [username={}]".format(self.username)
