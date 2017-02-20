
日程&课程
=====

已购买课程
-----
.. http:get:: /schedule/course/purchased/

    获取已购课程数&剩余课程

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/course/purchased/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "id": 1,
        "user_id": 12,
        "amount": 30,
        "remain": 13
        }

添加/修改购买课程
---------
.. http:post:: /schedule/course/

    添加购买课程

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param remain: 课程余量
    :type remain: int

    **请求示例**

    .. sourcecode:: http

        POST /schedule/course/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "添加成功"
        }

更新购买课程数
-------
.. http:put:: /schedule/course/<course_id>/

    更新购买课程

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param amount: 总量
    :type amount: int
    :param remain: 余量
    :type remain: int

    **请求示例**

    .. sourcecode:: http

        PUT /schedule/course/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 201 OK
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "更新成功"
        }


日历类型
----
.. http:get:: /schedule/calendar/

    获取日历类型, 目前只有一种 私教 default，可不获取。

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/calendar/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "name": "私教课程",
            "slug": "default"
            },
            {
            "id": 2,
            "name": "个人练习",
            "slug": "private"
            }
        ]


课程事件
----
.. http:get:: /schedule/event/

    获取健身目标, 包括系统

    **请求参数**:

    需要 Token 认证通过

    date 过滤传参
    :param day: 具体日期,如 2016-01-31
    :type day: string

    date_range 过滤传参
    :param begin: 开始日期,如 2016-01-31
    :type begin: string
    :param end: 结束日期,如 2016-02-31
    :type end: string

    month 过滤传参
    :param year: 具体年份,如 2016
    :type year: int
    :param month: 具体月份,如 2, 12
    :type month: int

    year 过滤传参
    :param day: 具体年份,如 2016
    :type day: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/event/?user_id=6&interval=date&day=2016-01-31 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "calendar_slug": "default",
            "user":{
                "id": 6,
                "nickname": "学员介绍23",
                "portrait": "学员头像"
                },
            "start": "2016-01-31 07:00:00",
            "end": "2016-01-31 08:00:00",
            "description": "添加数据描述",
            "end_recurring_period": null, // 过滤时间, 与rule配合使用
            "color_event": "#000000",
            "coach": 5,
            "rule": null
            }
        ]

最近课程事件
------
.. http:get:: /schedule/event/last/

    获取最近课程事件

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/event/last/?user_id=6&interval=date&day=2016-01-31 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "id": 1,
        "calendar_slug": "default",
        "user":{
            "id": 6,
            "nickname": "学员介绍23",
            "portrait": "学员头像"
            },
        "start": "2016-01-31 07:00:00",
        "end": "2016-01-31 08:00:00",
        "description": "添加数据描述",
        "end_recurring_period": null, // 过滤时间, 与rule配合使用
        "color_event": "#000000",
        "coach": 5,
        "rule": null
        }

过滤用户课程事件
--------
.. http:get:: /schedule/event/?user_id=<user_id>

    获取某用户自己的课程事件

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/event/?user_id=9 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "calendar_slug": "default",
            "user":{
                "id": 6,
                "nickname": "学员介绍23",
                "portrait": "学员头像"
                },
            "start": "2016-01-31 07:00:00",
            "end": "2016-01-31 08:00:00",
            "description": "添加数据描述",
            "end_recurring_period": null, // 过滤时间, 与rule配合使用
            "color_event": "#000000",
            "coach": 5,
            "rule": null
            }
        ]


添加课程事件
------
.. http:post:: /schedule/event/

    添加课程事件：**重复事件必须选择次数或终止时间其中一项，两项都选则叠加规则**

    **请求参数**:

    需要 Token 认证通过

    :param start: 开始时间
    :type start: string
    :param end: 结束时间
    :type end: string
    :param calendar_slug: 选择日历，默认为default，可不传; 如果设置休息，值为 rest
    :type calendar_slug: string
    :param coach: 教练ID
    :type coach: int
    :param user_id: 参与人员ID, 一般指学员; 设置休息值传为0或空即可
    :type user_id: int
    :param color_event: 日程颜色, 16进程颜色, 如 #000000
    :type color_event: string
    :param description: 事件备注或描述
    :type description: int
    :param rule_id: 如果需要重复，需要选择规则ID；**重复事件必须选择次数或终止时间其中一项，两项都选则叠加规则**
    :type rule_id: int
    :param end_recurring_period: 如果有重复，可选截止日期
    :type end_recurring_period: string
    :param times: 如果有重复事件，可选重复次数
    :type times: int
    :param custom: 如果是自定义每周重复，需要上传custom值，内容为选择的星期 "MO,TU,WE,TH,FR,SA,SU"
    :type custom: string

    **请求示例**

    .. sourcecode:: http

        POST /account/goal_record/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
        "calendar":1,
        "user": 6,
        "start": "2016-01-31 11:00:00",
        "end": "2016-01-31 13:00:00",
        "description": "数据描述",
        "color_event": "#000000",
        "coach": 5
        }

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "id": 2,
        "start": "2016-01-31 11:00:00",
        "end": "2016-01-31 13:00:00",
        "description": "数据描述",
        "end_recurring_period": null,
        "color_event": "#000000",
        "coach": 5,
        "user": 6,
        "rule": null,
        "calendar": 1
        }


删除课程事件
------
.. http:delete:: /schedule/event/<event_id>/

    创建健身目标

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        DELETE /schedule/event/2/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容

重复事件规则
------
.. http:get:: /schedule/rule/

    查看事件重复规则

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /schedule/rule/?user_id=9 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        [
            {
            "id": 1,
            "params":{
                "byweekday":["MO", "TU", "WE", "TH", "FR"]
                },
            "name": "每个工作日",
            "description": "每周一至周五",
            "frequency": "WEEKLY",
            "is_public": true
            },
            {
            "id": 2,
            "params":{
                "byweekday": "weekday"
            },
            "name": "每周今日",
            "description": "每周的星期【今日星期】",
            "frequency": "WEEKLY",
            "is_public": true
            },
            {
            "id": 3,
            "params":{
                "byweekday":["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
            },
            "name": "每天",
            "description": "每天，周一至周日",
            "frequency": "WEEKLY",
            "is_public": true
            },
            {
            "id": 4,
            "params":{
                "bymonthday": "date"
            },
            "name": "每月今日",
            "description": "每月的今天【几号】",
            "frequency": "MONTHLY",
            "is_public": false
            },
            {
            "id": 5,
            "params":{
                "byweekday": "custom"
            },
            "name": "自定义每周",
            "description": "选择每周【周一至周五日期】",
            "frequency": "WEEKLY",
            "is_public": true
            }
        ]

    **特殊说明**:

        如果选择 自定制每周，需要上传custom给 event接口。



课程统计
----
.. http:get:: /schedule/event/analytics/

    课程数据统计

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /schedule/event/analytics/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "month_count": 0,
            "week_count": 0,
            "weekday_report":[
                {
                "11-02": 0
                },
                {
                "11-01": 0
                },
                {
                "10-31": 0
                },
                {
                "10-30": 0
                },
                {
                "10-29": 0
                },
                {
                "10-28": 0
                },
                {
                "10-27": 0
                }
            ],
            "event_total": 8,
            "event_remain": 0
        }

    **返回参数**:

    :param month_count: 本月完成课程数
    :type month_count: int
    :param week_count: 本周完成课程数
    :type week_count: int
    :param event_total: 课程总数
    :type event_total: int
    :param week_count: 剩余课程数
    :type week_count: int
    :param weekday_report: 本周每天课程完成数据
    :type weekday_report: list