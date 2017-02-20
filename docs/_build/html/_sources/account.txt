
用户接口
====

注册新用户
-----

.. http:post:: /account/register/

    注册新用户, account可以是手机号或邮箱,自动识别主册帐户

    **请求参数**:

    :param account: 注册帐户
    :type account: string
    :param password: 密码
    :type password: string
    :param rpt_password: 确认密码
    :type rpt_password: string
    :param valid_code: 4位数字验证码
    :type valid_code: string

    **请求示例**

    .. sourcecode:: http

        POST /account/register/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "account": "18600432852",
            "password": "123212312",
            "rpt_password": "123212312",
            "valid_code": "1236"
        }

    **返回状态码**:

    :statuscode 200: 注册成功
    :statuscode 400: 参数缺失或错误

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 201 OK
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "注册成功",
        }

    **错误返回**:

    - 密码不相同:

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "密码不相同",
        }

    - 验证码不符

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "验证码不符,请重新输入",
        }

用户登录
----

.. http:post:: /account/login/

    用户登录, account可以是手机号或邮箱,自动识别主册帐户

    **请求参数**:

    :param account: 用户帐户
    :type account: string
    :param password: 密码
    :type password: string


    **请求示例**

    .. sourcecode:: http

        POST /account/login/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "account": "18600432852",
            "password": "123212312",
        }

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 400: 参数缺失或错误

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "gender": "0",
        "id": 9,
        "detail": "登录成功",
        "age": "0",
        "weight": "0",
        "portrait": "",
        "date_joined": "2016-06-14 17:09:50",
        "height": "0",
        "nickname": "18600432852",
        "token": "6fab6f6a67ba10ddda5fc976154a33752695d413"
        }

    **错误返回**:

    - 用户名或密码错误:

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "用户名或密码错误",
        }


微信小程序登录
-------

.. http:post:: /wechat/wx/

    小程序登录，进入获取 code和用户信息后调用

    **请求参数**:

    :param account: 用户帐户
    :type account: string
    :param password: 密码
    :type password: string


    **请求示例**

    .. sourcecode:: http

        POST /account/login/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "nickName":"vividma",
            "gender":2,
            "language":"zh_CN",
            "city":"Chaoyang",
            "province":"Beijing",
            "country":"CN",
            "avatarUrl":"http://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjTP6X5nGOexhIYTSUaZh3MeeN6bKQveclgQsqc8EFX4nQBFrsxgqCOyBlAIsx5XaNJKibt7zkKiag/0",
            "code":"021tRNQQ07bJQa2mCLQQ0VMLQQ0tRNQ7",
            "u_type":1
        }

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 400: 参数缺失或错误

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        教练端返回：

        {
            "token":"443098a5da938a5408ecf891e6de27e453994636",
            "user_id":10052,
            "gym":null,
            "id":53,
            "u_type":1,
            "expert_tags":[],
            "user":
                {
                    "id":10052,
                    "nickname":"vividma",
                    "portrait":"http://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjTP6X5nGOexhIYTSUaZh3MeeN6bKQveclgQsqc8EFX4nQBFrsxgqCOyBlAIsx5XaNJKibt7zkKiag/0",
                    "user_id":10052,
                    "intro":"undefined 北京"
                }
        }

        学员端返回：

        {
            "token":"b9d3230ec331fc248054c267e3a58af4e3aca274",
            "u_type":0,
            "user_id":10053,
            "coach":
                {
                    "id":50,
                    "gym":null,
                    "expert_tags":[],
                    "user":{"id":10049,"nickname":"Fitahol","portrait":"http://wx.qlogo.cn/mmopen/vi_32/4612iaEeX1TtEyzruUPDX5DDTetPCKeOIvibvpAbIXxsqu1O5n52a1gannVywj4T7gUUobaCLD3s7aia2nJZSFLZQ/0","user_id":10049,"intro":""}
                }
        }

    **错误返回**:

    - 服务异常时会出现



重置密码
----

