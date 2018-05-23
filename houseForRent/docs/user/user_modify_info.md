### 修改个人信息接口

#### request请求
    POST /user/user
##### params参数：
    user-avatar file 头像
    user-name str 姓名


#### response响应
##### 失败响应1：
    {
        'code':1006,
        'msg':'上传的图片不符合标准'
    }
##### 失败响应2：
    {
        'code':900,
        'msg':'数据库访问失败'
    }
##### 失败响应3：
    {
       'code':1007,
       'msg':'修改的名称在数据库中已存在'
    }
##### 失败响应4：
    {
       'code':901,
       'msg':'登录参数错误'
    }
##### 成功响应：
    {
        "code":200,
        "msg":"请求成功"
    }