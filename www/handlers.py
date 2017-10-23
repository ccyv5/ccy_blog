#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'handlers'

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

import os

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
        'blogs': blogs
    }
