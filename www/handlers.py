#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'handlers'

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post
from aiohttp import web
from models import User, Comment, Blog, next_id
from ApiErrorType import APIValueError, APIResourceNotfoundError
from conf import config
import os

COOKIE_NAME = 'awesession'#用来在set_cookie中命名
_COOKIE_KEY = config.config['session']['secret']#导入默认设置



@get('/')
async def index(request):
    """
    users = await User.findall()
    logging.info('###### url : "/" handler : "index" ######')
    #return web.Response(body=b'<h1>hello world!!!</h1>', content_type='text/html')
    return {
        '__template__': 'test.html',
        'users': users
    }
    """
    summary = 'Hello,World.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, create_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, create_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, create_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        'user': request.__user__
    }
"""
@get('/api/users')
async def api_get_users():
    users = await User.findall(orderBy='create_at desc')
    return dict(users = users)
"""
#显示注册页面
@get('/register')#这个作用是用来显示登录页面
def register():
    return {
        '__template__': 'register.html'

    }
#显示登录页面
@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

#制作用户注册api
@post('/api/users')#注意这里路径是'/api/users'，而不是`/register`
async def api_register_usesr(*,name,email,passwd):
    logging.info("api_register_usesr")
    if not name or not name.strip():#如果名字是空格或没有返错，这里感觉not name可以省去，因为在web框架中的RequsetHandler已经验证过一遍了
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd and not _RE_SHA1.match(passwd):
        raise APIValueError('password')
    users = await User.findall(where='email=?', args=[email])#查询邮箱是否已注册，查看ORM框架源码
    if len(users) > 0:
        raise APIError('register:failed','email','Email is already in use.')
    #接下来就是注册到数据库上,具体看会ORM框架中的models源码
    #这里用来注册数据库表id不是使用Use类中的默认id生成，而是调到外部来，原因是后面的密码存储摘要算法时，会把id使用上。
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())#
    await user.save()
    #制作cookie返回浏览器客户端
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user,86400), max_age=86400, httponly=True)        #在注册成功后需要向用户插入一个cookie
    user.passwd = '******'#掩盖passwd
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/authenticate')      #用于用户登录
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findall('email=?', [email])      #根据email 查找用户数据
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()                   #计算hash
    sha1.update(user.id.encode('utf-8'))    #用户的id进入hash            #看之前注册的
    sha1.update(b':')                       #: 进入hash
    sha1.update(passwd.encode('utf-8'))     #用户的秘密进入hash
    if user.passwd != sha1.hexdigest():     #用户密码 和登录的秘密进行比较
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 计算加密cookie:
def user2cookie(user, max_age):     #对返回给用户的cookie 进行加密设置生成日期
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))  #过期时间
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)
# 解密cookie:
async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None