.. http:post:: /account/reset_pwd/

    用户重置密码, account可以是手机号或邮箱, 需要先发送验证码

    **请求参数**:

    :param account: 用户帐户
    :type account: string
    :param password: 密码
    :type password: string
    :param valid_code: 验证码
    :type valid_code: string

    **请求示例**

    .. sourcecode:: http

        POST /account/reset_pwd/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "account": "18600432852",
            "password": "123212312",
            "valid_code": "1232",
        }

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 400: 参数缺失或错误

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "重置成功",
        }

    **错误返回**:

    - 验证码错误:

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "验证码错误",
        }
    - 用户帐户不存在

    .. sourcecode:: http

        HTTP/1.1 404 NOT FOUND
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "用户帐户不存在",
        }


个人中心
----

.. http:post:: /account/(user_id)/

    获取用户个人相关信息, 集成个人信息 帐户信息等

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        POST /account/3/ HTTP/1.1
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

        **教练返回**
        {
        "unread_count": 4,
        "user":{
            "date_joined": "2016-05-04 10:35:29",
            "id": 8,
            "nickname": "18600153507",
            "portrait": "",
            "gender": "0",
            "age": "0",
            "height": "0",
            "weight": "0"
        },
        "coach":{
            "gym":{"id": 1, "name": "麦加健身", "score": 10, "address": "", "telephone": "",…},
            "expert_tags":[
            {
            "id": 1,
            "name": "减脂",
            "desc": "减脂圣经"
            },
            {
            "id": 2,
            "name": "增肌",
            "desc": "肌肉维度"
            }
            ],
            "intro": "教练李辉",
            "experience": 3  //资历年限
        }
        }

        **学员返回**
        {
        "unread_count": 4,
        "user":{
            "date_joined": "2016-06-14 17:09:50",
            "id": 9,
            "nickname": "18600432852",
            "portrait": "",
            "gender": "0",
            "age": "0",
            "height": "0",
            "weight": "0"
        },
        "member":{
            "fit_goal":[
                {
                "id": 1,
                "name": "减脂增肌",
                "measure": "Kg",
                "goal": 0,
                "is_public": false
                }
            ],
            "gym":{
                "id": 1,
                "name": "麦加健身",
                "score": 10,
                "address": "",
                "telephone": "",
                "lat": 0,
                "lng": 0,
                "city": null
            },
            "intro": "马德岭"
        }
        }


查找用户
----
.. http:get:: /account/profile/?query=189324214324

    查找用户，返回用户个人信息

    **请求参数**:

    需要 Token 认证通过

    :param query: 查询参数，支持手机号/UID/用户名
    :type query: string

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
            "date_joined": "2016-06-14 17:09:50",
            "id": 9,  // 用户ID
            "nickname": "18600432852",
            "portrait": "",
            "gender": "0",  // 0未知,1男性,2女性
            "age": "0",
            "height": "0",
            "weight": "0"
            }
        ]


获取用户基本信息
--------
.. http:get:: /account/profile/(user_id)/

    获取用户基本用户信息

    **请求参数**:

    无, 需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /account/profile/3/ HTTP/1.1
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
        "date_joined": "2016-06-14 17:09:50",
        "id": 9,  // 用户ID
        "nickname": "18600432852",
        "portrait": "",
        "gender": "0",  // 0未知,1男性,2女性
        "age": "0",
        "height": "0",
        "weight": "0",
        "intro": "个性签名"
        }


更新用户信息
------
.. http:patch:: /account/profile/(user_id)/

    更新用户基本信息, put 为全量更新, 支持使用 patch 传单项数据进行更新

    **请求参数**:

    需要 Token 认证通过

    :param nickname: 用户昵称
    :type nickname: string
    :param intro: 个性签名／简介
    :type intro: string
    :param weight: 体重,单位kg
    :type weight: int
    :param height: 身高, 单位cm
    :type height: int
    :param age: 年龄
    :type age: int
    :param gender: 性别, 0未知,1男性,2女性
    :type gender: int
    :param gym_id: 健身房ID，如果不存在需要引导用户创建
    :type gym_id: int
    :param expert_tags: 擅长领域IDs，多个数据以,间隔："1,23,12,34"
    :type expert_tags: string

    **请求示例**

    .. sourcecode:: http

        PATCH /account/profile/3/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "nickname": "马德岭",
            "weight": 80,
            "height": 178,
            "age": 27,
            "gender": 0,
            "intro: "更新签名"
        }

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
            "detail": "更新成功"
        }


