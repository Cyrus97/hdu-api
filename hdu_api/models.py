# -*- coding: utf-8 -*-

"""
hdu_api.models
--------------

This module contains the primary object that power hdu_api.
"""

from __future__ import unicode_literals

import re
import time

from bs4 import BeautifulSoup

from hdu_api.config import CARD_URLS, EXAM_URLS, HOME_URLS, COURSE_URLS, PERSON_URLS, PUBLIC_URLS
from hdu_api.config import DEFAULT_DICTIONARY
from hdu_api.sessions import CardSession, TeachingSession, StudentSession, IHDUPhoneSession, BaseSession, IHDUSession


class BaseModel:
    pass


class CardBaseModel(BaseModel):
    """一卡通系统"""

    def __init__(self, session):
        if isinstance(session, CardSession):
            self.session = session
            # viewstates 储存表单的一个数据，该数据需要提前刷新页面得到
            # 但是可以只获取一次，之后可以再次使用
            self.reuse_form_data = {
                '__VIEWSTATE': {},
            }
        else:
            raise ValueError('session must be CardSession.')


class TeachingBaseModel(BaseModel):
    """教务管理系统"""

    def __init__(self, session):
        if isinstance(session, TeachingSession):
            self.session = session
            self.username = session.username
            self.realname = session.realname
            self.reuse_form_data = {
                '__VIEWSTATE': {},
                '__EVENTVALIDATION': {},

            }
            self.session.headers.update({'referer': HOME_URLS['teaching'].format(username=self.username)})
        else:
            raise ValueError('session must be TeachingSession.')


class StudentBaseModel(BaseModel):
    """学生管理系统"""

    def __init__(self, session):
        if isinstance(session, StudentSession):
            self.session = session
        else:
            raise ValueError('session must be StudentSession.')


class IHDUBaseModel(BaseModel):
    """ihdu"""

    def __init__(self, session):
        if isinstance(session, IHDUSession):
            self.session = session
        else:
            raise ValueError('session must be IHDUSession')


class IHDUPhoneBaseModel(BaseModel):
    """ihdu 手机版"""

    def __init__(self, session):
        if isinstance(session, IHDUPhoneSession):
            self.session = session
        else:
            raise ValueError('session must be IHDUPhoneSession')


