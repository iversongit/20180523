OK = 200
SUCCESS = {
            'code':200,
            'msg':'请求成功'
}
DATABASE_ERROR = {
    'code':900,
    'msg':'数据库访问失败'
}
PARAMS_ERROR = {
    'code':901,
    'msg':'登录参数错误'
}
# 用户模块
USER_REGISTER_PARAMS_ERROR = {'code':1000,'msg':'注册信息参数错误'}
USER_REGISTER_MOBILE_ERROR = {'code':1001,'msg':'注册手机号码不符合规则'}
USER_REGISTER_MOBILE_IS_EXISTS = {'code':1002,'msg':'手机号码已注册'}
USER_REGISTER_PASSWORD_IS_ERROR = {'code':1003,'msg':'注册密码两次不一致'}

USER_LOGIN_IS_NOT_EXISTS = {'code':1004,'msg':'用户不存在'}
USER_LOGIN_PASSWORD_IS_ERROR = {'code':1005,'msg':'用户登录密码错误'}

USER_UPLOAD_IMAGE_IS_ERROR = {'code':1006,'msg':'上传的图片不符合标准'}

MODIFY_NAME_IS_EXIST = {'code':1007,'msg':'修改的名称在数据库中已存在'}

AUTH_PARAMS_ERROR = {'code':1008,'msg':'实名认证参数错误'}
AUTH_IDCARD_ERROR = {'code':1009,'msg':'身份证参数错误'}

# 房屋模块
MYHOUSE_USER_IS_NOT_AUTH = {'code':2000,'msg':'用户没有实名认证'}
MYHOUSE_UPLOAD_IMAGE_IS_ERROR = {'code':1006,'msg':'房屋上传的图片不符合标准'}

# 订单模块
ORDER_START_TIME_GT_END_TIME = {'code':3000,'msg':'创建订单时间有误'}

