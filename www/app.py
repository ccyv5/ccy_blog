#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__='ccy'

'''
编写Web App骨架
'''

import logging; logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web

import coroweb
import orm
import os
#制作响应函数
async def index(request):
    return web.Response(body=b'<h1>hello world!!!</h1>',content_type='text/html')

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json, time
import logging
from handlers import cookie2user,COOKIE_NAME



#初始化jinja2，以便其他函数使用jinja2模板
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

async def logger_factory(app, handler):
    async def logger(request):
        # 记录日志:
        logging.info('Request: %s %s' % (request.method, request.path))
        # 继续处理请求:
        return (await handler(request))
    return logger
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data
#response_factory 拦截器 在处理一些url 是 直接返回web.response 的内容,不在麻烦到url中处理

#绑定解析cookie的中间件
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        logging.info("auth_factory##### %s" % (str(request.__user__),) )
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        return (await handler(request))
    return auth

async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        logging.info("response_factory##### %s" % (str(request.__user__),))
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))      #使用模板
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response




async def init(loop):#Web app服务器初始化
    #app = web.Application(loop=loop)#制作响应函数集合
    app = web.Application(loop=loop, middlewares=[
        logger_factory,auth_factory,response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))    #模板输出话初始化
    #app.router.add_route(method='GET',path='/',handler=index)#把响应函数添加到响应函数集合
    await orm.create_pool(loop, user='www-data', password='www-data', db='awesome')
    coroweb.add_routes(app, "handlers")     #将handlers 模块中的函数和url进行绑定
    coroweb.add_static(app)
    srv = await loop.create_server(app.make_handler(),'0.0.0.0',8000)
    logging.info('server start at http://0.0.0.0:8000')#创建服务器(连接网址、端口，绑定handler)
    return srv


loop = asyncio.get_event_loop()#创建事件
loop.run_until_complete(init(loop))#运行
loop.run_forever()#服务器不关闭