# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
from common.log import logger
from account.decorators import login_exempt
from blueking.component.shortcuts import get_client_by_user
from conf import default
import requests
import uuid
import time
import json
import threading


vcenterinfo ={
                "AD_DNS_Domain": "starbucks.net",
                "Action_Engine": "Yes",
                "Add_Description": "Additional Description - Test Bean API Server by idc1_cmdb_test",
                "App_Notes": "Additional Server Notes - Test Bean API Server by idc1_cmdb_test",
                "Backups": "Standard Backup Service",
                "Container_Zone": "1",
                "Description": "Test Bean API Server by idc1_cmdb_test",
                "Environment": "Test",
                "Existing_Container": "00205-sftpprod-prod_00",
                "Location": "DC - Shanghai (China)",
                "Maint_Window": "DOW_020420000400-America_Los_Angeles",
                "Networking": "Existing FGID Container",
                "OS_Disk": "129",
                "OS_Version": "CentOS 7",
                "Quantity": "1",
                "RAM": "4",
                "Request_Type": "New Virtual Server(s)",
                "Severity": "Low",
                "StageAE": "Yes",
                "Support_Queue": "Infrastructure Development",
                "Sustainment_Or_Project": "Sustainment",
                "Total_Storage": "25",
                "Unisys": "No",
                "fgid": "00205",
                "fgid_cost": "00205",
                "uuid": "1d9150ee-610c-11e9-8ab1-0050569306f8",
                "vCPUs": "2"
            }


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def hello(vm):

    print vm


def hostcreate(vm_id):
    """
    创建主机
    """
    time.sleep(2)
    try:
        for i in range(5):
            response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'),
                                    verify=False)
            token = response.headers['x-api-key']
            headers = {'Authorization': token, 'accept': 'application/json'}
            res = requests.get("https://api.starbucks.net/bean-api/api/v1/server/verde/" + str(vm_id), headers=headers,
                               verify=False)
            info = res['data']
            try:
                hostname = info['hostname']
                ip = info['ipAddress']
                kwargs = {
                    "app_code": default.APP_ID,
                    "app_secret": default.APP_TOKEN,
                    "username": "admin",
                    "hostips": ip,
                    "hostgroupids": 1,
                    "templateids": 10050,
                    "host": hostname,
                    "port": 10050
                }

                client = get_client_by_user("admin")
                res = client.zabbix.host_create(kwargs)
                info = res['data']
                hostids = info['hostids'][0]
                logger.info(hostids)
                # return hostids
            except:
                continue
            # else:

                # return hostids

    except Exception as e:
        logger.error(e)
        # hostids = 'failed'
        # return hostids


@login_exempt
def add_vm(request):
    if request.method == 'POST':
        try:
            response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
            token = response.headers['x-api-key']
            headers = {'Authorization': token, 'accept': 'application/json'}
            logger.error(11111)
            logger.error(request.POST)
            # data = request.POST.dict()
            data = json.loads(request.body)
            logger.error(data)
            data = {key: item.replace("&nbsp;", " ") for key, item in data.iteritems()}
            logger.error(data)
            # 替换默认值
            for key, item in vcenterinfo.iteritems():
                if data.has_key(key):
                    vcenterinfo[key] = data[key]
            vcenterinfo["uuid"] = str(uuid.uuid1(int(time.time())))
            res = requests.post("https://api.starbucks.net/bean-api/api/v1/server/verde", headers=headers, verify=False,
                                json=vcenterinfo)
            logger.info(u"add vm")
            logger.info(res.text)
            logger.info(res.json())
            vm_id = res.json()[0]['id']
            res = requests.get("https://api.starbucks.net/bean-api/api/v1/server/verde/" + str(vm_id), headers=headers,
                               verify=False)
            t = threading.Thread(target=hostcreate(vm_id))
            t.start()
            return render_json({
                "data": res.json(),
                "bk_status": True,
                "Message": u"成功",
                "vm_id": vm_id
            })
        except Exception as e:
            return render_json({
                "data": "",
                "bk_status": False,
                "Message": e.message,
                "error:": res.text
            })
    if request.method == 'GET':
        return render_json(
            {
                "AD_DNS_Domain": "starbucks.net",
                "Action_Engine": "Yes",
                "Add_Description": "Additional Description - Test Bean API Server by idc1_cmdb_test",
                "App_Notes": "Additional Server Notes - Test Bean API Server by idc1_cmdb_test",
                "Backups": "Standard Backup Service",
                "Container_Zone": "1",
                "Description": "Test Bean API Server by idc1_cmdb_test",
                "Environment": "Test",
                "Existing_Container": "00205-sftpprod-prod_00",
                "Location": "DC - Shanghai (China)",
                "Maint_Window": "DOW_020420000400-America_Los_Angeles",
                "Networking": "Existing FGID Container",
                "OS_Disk": "129",
                "OS_Version": "CentOS 7",
                "Quantity": "1",
                "RAM": "4",
                "Request_Type": "New Virtual Server(s)",
                "Severity": "Low",
                "StageAE": "Yes",
                "Support_Queue": "Infrastructure Development",
                "Sustainment_Or_Project": "Sustainment",
                "Total_Storage": "25",
                "Unisys": "No",
                "fgid": "00205",
                "fgid_cost": "00205",
                "uuid": "1d9150ee-610c-11e9-8ab1-0050569306f8",
                "vCPUs": "2"
            }
        )


@login_exempt
def vcenter(request, vm_id):
    # if request.method == 'GET':
    #     response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
    #     token = response.headers['x-api-key']
    #     return render_json({
    #         "result": "ok",
    #         "token": token
    #     })

    if request.method == "DELETE":
        logger.info(vm_id)
        if not vm_id:
            return render_json({
                "data": "",
                "bk_status": False,
                "Message": "vm id is required"
            })
        try:
            response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
            token = response.headers['x-api-key']
            headers = {'Authorization': token, 'accept': 'application/json'}
            # data = request.POST['data']
            # logger.info(data)
            logger.info(json.dumps(headers))
            res = requests.delete("https://api.starbucks.net/bean-api/api/v1/server/verde/" + vm_id, headers=headers,
                                  verify=False)
            return render_json({
                "data": res.json(),
                "bk_status": True,
                "Message": u"成功"
            })
        except Exception as e:
            return render_json({
                "data": "",
                "bk_status": False,
                "Message": e.message
            })


@login_exempt
def get_vminfo(request):
    if request.method == 'GET':
        response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
        token = response.headers['x-api-key']
        return render_json({
            "result": "ok",
            "token": token
        })
    if request.method == 'POST':
        try:
            response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
            token = response.headers['x-api-key']
            headers = {'Authorization': token, 'accept': 'application/json'}
            data = json.loads(request.body)
            logger.info(data)
            vm_id = data['id']
            res = requests.get("https://api.starbucks.net/bean-api/api/v1/server/verde/" + str(vm_id), headers=headers,
                               verify=False)
            #todo : 拉取需要的信息（sn）
            return render_json({
                "data": res.json()['data'],
                "bk_status": True,
                "Message": u"成功"
            })
        except Exception as e:
            return render_json({
                "data": "",
                "bk_status": False,
                "Message": e.message,
                "error:": res.text
            })







