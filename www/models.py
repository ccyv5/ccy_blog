#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
创建model
'''

__author__='ccy'

import uuid,time
import asyncio
import orm
from orm import Model,StringField,IntegerField,BooleanField,TextField,FloatField

def next_id():#随机生成id
    return '%015d%s000'%(int(time.time()*1000),uuid.uuid4().hex)

class User(Model):
    __tablename__ = 'users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email =  StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')#注意由于是image，所以这里接受字节是500
    create_at = FloatField(default=time.time)

class Blog(Model):
    __tablename__ = 'blogs'
    id = StringField(primary_key=True, default=next_id,ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    create_at = FloatField(default=time.time)

class Comment(Model):
    __tablename__ = 'comments'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    create_at = FloatField(default=time.time)

if __name__== '__main__':

    async def test():
        await orm.create_pool(loop,user='www-data', password='www-data', db='awesome')
        u = User(name='Test3', email='test3@example.com', passwd='123456780', image='about:blank')
        await u.save()
        a = await u.findall() #这个要打印才显示出来
        print(a)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    orm.__pool.close()  #在关闭event loop之前，首先需要关闭连接池。
    loop.run_until_complete(orm.__pool.wait_closed())#在关闭event loop之前，首先需要关闭连接池。
    loop.close()