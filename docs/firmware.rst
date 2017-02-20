
固件接口
====

发送验证码
-----

.. http:get:: /firmware/valid_code/?account=(account)

    发送验证码接口, account可以是手机号或邮箱,自动识别发送到相应的帐户中

    **请求参数**:

    :param account: 用户帐户
    :type account: string
    :param v_type: 验证码类型: 不传为默认值register表示注册验证码; 重置密码请求 reset_pwd
    :type v_type: string

    **示例请求**:

    .. sourcecode:: http

        GET /firmware/valid_code/?account=fitahol@163.com HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 处理成功
    :statuscode 400: 参数错误

        :code 10001: 注册帐户已存在
        :code 10002: 重置密码用户不存在

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "发送成功,请注意查收",
        }

    **错误返回**:

    - 注册帐户已存在:

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "帐户已存在, 请直接登陆",
        }

    - 重置密码帐户不存在

    .. sourcecode:: http

        HTTP/1.1 404 NOT FOUND
        Vary: Accept
        Content-Type: application/json

        {
        "detail": "用户帐户不存在",
        }



版本号更新
-----

.. http:get:: /firmware/(ios|android)/upgrade/?version=(1.0.0)

    版本更新接品，版本号默认为 x.x.x 三位，单位数。

    **请求参数**:

    :param version: 当前版本号
    :type version: string

    **示例请求**:

    .. sourcecode:: http

        GET /firmware/ios/upgrade/?version=1.0.0 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 处理成功
    :statuscode 400: 参数错误

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {"id": 1, "url": "下载地址", "version": "", "desc": "升级描述信息", "is_force": true}

        is_force 表示是否强制升级

    **错误返回**:

    - 暂无新版本，返回空 :

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Vary: Accept
        Content-Type: application/json

        {}
