#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'handlers'

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

@get('/')
async def index(request):
    users = await User.findall()
    logging.info('indexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindexindex...')
    #return web.Response(body=b'<h1>hello world!!!</h1>', content_type='text/html')
    return {
        '__template__': 'test.html',
        'users': users
    }