#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import orm
import asyncio
from models import User, Blog, Comment


@asyncio.coroutine
def test_save(loop):
    yield from orm.create_pool(user='www-data', password='www-data', db='awesome',loop=loop)
    u=User(name='test8',email='test8@test.com',password='test',image='about:blank')
    yield from u.save()

@asyncio.coroutine
def test_remove(loop):
    yield from orm.create_pool(user='www-data', password='www-data', db='awesome',loop=loop)
    users = yield from User.findAll(where='email=?', args=('test8@test.com',))
    for u in users:
        if isinstance(u, orm.Model):
            # 一定要注意加上yield from
            yield from u.remove()

@asyncio.coroutine
def test_remove_direct(loop):
    yield from orm.create_pool(user='www-data', password='www-data', db='awesome',loop=loop)
    affected = yield from User.deleteAll(where='email=?', args=('test8@test.com',))
    print(affected)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_save(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)
