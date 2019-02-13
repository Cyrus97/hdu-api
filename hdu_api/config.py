# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# urls
CAS_LOGIN_URLS = {
    'teaching': "http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/index.aspx",
    'card': "http://cas.hdu.edu.cn/cas/login?service=http://once.hdu.edu.cn/dcp/dcp/sso/ssoYkt.jsp",
    'student': "http://cas.hdu.edu.cn/cas/login?service=http://xgxt.hdu.edu.cn:80/neusoftcas.jsp",
    'ihdu_phone': "http://cas.hdu.edu.cn/cas/login?service=http://once.hdu.edu.cn/dcp/xphone/m.jsp",
    'ihdu': "http://cas.hdu.edu.cn/cas/login?service=https://i.hdu.edu.cn/tp_up/view?m=up",
}

HOME_URLS = {
    'teaching': "http://jxgl.hdu.edu.cn/xs_main.aspx?xh={username}",
    'card': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/Cardholder.aspx",
    'student': "http://xgxt.hdu.edu.cn/login",
    'ihdu': "https://i.hdu.edu.cn/tp_up/view?m=up",
    'ihdu_phone': "http://once.hdu.edu.cn/dcp/xphone/m.jsp",
}

CARD_URLS = {
    'account': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/AccInfo.aspx",
    'balance': (
        "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/AccBalance.aspx",
        "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/Transfer.aspx",
    ),
    'today': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/QueryCurrDetailFrame.aspx",
    'history': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/Queryhistory.aspx",
    'history_detail': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/QueryhistoryDetailFrame.aspx",
    'statistics': "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/QueryMonthCollect.aspx",
    "statistics_result": "http://ykt.hdu.edu.cn/zytk32portal/Cardholder/QueryMonthResult.aspx",
}

CARD_ERROR_URL = (
    '/zytk32portal/error.aspx?t=1',
)

EXAM_URLS = {
    'grade': "http://jxgl.hdu.edu.cn/xscjcx_dq.aspx?xh={username}&xm={realname}&gnmkdm=N121605",
    'level_grade': "http://jxgl.hdu.edu.cn/xsdjkscx.aspx?xh={username}&xm={realname}&gnmkdm=N121606",
    'schedule': "http://jxgl.hdu.edu.cn/xskscx.aspx?xh={username}&xm={realname}&gnmkdm=N121604",
    'schedule_make_up': "http://jxgl.hdu.edu.cn/xsbkkscx.aspx?xh={username}&xm={realname}&gnmkdm=N121618",
}

PERSON_URLS = {
    'common': "http://xgxt.hdu.edu.cn/xuesheng/look",
}

COURSE_URLS = {
    'schedule': "http://jxgl.hdu.edu.cn/xskbcx.aspx?xh={username}&xm={realname}&gnmkdm=N121603",
    'selected': "http://jxgl.hdu.edu.cn/xsxkqk.aspx?xh={username}&xm={realname}&gnmkdm=N121621",

}

PUBLIC_URLS = {
    'class_free': "http://once.hdu.edu.cn/dcp/xphone/jscx.jsp?f=1",  # 空闲教室
    'class_in_use': "http://once.hdu.edu.cn/dcp/xphone/jscx.jsp?f=0",  # 有课教室
    'school_time': "https://i.hdu.edu.cn/tp_up/resource/hdu/schoolTime.html",
}

TEACHING_ERROR_URL = (
    "/zdy.htm?aspxerrorpath=/xs_main.aspx",
    "http://jxgl.hdu.edu.cn/zdy.htm?aspxerrorpath=/xs_main.aspx",
)

IHDU_URLS = {

}

IHDU_PHONE_URLS = {
    'course': "http://once.hdu.edu.cn/dcp/xphone/kbcx0.jsp",  # 课表
    'grade': "http://once.hdu.edu.cn/dcp/xphone/cjcx.jsp",  # 成绩
    'exam': "http://once.hdu.edu.cn/dcp/xphone/ksap.jsp",  # 考试安排
    'class_free': "http://once.hdu.edu.cn/dcp/xphone/jscx.jsp?f=1",  # 空闲教室
    "class_not_free": "http://once.hdu.edu.cn/dcp/xphone/jscx.jsp?f=0",  # 有课教室
    'card': "http://once.hdu.edu.cn/dcp/xphone/yktxx.jsp",  # 一卡通
    'level_grade': "http://once.hdu.edu.cn/dcp/xphone/djkscjcx.jsp",  # 等级考试成绩
}

