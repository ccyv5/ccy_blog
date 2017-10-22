#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = 'Michael Liao'

configs = {
    'debug': True,
    'db': {
        'host': '0.0.0.0',
        'port': 3306,
        'user': 'www-data',
        'password': 'www-data',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}