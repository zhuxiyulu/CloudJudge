
# 前台信息编码表
FrontMessageCode = {}
# 后台信息编码表
BackMessageCode = {}


# 编码、语言
FrontMessageCode['1'] = {"Help": "Username_Empty", "Zh": "用户不能为空"}
FrontMessageCode['2'] = {"Help": "Password_Empty", "Zh": "密码不能为空"}
FrontMessageCode['3'] = {"Help": "Username_NotEqual_Password", "Zh": "用户名和密码不匹配"}
FrontMessageCode['4'] = {"Help": "LogoutFailed", "Zh": "登出失败"}
FrontMessageCode['5'] = {"Help": "Captcha_Empty", "Zh": "验证码不能为空"}
FrontMessageCode['6'] = {"Help": "Captcha_Wrong", "Zh": "验证码错误"}
FrontMessageCode['7'] = {"Help": "User_Exists", "Zh": "该用户名已存在"}


for key in FrontMessageCode.keys():
    BackMessageCode[FrontMessageCode[key]['Help']] = key

def getFrontMessage():
    return FrontMessageCode

def getBackMessage():
    return BackMessageCode