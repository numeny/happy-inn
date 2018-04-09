#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging

sys.path.append("../")

def get_my_logger():
    logger = logging.getLogger('YLInfoRestHomeSpider')
    return logger