头像上传
----
.. http:post:: /account/portrait/

    用户头像文件上传

    **请求参数**:

    需要 Token 认证通过

    portrait 头像文件名称, 需要前端压缩文件，网页端按 base64上传

    type 文件类型

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
            "detail": "上传成功"
        }



学员列表
----
.. http:get:: /account/member/

    获取学员列表

    **请求参数**:

    需要 Token 认证通过

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
            "user_id": 9,
            "nickname": "18600432852",
            "gender": "0",
            "portrait": ""
            }
        ]


学员ID/名称列表
---------
.. http:get:: /account/member/card/

    学员ID/名称列表, 用在课程选择显示所有学员名称处。 同时返回头像地址

    **请求参数**:

    需要 Token 认证通过

    :param query: 查询参数，支持手机号/UID/用户名
    :type query: string

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
            "user_id": 10008,
            "nickname": "小助手",
            "portrait": "头像地址"
            }
        ]


查询教练学员
------
.. http:get:: /account/member/?query=189324214324

    查询学员，仅包括查询教练自己的学员； 建议本查询使用本地缓存，避免使用接口

    **请求参数**:

    需要 Token 认证通过

    :param query: 查询参数，支持手机号/UID/用户名
    :type query: string

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
            "user_id": 9,
            "nickname": "18600432852",
            "gender": "0",
            "portrait": ""
            }
        ]


学员详情
----
.. http:get:: /account/member/(user_id)/

    更新用户基本信息

    **请求参数**:

    需要 Token 认证通过

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
            "fit_goal":[
                {
                    "id": 1,
                    "name": "减脂增肌",
                    "measure": "Kg",
                    "goal": 0,
                    "is_public": false
                }
            ],
            "user":{
                date_joined": "2016-06-14 17:09:50",
                "id": 9,
                "nickname": "18600432852",
                "portrait": "",
                "gender": "0",
                "age": "0",
                "height": "0",
                "weight": "0"
            },
            "gym":{
                "id": 1,
                "name": "麦加健身",
                "score": 10,
                "address": "",
                "telephone": "",
                "lat": 0,
                "lng": 0,
                "city": null
            },
            "intro": "马德岭"
        }


个人私教列表
------
.. http:get:: /account/coach/personal/

    获取学员私人教练

    **请求参数**:

    需要 Token 认证通过

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
                "gym": null,
                "expert_tags":[
                    {"id": 3, "name": "增肌塑体", "desc": "增肌塑体", "is_public": true…},
                    {"id": 4, "name": "减脂塑型", "desc": "减脂塑型", "is_public": true…}
                    ],
                "user":{
                    "id": 10008,
                    "nickname": "小助手",
                    "portrait": "http://www.fitahol.com/media/account/portrait/fitahol-icon.jpg"
                    }
            },
            {
                "gym": null,
                "expert_tags":[
                    {"id": 3, "name": "增肌塑体", "desc": "增肌塑体", "is_public": true…},
                    {"id": 4, "name": "减脂塑型", "desc": "减脂塑型", "is_public": true…}
                    ],
                "user":{
                    "id": 10037,
                    "nickname": "随便写",
                    "portrait": "http://www.fitahol.com/media/icon/fitness-boy.png"
                }
            }
        ]

    **返回参数**:

    :param gym: 所在健身房
    :type gym: string
    :param expert_tags: 擅长领域
    :type expert_tags: list
    :param user: 个人信息
    :type user: json


