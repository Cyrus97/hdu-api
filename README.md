<p align="center">
  <a href="https://github.com/Cyrus97/hdu-api"><img src="https://i.loli.net/2019/04/03/5ca4c6ffc61fa.png" alt="HDU-API"></a>
</p>
<p align="center">
A simple SDK for HDU.
</p>
<p align="center">
  <a href="https://pypi.org/project/hdu-api/"><img src="https://img.shields.io/pypi/v/hdu-api.svg?style=flat"></a>
  <a href="https://github.com/Cyrus97/hdu-api"><img src="https://img.shields.io/pypi/pyversions/hdu-api.svg?style=flat"></a>
  <a href="https://github.com/Cyrus97/hdu-api/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/hdu-api.svg?style=flat"></a>
  <a href="https://pepy.tech/project/hdu-api"><img src="https://pepy.tech/badge/hdu-api"></a> 
  <a href="https://996.icu"><img src="https://img.shields.io/badge/link-996.icu-red.svg" alt="996.icu"></a>
</p>

---

hdu-api 是一个集结 HDU 所有教务管理服务的 SDK，提供了一卡通服务、考试、课表、选课和一些公共信息如空闲教室、上课时间等信息的 API。 hdu-api 主要基于 Requests 库和 Beautiful Soup 库写成。

## 特性

* 支持一卡通服务的信息查询
* 支持教务管理系统的考试、课程等信息查询
* 支持学生管理系统的信息查询
* 支持 ihdu PC 版和手机版的信息查询
* 易用，友好的 API
* 基于 requests 库，支持每个网站的 session 使用和管理，重用性高
* 自定义，对返回数据进行自定义化

## 安装

使用包管理器安装，如 pip:

```text
pip install hdu-api
```

## 快速开始

```text
>>> import hdu_api
>>> hdu = hdu_api.HDU('学号', '密码')
>>> client = hdu.create()
>>> client.exam.schedule_current()
[{'classroom': '第12教研楼201',
  'course_name': '操作系统（甲）',
  'exam_time': '2019年1月17日(09:00-11:00)',
  'exam_type': '',
  'seat': '10',
  'select_code': '(2018-2019-1)-A0507050-06018-1',
  'staff_name': 'xxx'},

 ...

 {'classroom': '第6教研楼北308',
  'course_name': '软件工程（甲）',
  'exam_time': '2019年1月9日(13:45-15:45)',
  'exam_type': '',
  'seat': '24',
  'select_code': '(2018-2019-1)-A0507190-06061-2',
  'staff_name': 'xxx'}]

>>> client.card.balance()
[{'account_id': 'xxxxxx',
  'balance': '69.97',
  'card_id': 'xxxxxx',
  'staff_id': 'xxxxxx',
  'staff_name': 'xxx'}]
```

## 文档

https://liuxingran.gitbook.io/hdu-api/
