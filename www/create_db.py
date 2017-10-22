#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ccy'

#在终端键入mysql
#键入create database awesome;
#键入exit();  退出mysql
import pymysql
conn = pymysql.connect(user='root', password='',port=3306, database='awesome')#连接MySQL数据库中的awesome数据库
cursor = conn.cursor()#创建游标
cursor.execute('create table users (id varchar(50) primary key,email varchar(50),passwd varchar(50),name varchar(50),image varchar(500),admin boolean,create_at real)')#创建users表-->表列都要定义名字及类型，主键后还要跟primary key
cursor.execute('create table blogs (id varchar(50) primary key,user_id varchar(50),user_name varchar(50),user_image varchar(500),name varchar(50),summary varchar(200),content text,create_at real)')#创建blogs表
cursor.execute('create table comments (id varchar(50) primary key,blog_id varchar(50),user_id varchar(50),user_name varchar(50),user_image varchar(500),content text,create_at real)')#创建comments表
cursor.close()
conn.close()
# 无法创建新表

#在终端键入mysql
#键入mysql
#键入show databas;   显示当前的所有数据库
#键入use awesome;    使用awesome 数据库
#键入show tables;    显示数据库中的所有表
#键入describe tablename:显示表的属性:  如 describe users;
#键入select * from tablename :显示表的所有内容
#键入exit()
