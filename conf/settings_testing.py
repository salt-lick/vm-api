# -*- coding: utf-8 -*-
"""
用于测试环境的全局配置
"""
from settings import APP_ID, BASE_DIR
import os


# ===============================================================================
# 数据库设置, 测试环境数据库设置
# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    },
}
