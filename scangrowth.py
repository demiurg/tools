#!/usr/bin/env python3

import os
from peewee import *
import datetime
import argparse
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk


db = SqliteDatabase('history.db', journal_mode='WAL')


class BaseModel(Model):
    class Meta:
        database = db


class Record(Model):
    path = CharField(index=True)
    size = IntegerField()
    is_file = BooleanField()
    delta = IntegerField(null=True)
    rate = FloatField(null=True)
    stamp = DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        database = db


def save(path, size, is_file, level):
    if level > 4:
        return

    stamp = datetime.datetime.now()
    r = Record.create(path=path, size=size, is_file=is_file, stamp=stamp)
    try:
        old = Record.select().where(
            Record.path==path
        ).order_by(
            Record.stamp
        )
        r.delta = size - old[0].size
        r.rate = r.delta / (r.stamp - old[0].stamp).total_seconds()
    except Exception as e:
        pass

    r.save()


def scan(path, v, level=None):
    if level is None:
        level = 0
    else:
        level += 1
    '''Always takes path object'''
    size = 0.0
    for entry in scandir(path):
        stat = entry.stat(follow_symlinks=False)
        if entry.is_file(follow_symlinks=False):
            size += stat.st_size
            save(entry.path, stat.st_size, True, level)
        elif entry.is_dir(follow_symlinks=False):
            size += scan(entry.path, v, level)

    save(path, size, False, level)
    return size


def hbytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--init', dest='init', action='store_true')
    parser.add_argument('-d', '--dir', dest='dir')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.set_defaults(init=False, dir=False, verbose=False)

    args = parser.parse_args()

    db.connect()
    if args.init:
        print('Initializing DB')
        db.create_tables([Record])

    if args.dir:
        if not os.path.exists(args.dir):
            print(args.dir, 'does not exist')
            return
        if not os.path.isdir(args.dir):
            print(args.dir, 'is not a directory')
            return

        path = os.path.realpath(args.dir)
        size = scan(path, args.verbose)
        print("total size of", path, "is", hbytes(size))

if __name__ == '__main__':
    main()
