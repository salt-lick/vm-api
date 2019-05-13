# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
from common.log import logger
from account.decorators import login_exempt
import requests
import uuid
import time
import json


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


@login_exempt
def add_vm(request):
    if request.method == 'POST':
        try:
            response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
            token = response.headers['x-api-key']
            headers = {'Authorization': token, 'accept': 'application/json'}
            logger.error(11111)
            logger.error(request.POST)
            data = request.POST.dict()
            logger.error(data)
            data = {key: item.replace("&nbsp;", " ") for key, item in data.iteritems()}
            logger.error(data)
            # data = request.POST['data']
            # body_data = request.body['data']
            # logger.error(body_data)
            # logger.info(body_data)
            # logger.error(data)
            # logger.info(data)
            # logger.debug(data)
            data["uuid"] = str(uuid.uuid1(int(time.time())))
            res = requests.post("https://api.starbucks.net/bean-api/api/v1/server/verde", headers=headers, verify=False,
                                json=data)
            logger.info(u"add vm")
            logger.info(res.text)
            logger.info(res.json())
            vm_id = res.json()[0]['id']
            res = requests.get("https://api.starbucks.net/bean-api/api/v1/server/verde/" + str(vm_id), headers=headers,
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
    if request.method == 'GET':
        response = requests.get("https://api.starbucks.net/auth", auth=('S-Cmdbcn', 'K{RTOLtTP^*Muc#'), verify=False)
        token = response.headers['x-api-key']
        return render_json({
            "result": "ok",
            "token": token
        })

    if request.method == "DELETE":
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
            data = request.POST['data']
            logger.info(data)
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
            data = request.POST['data']
            logger.info(data)
            vm_id = data['id']
            res = requests.get("https://api.starbucks.net/bean-api/api/v1/server/verde/" + str(vm_id), headers=headers,
                               verify=False)
            #todo : 拉取需要的信息（sn）
            return render_json({
                "data": res.json(),
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





