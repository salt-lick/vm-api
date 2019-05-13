# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsZABBIX(object):
    """Collections of ZABBIX_ESB APIS"""

    def __init__(self, client):
        self.client = client

        self.host_create = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi/zabbix/host_create/',
            description=u'创建新主机'
        )
