# 快速上手

这一文档部分介绍了如何快速上手 `hdu-api`。现已假设你已安装 `hdu-api`，如果还没有安装，请去[安装](install.md)一节进行安装。

现在让我们从一些简单的示例开始吧！

## 创建 client

要想使用 `hdu-api` 访问到一卡通、课表等信息，必须先创建一个 `client`。

首先我们先导入使用的模块：

```text
>>> from hdu_api import HDU
```

之后传入正确的 `学号` 和 `密码` 创建一个 `HDU` 对象:

```text
>>> hdu = HDU('学号', '密码')
```

最后使用该对象创建一个 client：

```text
>>> client = hdu.create()
```

我们最后得到了一个名为 `client` 的 `HduClient` 对象，通过该对象可以获取到任意的信息。

## 访问信息

通过上面，我们已经创建了一个名为 `client` 的 `HduClient` 对象，现在我们看看如何访问我们想要的信息。

### 获取一卡通相关的信息

通过 `HduClient.card` 可以获取到使用一卡通的信息。

一卡通账户：

```text
>>> from hdu_api import HDU
>>> hdu = HDU('学号', '密码')
>>> client = hdu.create()
>>> client.card.account()
[{'account_id': '30***86',
  'card_id': '13***42',
  'card_type': 'M1',
  'department': '1***7',
  'expiry_date': '2020年8月29日',
  'gender': '*',
  'id_card': '',
  'id_type': '',
  'identity': '***',
  'staff_id': '1***7',
  'staff_name': '***',
  'status': '有效卡'}]
```

一卡通余额：

```text
>>> client.card.balance()
[{'account_id': '3***6',
  'balance': '76.07',
  'card_id': '1***2',
  'staff_id': '1***7',
  'staff_name': '***'}]
```

更多一卡通信息 API 使用可以查看[这里](apis/card.md)。

### 获取考试相关的信息

通过 `HduClient.exam` 可以获取到使用考试相关的信息。

考试成绩：

```text
>>> client.exam.grade_current()
[{'college': '外国语学院',
  'comments': '',
  'comments_of_makeup': '',
  'course_attribution': '通识必修',
  'course_code': 'A1103780',
  'course_name': '实用翻译',
  'course_type': '外语模块',
  'credit': '2.0',
  'experimental_score': '',
  'final_score': '76.5',
  'mid_score': '',
  'retake_or_not': '',
  'retest_mark': '',
  'school_year': '2018-2019',
  'score': '82',
  'semester': '1',
  'usual_score': '91'},

 ...

 {'college': '计算机学院',
  'comments': '',
  'comments_of_makeup': '',
  'course_attribution': '',
  'course_code': 'B0507370',
  'course_name': '数据挖掘',
  'course_type': '专业限选',
  'credit': '3.0',
  'experimental_score': '',
  'final_score': '85',
  'mid_score': '',
  'retake_or_not': '',
  'retest_mark': '',
  'school_year': '2018-2019',
  'score': '84',
  'semester': '1',
  'usual_score': '83'}]
```

考试安排：

```text
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
```

更多考试相关信息 API 使用可以查看[这里](apis/exam.md)。

{% hint style="info" %}
当然，`hdu-api` 提供的 API 访问服务不仅仅只有这些，想查看所有的 API 使用吗？请访问[这里](apis/)。
{% endhint %}

