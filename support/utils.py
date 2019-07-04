#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ikwen.conf.settings")

import logging.handlers
error_log = logging.getLogger('rename_webnode_dbs_collections.error')
error_log.setLevel(logging.ERROR)
error_file_handler = logging.handlers.RotatingFileHandler('rename_dbs.log', 'w', 1000000, 4)
error_file_handler.setLevel(logging.INFO)
error_log.addHandler(error_file_handler)


def rename_ikwen_support_db_collections(*args, **kwargs):
    import pymongo

    db_connect = pymongo.MongoClient('46.101.107.75', 27017)
    dbs = 'ikwen_support'

    database = db_connect[dbs]
    try:
        topic = database['support_subchapter']
        topic.rename('support_topic')
    except:
        pass


if __name__ == "__main__":
    try:
        rename_ikwen_support_db_collections()
    except:
        error_log.error(u"Fatal error occured", exc_info=True)