学员/教练请求列表
---------
.. http:get:: /account/relation/

    学员/教练请求列表, 数据分页; 同微信新的朋友界面

    **请求参数**:

    需要 Token 认证通过

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求示例**

    .. sourcecode:: http

        GET /account/relation/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "count": 8,
        "next": null,
        "previous": null,
        "results":[
            {
            "id": 1,
            "sender":{"id": 8, "nickname": "18600153507", "portrait": ""},
            "recipient":{"id": 3, "nickname": "lingnck@163", "portrait": ""},
            "ref_type": "add_member",
            "status": 0,
            "ctime": "2016-06-16 15:43:20"
            },
            {"id": 2, "sender":{"id": 8, "nickname": "18600153507", "portrait": ""…},
        ]
        }

    **返回参数**:

    :param ref_type: 添加类型 ("add_member", "添加学员"), ("add_coach", "添加教练"), ("add_friend", "添加好友"),("add_follow", "添加关注")
    :type ref_type: string
    :param status: 接受状态 (1, "接受"), (-1, "拒绝"), (0, "等待回应"),
    :type status: int
    :param ctime: 请求时间
    :type ctime: string
    :param sender: 发送人信息
    :type sender: json
    :param sender: 接收方信息
    :type sender: json


请求添加学员/教练
---------
.. http:post:: /account/relation/

    添加新学员

    **请求参数**:

    需要 Token 认证通过

    user_id 对应的添加 用户id； 系统自动识别用户身份添加关系

    **请求示例**

    .. sourcecode:: http

        POST /account/relation/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "user_id": 9
        }

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
        "detail": "添加成功,请等待对方验证",
        }

确认添加学员/教练
---------
.. http:post:: /account/relation/<relation_id>/

    确认添加新学员或教练; 添加请求会以通知方式发给对方, 在通知中点击查看是否确认添加

    **请求参数**:

    需要 Token 认证通过

    status 接受状态, 拒绝为-1, 接受为1

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        拒绝对方:

            {
            "detail": "已拒绝对方请求",
            }

        确认添加:

            {
            "detail": "确认成功",
            }


删除教练与学员关联
---------
.. http:post:: /account/del/relation/

    删除学员与教练关联

    **请求参数**:

    需要 Token 认证通过

    需要上传对应的 删除人员【学员／教练】 user_id

    **请求示例**

    .. sourcecode:: http

        POST /account/del/relation/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {"user_id": 10008}

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    {"detail": "删除成功"}

最近几张照片形象
--------
.. http:get:: /account/figure/latest/

    获取照片

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /account/figure/?user_id=6 HTTP/1.1
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
            "figure": "http://0.0.0.0:9999/media/account/figure/s25505835.jpg",
            "desc": "i try",
            "ctime": "2016-01-30 15:09:07",
            "user_id": 6
            }
        ]

    **返回参数**:

    :param figure: 照片地址
    :type figure: string
    :param desc: 描述
    :type desc: string

照片形象
----
.. http:get:: /account/figure/

    获取照片

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /account/figure/?user_id=6 HTTP/1.1
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
        "count": 1,
        "next": null,
        "previous": null,
        "results":[
            {
            "id": 1,
            "figure": "http://0.0.0.0:9999/media/account/figure/s25505835.jpg",
            "desc": "i try",
            "ctime": "2016-01-30 15:09:07",
            "user_id": 6
            }
        ]
        }

    **返回参数**:

    :param figure: 照片地址
    :type figure: string
    :param desc: 描述
    :type desc: string


添加照片形象
------
.. http:post:: /account/figure/

    添加照片形象

    **请求参数**:

    需要 Token 认证通过； figure和 figure_file 可选，一种是base64压缩数据，一种文件本身

    :param user_id: 学员用户id
    :type user_id: int
    :param figure: 形象照片, 文件上传需要压缩传为base64数据
    :type figure: string
    :param figure_file: 形象照片, 可直接上传文件，需要 multipart/form-data支持
    :type figure_file: file
    :param cdate: 日期选择
    :type cdate: string
    :param desc: 描述
    :type desc: string

    **请求示例**

    .. sourcecode:: http

        POST /account/figure/ HTTP/1.1
        Host: api.fitahol.com
        Accept: multipart/form-data


    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

    {
    "id": 2,
    "figure": "http://0.0.0.0:9999/media/account/figure/s25505835_uoR8YlH.jpg",
    "desc": "描述",
    "utime": "2016-01-30 15:19:33",
    "user_id": 6
    }


删除照片形象
------
.. http:delete:: /account/figure/<figure_id>/

    创建照片形象

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        DELETE /account/figure/1/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容