class Card(CardBaseModel):
    """一卡通相关信息.

    Card.account - 账户信息
    Card.balance - 余额
    Card.consume
    Card.consume_today
    Card.statistics

    """

    # TODO: 提供原始数据选项
    def account(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """一卡通账户信息"""
        results = None
        rsp = self.session.get(CARD_URLS['account'], allow_redirects=False)
        # TODO: 一个统一的检测
        if rsp.status_code == 200:
            results = []

            try:
                soup = BeautifulSoup(rsp.text, 'lxml')
                result = {}
                rows = soup.find('table', id='Table16').find_all('tr')
                for row in rows:
                    tds = row.find_all('td')
                    for i in range(len(tds) // 2):
                        key = tds[i * 2].get_text(strip=True)
                        if not raw:
                            key = dictionary[key]
                        result.update({
                            key: tds[i * 2 + 1].get_text(strip=True),
                        })
                results.append(result)
            except Exception:
                return None

        return results

    def balance(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询一卡通余额.

        :return:
        """
        results = None
        # 因为在余额查询页面 rsp1 里的余额与实际不符
        # 但是在转账页面 rsp2 里显示的余额是正确的
        rsp1 = self.session.get(CARD_URLS['balance'][0], allow_redirects=False)
        rsp2 = self.session.get(CARD_URLS['balance'][1], allow_redirects=False)
        if rsp1.status_code == 200 and rsp2.status_code == 200:
            results = []

            result = {}
            # 余额页面
            soup = BeautifulSoup(rsp1.text, 'lxml')
            rows = soup.find('div', id='Panel0').find('table', cellspacing=1).find_all('tr')

            for row in rows:
                tds = row.find_all('td')
                for i in range(len(tds) // 2):
                    key = tds[i * 2].get_text(strip=True)
                    if not raw:
                        key = dictionary[key]
                    result.update({
                        key: tds[i * 2 + 1].get_text(strip=True),
                    })

            # 转账页面，获取余额信息
            soup = BeautifulSoup(rsp2.text, 'lxml')
            row = soup.find('table', id='Table13').next_sibling.next_sibling.find_all('tr')[-1]

            tds = row.find_all('td')
            key = '卡余额'
            if not raw:
                key = dictionary[key]
            result.update({
                key: tds[1].get_text(strip=True),
            })

            results.append(result)

        return results

    def consume(self, year, month, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询 :param year: :param month: 的消费记录。

        :param year:
        :param month:
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        payload = self._prepare_payload(CARD_URLS['history'], year, month)

        rsp = self.session.post(CARD_URLS['history'], data=payload, allow_redirects=False)
        if rsp.headers['location'] == '/zytk32portal/Cardholder/QueryhistoryDetail.aspx':
            rsp = self.session.get(CARD_URLS['history_detail'], allow_redirects=False)
            # TODO: 对成功，失败，无信息的分辨
            # 是否可以 None 为失败，[] 为成功但无数据，[...] 成功且有数据
            if rsp.status_code == 200:
                results = self._process_consume_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def consume_today(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询今天的消费记录。



        Usage::

        >>> Card.consume_today()
        [{'流水号': '232205811', '帐号': '30003086', '卡片类型': 'M1', '交易类型': '卡户存款', '商户': '',
        '站点': '校付宝', '终端号': '0', '交易额': '50', '到帐时间': '2019-01-30 19:48', '钱包名称': '1号钱包',
          '卡余额': 'N/A'}]

        :return:
        """
        results = None

        rsp = self.session.get(CARD_URLS['today'], allow_redirects=False)
        if rsp.status_code == 200:
            # TODO: 没有处理无的情况
            results = self._process_consume_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def consume_week(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """
        查询这一周的消费记录。

        :return:
        """
        pass

    def statistics(self, year, month, raw=False, dictionary=DEFAULT_DICTIONARY):
        """
        查询某个月的交易统计。

        :param year:
        :param month:
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        payload = self._prepare_payload(CARD_URLS['statistics'], year, month)

        rsp = self.session.post(CARD_URLS['statistics'], data=payload, allow_redirects=False)
        if rsp.headers['location'] == '/zytk32portal/Cardholder/QueryMonthResult.aspx':
            rsp = self.session.get(CARD_URLS['statistics_result'], allow_redirects=False)
            if rsp.status_code == 200:
                results = []

                soup = BeautifulSoup(rsp.text, 'lxml')
                rows = soup.find('table', id='Table13').next_sibling.next_sibling.find_all('tr')[2].find(
                    'table').find_all('tr')

                keys = []
                row = rows.pop(0)
                tds = row.find_all('td')[1:]
                for td in tds:
                    key = td.get_text(strip=True)
                    if not raw:
                        key = dictionary[key]
                    keys.append(key)

                for row in rows:
                    result = {}
                    tds = row.find_all('td')[1:]
                    for key, td in zip(keys, tds):
                        result.update({key: td.get_text(strip=True)})
                    results.append(result)

        return results

    def _prepare_payload(self, url, year, month):
        """准备表单数据。

        :param url:
        :param year:
        :param month:
        :return:
        """
        if url not in self.reuse_form_data['__VIEWSTATE']:
            rsp = self.session.get(url, allow_redirects=False)
            soup = BeautifulSoup(rsp.text, 'lxml')
            viewstate = soup.find('input', id='__VIEWSTATE')['value']
            self.reuse_form_data['__VIEWSTATE'].update({url: viewstate})
        payload = {
            '__VIEWSTATE': self.reuse_form_data['__VIEWSTATE'][url],
            'ddlYear': year,
            'ddlMonth': month,
            'txtMonth': month,
            'ImageButton1.x': 33,
            'ImageButton1.y': 5,

        }

        return payload

    @staticmethod
    def _process_consume_data(rsp, raw, dictionary):
        results = []

        soup = BeautifulSoup(rsp.text, 'lxml')
        try:
            rows = soup.find('table', id='dgShow').find_all('tr')

            keys = []
            row = rows.pop(0)
            tds = row.find_all('td')
            for td in tds:
                key = td.get_text(strip=True)
                if not raw:
                    key = dictionary[key]
                keys.append(key)

            for row in rows:
                result = {}
                tds = row.find_all('td')
                for key, td in zip(keys, tds):
                    result.update({key: td.get_text(strip=True)})

                results.append(result)
        except:
            if "<script>alert('没有检索到符合的记录！');</script>" in rsp.text:
                return results
            else:
                return None

        return results


class Exam(TeachingBaseModel):
    """考试相关.

    """

    def grade(self, year, term, raw=False, dictionary=DEFAULT_DICTIONARY):
        """
        查询学期成绩。

        :param year:
        :param term:
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        url = EXAM_URLS['grade'].format(username=self.username, realname=self.realname)
        payload = self._prepare_payload(url, year, term)

        rsp = self.session.post(url, data=payload, allow_redirects=False)
        if rsp.status_code == 200:
            results = self._process_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def grade_current(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询本学期的成绩。

        :return:
        """
        year, term = get_current_term()
        return self.grade(year, term, raw=raw, dictionary=dictionary)

    def level_grade(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询等级考试成绩

        :return:
        """
        results = None

        url = EXAM_URLS['level_grade'].format(username=self.username, realname=self.realname)
        rsp = self.session.get(url, allow_redirects=False)

        if rsp.status_code == 200:
            results = self._process_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def schedule(self, year, term, raw=False, dictionary=DEFAULT_DICTIONARY):
        """
        查询考试安排。

        :param year:
        :param term:
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        url = EXAM_URLS['schedule'].format(username=self.username, realname=self.realname)
        payload = self._prepare_payload(url, year, term)

        rsp = self.session.post(url, data=payload, allow_redirects=False)
        if rsp.status_code == 200:
            results = self._process_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def schedule_current(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询本学期考试安排。

        :return:
        """
        year, term = get_current_term()
        return self.schedule(year, term, raw=raw, dictionary=dictionary)

    def schedule_make_up(self, term, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询补考安排"""
        results = None

        url = EXAM_URLS['schedule_make_up'].format(username=self.username, realname=self.realname)
        payload = self._prepare_payload(url, None, term)

        rsp = self.session.post(url, data=payload, allow_redirects=False)
        if rsp.status_code == 200:
            results = self._process_data(rsp, raw=raw, dictionary=dictionary)

        return results

    def _prepare_payload(self, url, year, term):
        if url not in self.reuse_form_data['__VIEWSTATE'] or url not in self.reuse_form_data['__EVENTVALIDATION']:
            rsp = self.session.get(url, allow_redirects=False)
            if rsp.status_code == 200:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    viewstate = soup.find('input', id='__VIEWSTATE')['value']
                    eventvalidation = soup.find('input', id='__EVENTVALIDATION')['value']
                    self.reuse_form_data['__VIEWSTATE'].update({url: viewstate})
                    self.reuse_form_data['__EVENTVALIDATION'].update({url: eventvalidation})
                except:
                    pass

        # 表单数据混合了两个，但无影响
        paylaod = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.reuse_form_data['__VIEWSTATE'][url],
            '__EVENTVALIDATION': self.reuse_form_data['__EVENTVALIDATION'][url],
            'xnd': year,
            'xqd': term,
            'ddlxn': year,
            'ddlxq': term,
            'btnCx': ' 查  询 ',
        }

        return paylaod

    @staticmethod
    def _process_data(rsp, raw, dictionary):
        results = []

        soup = BeautifulSoup(rsp.text, 'xml')

        try:
            rows = soup.find('table', id='DataGrid1').find_all('tr')

            keys = []
            row = rows.pop(0)
            tds = row.find_all('td')
            for td in tds:
                key = td.get_text(strip=True)
                if not raw:
                    key = dictionary[key]
                keys.append(key)

            for row in rows:
                result = {}
                tds = row.find_all('td')
                for key, td in zip(keys, tds):
                    result.update({key: td.get_text(strip=True)})

                results.append(result)
        except:
            if 'Object moved to' in rsp.text:
                return None

        return results


class Course(TeachingBaseModel):
    """

    """

    def selected(self, year, term, raw=False, dictionary=DEFAULT_DICTIONARY):
        results = None

        url = COURSE_URLS['selected'].format(username=self.username, realname=self.realname)
        payload = self._prepare_payload(url, year, term)
        rsp = self.session.post(url, data=payload, allow_redirects=False)

        if rsp.status_code == 200:
            results = self._process_data(rsp, raw=raw, dictionary=dictionary)

        return results

    @staticmethod
    def _process_data(rsp, raw, dictionary):
        results = []

        soup = BeautifulSoup(rsp.text, 'lxml')
        try:
            rows = soup.find('table', id='DBGrid').find_all('tr')

            keys = []
            row = rows.pop(0)
            tds = row.find_all('td')[:-4]  # 这里把后面 4 项省去了
            for td in tds:
                key = td.get_text(strip=True)
                if not raw:
                    key = dictionary[key]
                keys.append(key)
            for row in rows:
                result = {}
                tds = row.find_all('td')[:-4]
                for key, td in zip(keys, tds):
                    result.update({key: td.get('title') if td.get('title') else td.get_text(strip=True)})

                results.append(result)
        except:
            if 'Object moved to' in rsp.text:
                return None

        return results

    def selected_current(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        year, term = get_current_term()
        return self.selected(year, term, raw, dictionary)

    def schedule(self, year, term, raw=False, dictionary=DEFAULT_DICTIONARY):
        """
        查询某学期的课表。

        :param year:
        :param term:
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        # url = COURSE_URLS['schedule'].format(username=self.username, realname=self.realname)
        # payload = self._prepare_payload(url, year, term)
        #
        # rsp = self.session.post(url, data=payload, allow_redirects=False)
        # if rsp.status_code == 200:
        #     results = self._process_course_data(rsp)

        selected = self.selected(year, term, raw=True, dictionary=dictionary)
        if selected:
            results = self._process_course_data(selected, raw=raw, dictionary=dictionary)

        return results

    @staticmethod
    def _process_course_data(selected, raw, dictionary):
        """
        处理课表数据。

        :param selected:
        :param raw:
        :param dictionary:
        :return:
        """

        results = []

        for s in selected:
            name = s.get('课程名称')
            teacher = s.get('教师姓名')
            classroom = s.get('上课地点').split(';')
            classtime = s.get('上课时间').split(';')
            weekday = None
            start_section = None
            end_section = None
            start_week = None
            end_week = None
            distribute = '每周'

            for i in range(len(classtime)):
                m1 = re.match(r'^(周.{1})第(\d*).*?(\d*)节{第(\d*)-(\d*)周\|?([单双]周)?}$', classtime[i])
                m2 = re.match(r'^第(\d*)周/(周.{1})/(.*)第(\d*)周/(周.{1})/(.*)$', classtime[i])
                if m1:
                    time_t = m1.groups()
                    weekday = time_t[0]
                    start_section = time_t[1]
                    end_section = time_t[2]
                    start_week = time_t[3]
                    end_week = time_t[4]
                    distribute = time_t[5] if time_t[5] else '每周'
                elif m2:
                    time_t = m2.groups()
                    start_week = time_t[0]
                    start_section = time_t[2]
                    end_week = time_t[3]
                    end_section = time_t[5]
                    weekday = time_t[1] + ' - ' + time_t[4]

                if raw:
                    course = {
                        '课程名称': name,
                        '教师姓名': teacher,
                        '上课地点': classroom[i],
                        '星期': weekday,
                        '开始节数': start_section,
                        '结束节数': end_section,
                        '开始周': start_week,
                        '结束周': end_week,
                        '课程分布': distribute,
                    }
                else:
                    course = {
                        dictionary.get('课程名称', '课程名称'): name,
                        dictionary.get('教师姓名', '教师姓名'): teacher,
                        dictionary.get('上课地点', '上课地点'): classroom[i],
                        dictionary.get('星期', '星期'): weekday,
                        dictionary.get('开始节数', '开始节数'): start_section,
                        dictionary.get('结束节数', '结束节数'): end_section,
                        dictionary.get('开始周', '开始周'): start_week,
                        dictionary.get('结束周', '结束周'): end_week,
                        dictionary.get('课程分布', '课程分布'): distribute,
                    }

                results.append(course)

        return results

    def schedule_current(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        year, term = get_current_term()
        return self.schedule(year, term, raw=raw, dictionary=dictionary)

    def _prepare_payload(self, url, year, term):
        if url not in self.reuse_form_data['__VIEWSTATE'] or url not in self.reuse_form_data['__EVENTVALIDATION']:
            rsp = self.session.get(url, allow_redirects=False)
            if rsp.status_code == 200:
                soup = BeautifulSoup(rsp.text, 'lxml')
                try:
                    viewstate = soup.find('input', id='__VIEWSTATE')['value']
                    eventvalidation = soup.find('input', id='__EVENTVALIDATION')['value']
                    self.reuse_form_data['__VIEWSTATE'].update({url: viewstate})
                    self.reuse_form_data['__EVENTVALIDATION'].update({url: eventvalidation})
                except:
                    pass

        # 表单数据混合了两个，但无影响
        paylaod = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.reuse_form_data['__VIEWSTATE'][url],
            '__EVENTVALIDATION': self.reuse_form_data['__EVENTVALIDATION'][url],
            'xnd': year,
            'xqd': term,
            # 'ddlxn': year,
            # 'ddlxq': term,  # 和 ddlXQ 冲突
            'ddlXN': year,
            'ddlXQ': term,
            'btnCx': ' 查  询 ',
        }

        return paylaod


class Person(StudentBaseModel):
    """
    个人信息。
    """

    def _get_common_page(self):
        rsp = self.session.get(PERSON_URLS['common'], allow_redirects=False)
        if rsp.status_code == 200:
            soup = BeautifulSoup(rsp.text, 'lxml')
            rows = soup.find('div', class_='cg-form-elements').find_all('tr')
            return rows

    @staticmethod
    def _process_data_from_rows(rows, raw, dictionary):
        result = None
        if rows:
            result = {}
            for row in rows:
                tds = row.find_all('td')
                for i in range(len(tds) // 2):
                    key = tds[2 * i].get_text(strip=True).replace('：', '').replace(' ', '')
                    if key == '':
                        continue
                    if not raw:
                        key = dictionary[key]
                    result.update({key: tds[2 * i + 1].get_text(strip=True)})

        return result

    @staticmethod
    def _process_award_data_form_rows(rows, raw, dictionary):
        result = None
        if rows:
            result = {}

            keys = []
            row = rows.pop(0)
            tds = row.find_all('td')[1:]
            # 生成数据模板 {'2018-2019': {各奖项}, '2017-2018':{}, ...}
            for td in tds:
                key = td.get_text(strip=True)
                if not raw:
                    key = dictionary[key]
                keys.append(key)
                result.update({key: dict()})

            for row in rows[:-5]:
                tds = row.find_all('td')
                key = tds.pop(0).get_text(strip=True)
                for i in range(len(tds)):
                    result[keys[i]].update({key: tds[i].get_text(strip=True)})

            tds = rows[-3].find_all('td')  # 学期标题
            term_keys = []
            for i in range(len(tds) // 2):  # 学期标题，两组一学年
                for j in range(2):
                    key = tds[2 * i + j].get_text(strip=True)
                    if not raw:
                        key = dictionary[key]
                    term_keys.append(key)
                    result[keys[i]].update({key: dict()})

            for row in rows[-2:]:
                tds = row.find_all('td')
                key = tds.pop(0).get_text(strip=True)
                for i in range(len(tds) // 2):
                    result[keys[i]][term_keys[2 * i]].update({key: tds[2 * i].get_text(strip=True)})
                    result[keys[i]][term_keys[2 * i + 1]].update({key: tds[2 * i + 1].get_text(strip=True)})

        return result

    def profile(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询基本个人信息。

        :return:
        """
        rows = self._get_common_page()
        return self._process_data_from_rows(rows[1:9], raw=raw, dictionary=dictionary)

    def instructor(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """辅导员信息。"""
        rows = self._get_common_page()
        return self._process_data_from_rows(rows[10:12], raw=raw, dictionary=dictionary)

    def status(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询学籍信息。"""
        rows = self._get_common_page()
        return self._process_data_from_rows(rows[13:17], raw=raw, dictionary=dictionary)

    def accommodation(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """住宿信息。

        :return:
        """
        rows = self._get_common_page()
        return self._process_data_from_rows(rows[18:20], raw=raw, dictionary=dictionary)

    def award(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询奖项。"""
        rows = self._get_common_page()
        return self._process_award_data_form_rows(rows[-18:-4], raw=raw, dictionary=dictionary)

    def profile_all(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询详细的个人信息。

        :return:
        """
        rows = self._get_common_page()
        return {
            # 基本信息
            rows[0].get_text(strip=True): self._process_data_from_rows(rows[1:9], raw=raw, dictionary=dictionary),
            # 辅导员信息
            rows[9].get_text(strip=True): self._process_data_from_rows(rows[10:12], raw=raw, dictionary=dictionary),
            # 学籍信息
            rows[12].get_text(strip=True): self._process_data_from_rows(rows[13:17], raw=raw, dictionary=dictionary),
            # 宿舍信息
            rows[17].get_text(strip=True): self._process_data_from_rows(rows[18:20], raw=raw, dictionary=dictionary),
            # 获奖信息
            rows[-20].get_text(strip=True): self._process_award_data_form_rows(rows[-18:-4], raw=raw,
                                                                               dictionary=dictionary),
        }


class Public(IHDUPhoneBaseModel):
    """

    """

    def classroom_free(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询空闲教室。

        :return:
        """

        results = None

        rsp = self.session.get(PUBLIC_URLS['class_free'], allow_redirects=False)
        if rsp.status_code == 200:
            results = self._process_classroom_data(rsp, raw=raw, dictionary=dictionary)
        return results

    def classroom_in_use(self, raw=False, dictionary=DEFAULT_DICTIONARY):
        """查询有课的教室。

        :return:
        """
        results = None

        rsp = self.session.get(PUBLIC_URLS['class_in_use'], allow_redirects=False)
        if rsp.status_code == 200:
            results = self._process_classroom_data(rsp, raw=raw, dictionary=dictionary)
        return results

    @staticmethod
    def schooltime(location=0, raw=False, dictionary=DEFAULT_DICTIONARY):
        """

        :param location: 0 means 下沙, 1 means 青山湖
        :param raw:
        :param dictionary:
        :return:
        """
        results = None

        rsp = BaseSession().get(PUBLIC_URLS['school_time'], allow_redirects=False)
        if rsp.status_code == 200:
            results = []

            div_id = 'xiashaTime'
            if int(location) == 1:
                div_id = 'xingongTime'
            soup = BeautifulSoup(rsp.text, 'lxml')
            rows = soup.find('div', id=div_id).find_all('tr')

            for row in rows:
                result = {}
                tds = row.find_all('td')
                key1 = '节数'
                key2 = '开始时间'
                key3 = '结束时间'
                if not raw:
                    key1 = dictionary[key1]
                    key2 = dictionary[key2]
                    key3 = dictionary[key3]
                times = tds[-1].get_text(strip=True).split('～')
                times.append('')  # 有些只有一个
                result.update({
                    key1: tds[-2].get_text(strip=True),
                    key2: times[0].strip(),
                    key3: times[1].strip(),
                })
                results.append(result)

        return results

    @staticmethod
    def _process_classroom_data(rsp, raw, dictionary):
        results = []
        soup = BeautifulSoup(rsp.text, 'lxml')

        try:
            tables = soup.find_all('table')[1:]
            if tables:
                for table in tables:
                    result = {}

                    key1 = '教研楼'
                    key2 = '教室'
                    if not raw:
                        key1 = dictionary[key1]
                        key2 = dictionary[key2]
                    location = table.find('tr').get_text(strip=True)
                    classroom = []

                    ths = table.find_all('th', class_='xl1')
                    for th in ths:
                        classroom.append(th.get_text(strip=True))

                    result.update({
                        key1: location,
                        key2: classroom,
                    })

                    results.append(result)
        except:
            return None

        return results


def get_current_term():
    localtime = time.localtime(time.time())

    if localtime.tm_mon in range(3, 9):  # 下学期 3, 4, 5, 6, 7, 8
        year = '{}-{}'.format(localtime.tm_year - 1, localtime.tm_year)
        term = 2
    else:  # 上学期 9, 10, 11, 12, 1, 2
        term = 1
        if localtime.tm_mon in range(9, 13):  # 上学期 9, 10, 11, 12, 年份向前看
            year = '{}-{}'.format(localtime.tm_year, localtime.tm_year + 1)
        else:
            year = '{}-{}'.format(localtime.tm_year - 1, localtime.tm_year)

    return year, term
