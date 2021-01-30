# 一、JWT认证

用户注册或登录成功后，要保存用户登录状态。已经知道了cookie和session两种状态认证方式，但是它们都有缺点。
* cookie由于信息保存在用户的浏览器之上，用户信息安全不能够保证。
* session是将用户信息保存在服务端，返回给用户一个随机字符串。当用户登录过多时，会造成服务器数据压力大。对于服务器的集群部署支持不好。
    ![](https://images.gitee.com/uploads/images/2021/0130/103150_d371cec0_7841459.jpeg "基于session认证.jpg")
    
    ![](https://images.gitee.com/uploads/images/2021/0130/103226_9a7d3c49_7841459.jpeg "基于session认证集群部署.jpg")

为了解决上述问题，将用户的特征信息，及特征信息的加密数据存放在浏览器。每当用户访问时，都会携带着这个信息，在服务进行认证。基于JSON数据格式的。将这种认证称为Json Web Token，实际就是token认证。

![](https://images.gitee.com/uploads/images/2021/0130/103618_b264a0bc_7841459.jpeg "jwt认证.jpg")

![](https://images.gitee.com/uploads/images/2021/0130/103634_2d9c66be_7841459.jpeg "jwt认证集群部署.jpg")

## 1.1 JWT的构成和工作原理
### JWT的构成
JWT就是一段字符串，由三段信息构成的，将这三段信息文本用.链接一起就构成了Jwt字符串。就像这样
```python
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```
*  **第一部分** 我们称它为头部（header): 头部承载两部分信息
    1. 声明类型，这里是jwt
    2. 声明加密的算法 通常直接使用 `HMACSHA256`
    
    头部信息是像这样的
    ```python
    {
      'typ': 'JWT',
      'alg': 'HS256'
    }
    ```
    然后进行base64编码后的信息
    ```python
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
    ```
        
*  **第二部分** 我们称其为载荷（payload, 类似于飞机上承载的物品): 存放有效信息的地方, 包含三部分内容
    1. 标准中注册的声明
        * iss:  **jwt签发者** 
        * sub:  **jwt所面向的用户** 
        * aud: 接收jwt的一方
        * exp:  **jwt的过期时间，这个过期时间必须要大于签发时间** 
        * nbf: 定义在什么时间之前，该jwt都是不可用的.
        * iat: jwt的签发时间
        * jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避时序攻击。
    2. 公共的声明

        公共的声明可以添加任何的信息，一般添加 **用户的相关信息或其他业务需要的必要信息** .但不建议添加敏感信息，因为该部分在客户端可解密.

    3. 私有的声明

        私有声明是 **提供者和消费者** 所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息
    
    定义一个payload:
    ```python
    {
      "sub": "1234567890",
      "name": "John Doe",
      "admin": true
    }
    ```
    然后将其进行base64编码，得到JWT的第二部分
    ```python
    eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9
    ```
    
*  **第三部** 分是签证（signature): 是一个签证信息，这个签证信息由三部分组成

    1.  **header**  (base64后的)
    2.  **payload**  (base64后的)
    3.  **secret** 
    
    这个部分需要base64编码后的header和base64编码后的payload使用`.`连接组成的字符串，然后通过header中声明的加密方式进行加盐`secret`组合加密，然后就构成了jwt的第三部分
    ```js
    // javascript
    var encodedString = base64UrlEncode(header) + '.' + base64UrlEncode(payload);
    
    var signature = HMACSHA256(encodedString, 'secret'); // TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
    ```

将这三部分用`.`连接成一个完整的字符串,构成了最终的jwt
```python
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

 **注意：secret是保存在服务器端的，jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。一旦客户端得知这个secret, 那就意味着客户端是可以自我签发jwt了** 

### JWT原理

1. jwt分三段式：头.体.签名 （head.payload.sgin）

2.  **头和体是可逆加密** ，让服务器可以反解出user对象； **签名是不可逆加密** ，保证整个token的安全性的

3. 头体签名三部分， **都是采用json格式的字符串** ，进行加密，可逆加密一般采用base64算法，不可逆加密一般采用hash(md5)算法

4. 头中的内容是基本信息：公司信息、项目组信息、token采用的加密方式信息
    ```python
    {
    	"company": "公司信息",
    	...
    }
    ```

5. 体中的内容是关键信息：用户主键、用户名、签发时客户端信息(设备号、地址)、过期时间
    ```python
    {
    	"user_id": 1,
    	...
    }
    ```
6. 签名中的内容时安全信息：头的加密结果 + 体的加密结果 + 服务器不对外公开的安全码 进行md5加密
    ```python
    {
    	"head": "头的加密字符串",
    	"payload": "体的加密字符串",
    	"secret_key": "安全码"
    }
    ```

**签发：根据登录请求提交来的 账号 + 密码 + 设备信息 签发 token**

```python
"""
1）用基本信息存储json字典，采用base64算法加密得到 头字符串
2）用关键信息存储json字典，采用base64算法加密得到 体字符串
3）用头、体加密字符串再加安全码信息存储json字典，采用hash md5算法加密得到 签名字符串

账号密码就能根据User表得到user对象，形成的三段字符串用 . 拼接成token返回给前台
"""
```

**校验：根据客户端带token的请求 反解出 user 对象**
```python

"""
1）将token按 . 拆分为三段字符串，第一段 头加密字符串 一般不需要做任何处理
2）第二段 体加密字符串，要反解出用户主键，通过主键从User表中就能得到登录用户，过期时间和设备信息都是安全信息，确保token没过期，且时同一设备来的
3）再用 第一段 + 第二段 + 服务器安全码 不可逆md5加密，与第三段 签名字符串 进行碰撞校验，通过后才能代表第二段校验得到的user对象就是合法的登录用户
"""
```

**drf项目的jwt认证开发流程**

```python
"""
1）用账号密码访问登录接口，登录接口逻辑中调用 签发token 算法，得到token，返回给客户端，客户端自己存到cookies中

2）校验token的算法应该写在认证类中(在认证类中调用)，全局配置给认证组件，所有视图类请求，都会进行认证校验，所以请求带了token，就会反解出user对象，在视图类中用request.user就能访问登录的用户

注：登录接口需要做 认证 + 权限 两个局部禁用
"""
```

# 二、drf-jwt安装和简单使用

## 2.1 安装
```python
pip install djangorestframework-jwt
```

## 2.2 使用
### 2.2.1 基于Django自带的认证模块

**自定义user表**
```python
from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    phone = models.CharField(max_length=12, verbose_name='手机号码')
    icon = models.ImageField(upload_to='icon', verbose_name='头像')
```
在配置文件中添加如下配置
```python
# 支持头像
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'api.UserInfo'
```
* **在INSTALL_APP中注册**


**执行数据库迁移命令** 
```python
python manage.py makemigrations
python manage.py migrate
```

**创建超级用户**
```python
python3 manage.py createsuperuser
```

**配置路由`urls.py`**
```python
from rest_framework_jwt.views import obtain_jwt_token
"""
JSONWebTokenAPIView: drf_jwt的认证基类

ObtainJSONWebToken，VerifyJSONWebToken，RefreshJSONWebToken：继承基类，实现认证
"""

urlpatterns = [
    path('login/', obtain_jwt_token),
]
```
完成之后，就可以使用了。
![](https://images.gitee.com/uploads/images/2021/0130/131306_c8277beb_7841459.png "屏幕截图.png")

下面使用drf-jwt提供的认证，编写如下视图类
```python
class View(APIView):
    def get(self, request):
        return Response("ok")
```
配置全局认证(`settings.py`)
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
}
```
配置访问接口
```python
from api.views import View
urlpatterns = [
    ...
    path('books/', View.as_view())
]
```
访问该接口
![](https://images.gitee.com/uploads/images/2021/0130/131659_30768875_7841459.png "屏幕截图.png")
* 必须要在`Headers`中添加一个`Authorization`属性，该属性的值为`JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj`这样才会通过认证。 **如果不带`JWT `(末尾有个空格)不会进行认证。** 

### 2.2.2 自定义JWT认证类

```python
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework import exceptions


class TokenAuthenticate(BaseJSONWebTokenAuthentication):
    # 1. 获取jwt_token字符串
    # 2. 反解出payload，
    # 3. 通过payload反解出用户
    # 返回一个元组(user, None)
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)  # 获取jwt字符串
        if not jwt_value:
            raise exceptions.AuthenticationFailed("用户未登录")
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("登录过期")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("用户非法")
        user = self.authenticate_credentials(payload)
        return user, jwt_value

    @staticmethod
    def get_jwt_value(request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        return auth
```