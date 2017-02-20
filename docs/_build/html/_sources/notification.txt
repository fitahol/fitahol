消息通知
====

获取所有通知
------
.. http:get:: /notification/

    获取用户所有通知, 默认分页

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "count": 2,
        "next": null,
        "previous": null,
        "results":[
            {
            "id": 2,
            "description": "绑定[用户8 & 用户3]关系确认 ~ 7 分钟 之前",
            "show_time": "2016-06-16 19:13:23",
            "unread": true,
            "target": "",
            "action_type": "userrelationconfirm",
            "action_object_id": "7",
            "extra":{}
            },
            {
            "id": 3,
            "description": "绑定[用户8 & 用户3]关系确认 ~ 7 分钟 之前",
            "show_time": "2016-06-16 19:13:23",
            "unread": true,
            "target": "",
            "action_type": "userrelationconfirm",
            "action_object_id": "7",
            "extra":{}
            }
            ]
        }

    **返回参数说明**

    :param id: 通知id
    :type id: int

    :param level: 通知类型: (0, '通知')(1, '私信'), (2, '评论'), (3, '@我'); 1.0版暂时只有level=0
    :type level: string

    :param description: 通知内容描述
    :type description: string

    :param unread: 是否已读
    :type unread: bool

    :param target: 跳转类型: 空为不跳转, http:// 开头为跳转网页, app:// 开头为跳转界面
    :type target: string

    :param action_type: 事件类型协定; 如userrelationconfirm指绑定关系确认
    :type action_type: string

    :param action_object_id: 事件类型对应ID, 无值则跳列表
    :type action_object_id: int

    :param extra: 附加参数
    :type extra: json


获取未读通知
------
.. http:get:: /notification/unread/

    获取用户未读通知, 不分页

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/unread/ HTTP/1.1
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
        "id": 2,
        "description": "绑定[用户8 & 用户3]关系确认 ~ 7 分钟 之前",
        "show_time": "2016-06-16 19:13:23",
        "unread": true,
        "target": "",
        "action_type": "userrelationconfirm",
        "action_object_id": "7",
        "extra":{}
        }
    ]

    **参数说明同上**


所有未读通知置为已读
----------
.. http:get:: /notification/mark_all_read/

    将所有未读的通知,置为已读状态

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/mark_all_read/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "detail": "请求成功"
        }

指定通知置为已读
--------
.. http:get:: /notification/mark_read/<notification_id>/

    指定通知id,置为已读状态

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/mark_read/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "detail": "请求成功"
        }

指定通知置为未读
--------
.. http:get:: /notification/mark_unread/<notification_id>/

    指定通知id,置为已读状态

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/mark_unread/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "detail": "请求成功"
        }

获取未读通知总数
--------
.. http:get:: /notification/unread_count/

    指定通知id,置为已读状态

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /notification/mark-unread/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "unread_count": 8
        }

删除通知
----
.. http:delete:: /notification/<notification_id>/

    指定通知id, GET请求获取详细, DELETE 请求删除通知

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        DELETE /notification/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
            "detail": "请求删除成功"
        }

