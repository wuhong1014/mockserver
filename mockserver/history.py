#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：wuhong time:2019/7/24
import datetime


def organize_history_info(rule_info,request_info,response_info) :
    """
    :param rule_info: (dict)
    :param request_info: (dict)
    :param response_info: (dict)
    :return: OrderedDict like {
        rule_mapping:{},
        request:{}
        response:{}
    }
    """

    h_info={}
    h_info["time"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    h_info["rule_mapping"]=rule_info
    h_info["request"]=request_info
    h_info["response"]=response_info
    return h_info
def organize_history_request(url,method,headers,body,):
    request_info={}
    request_info["url"]=url
    request_info["method"]=method
    request_info["headers"]=headers
    request_info["body"]=body
    request_info["request_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return request_info
def organize_history_response(status,headers,body):
    response_info = {}
    response_info["status"] = status
    response_info["headers"] = headers
    response_info["body"] = body
    response_info["response_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return response_info