# headers
CAS_LOGIN_HEADERS = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cache-control': "max-age=0",
    'connection': "keep-alive",
    'content-type': "application/x-www-form-urlencoded",
    'host': "cas.hdu.edu.cn",
    'origin': "http://cas.hdu.edu.cn",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

TEACHING_HEADERS = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'connection': "keep-alive",
    'host': "jxgl.hdu.edu.cn",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'DNT': '1',
}

CARD_HEADERS = {
    'Host': "ykt.hdu.edu.cn",
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'DNT': "1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
}

STUDENT_HEADERS = {
    'Host': "xgxt.hdu.edu.cn",
    'Connection': "keep-alive",
    # 'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'DNT': "1",
    'Referer': "http://xgxt.hdu.edu.cn/login",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
}

IHDU_HEADERS = {
    'Host': "i.hdu.edu.cn",
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'DNT': "1",
    'Referer': "https://i.hdu.edu.cn/tp_up/view?m=up",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
}

IHDU_PHONE_HEADERS = {
    'Host': "once.hdu.edu.cn",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'DNT': "1",
    'Referer': "http://once.hdu.edu.cn/dcp/xphone/m.jsp",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
}

# 默认使用的数据替换词典
DEFAULT_DICTIONARY = {
    # Card
    '个人编号': 'staff_id',
    '卡号': 'card_id',
    '卡片类型': 'card_type',
    '姓名': 'staff_name',
    '帐号': 'account_id',
    '性别': 'gender',
    '有效期': 'expiry_date',
    '状态': 'status',
    '证件号码': 'id_card',
    '证件类型': 'id_type',
    '身份': 'identity',
    '部门': 'department',

    '卡余额': 'balance',

    '交易类型': 'deal_type',
    '交易额': 'mondeal',
    '到帐时间': 'deal_time',
    '商户': 'shop',
    '流水号': 'order_num',
    '站点': 'location',
    '终端号': 'terminal_id',
    '钱包名称': 'wallet',

    '交易次数': 'deal_frequency',
    '交易金额': 'deal_amount',

    # Exam
    '学年': 'school_year',
    '学期': 'semester',
    '课程代码': 'course_code',
    '课程名称': 'course_name',
    '课程性质': 'course_type',
    '课程归属': 'course_attribution',
    '学分': 'credit',
    '平时成绩': 'usual_score',
    '期中成绩': 'mid_score',
    '期末成绩': 'final_score',
    '实验成绩': 'experimental_score',
    '成绩': 'score',
    '补考成绩': 'retest_mark',
    '是否重修': 'retake_or_not',
    '开课学院': 'college',
    '备注': 'comments',
    '补考备注': 'comments_of_makeup',

    '选课课号': 'select_code',
    '考试时间': 'exam_time',
    '考试地点': 'classroom',
    '考试形式': 'exam_type',
    '座位号': 'seat',

    '等级考试名称': 'level_exam_name',
    '准考证号': 'ticket_number',
    '考试日期': 'exam_time',
    '听力成绩': 'listening_score',
    '阅读成绩': 'reading_score',
    '写作成绩': 'writing_score',
    '综合成绩': 'comprehensive_score',

    # Course
    '是否选课': 'is_selected',
    '教师姓名': 'teacher',
    '周学时': 'weekly_hour',
    '上课时间': 'class_time',
    '上课地点': 'classroom',
    '教材': 'material',
    '重修标记': 'retake_mark',

    '星期': 'weekday',
    '开始节数': 'start_section',
    '结束节数': 'end_section',
    '开始周': 'start_week',
    '结束周': 'end_week',
    '课程分布': 'distribute',

    # Person
    '产权': 'property',
    '公寓楼': 'apartment ',
    '寝室号': 'dormitory ',
    '床号': 'bed',

    'qq': 'qq',
    'Email': 'email',
    '兴趣': 'hobby',
    '出生日期': 'birthday',
    '学号': 'staff_id',
    '宗教信仰': 'religion',
    '户籍所在地': 'domicile',
    '政治面貌': 'political',
    '毕业中学': 'graduation_school',
    '民族': 'nationality',
    '生源地': 'student_source',
    '联系手机': 'phone',
    '身份证号': 'id_card',

    '办公地点': 'office_location',
    '联系电话': 'phone',

    '专业': 'major',
    '入学时间': 'admission_time',
    '在校状况': 'school_situation',
    '学制': 'duration',
    '学生类别': 'student_type',
    '学籍状态': 'student_status',
    '学院': 'college',
    '年级': 'grade',
    '班级': 'class',

    '节数': 'lesson',
    '开始时间': 'start_time',
    '结束时间': 'end_time',

    '教研楼': 'building',
    '教室': 'classroom'
}
