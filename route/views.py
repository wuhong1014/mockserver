import time,json
import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import History
from mockserver import match
from mockserver.history import organize_history_request, organize_history_response
from mockserver.match import best_matched, ParserRequestRule

def forward_proxy(request,proxy):
    """
    :url:
    :return: Response
    """
    if  proxy.startswith("http://"):
        proxy_type ='http'
        proxy = proxy.split('http://')[-1]
    elif proxy.startswith("https://"):
        proxy_type='https'
        proxy = proxy.split('https://')[-1]
    else:
        proxy_type='http'
    url = ''.join((proxy_type,"://",proxy,request.path))
    method=request.method
    headers={}
    for k,v in request.META.items():
        headers[k] = str(v)
    params=request.query_params
    data=request.data
    cookies=request.COOKIES
    session=requests.Session()
    session.proxies = {proxy_type: proxy}
    response=session.request(method,url,headers=headers,data=data,params=params,cookies=cookies)
    return response
@api_view(['GET','POST','PUT','DELETE','PATCH'])
def route(request):
    method = request.method
    url = request.path
    meta = request.META
    headers={}
    for k, v in meta.items():
        if 'wsgi' not  in k :
            headers[k] = v

    params = request.query_params
    data = request.data
    #匹配
    req_info = {}
    req_info.update(url=url, method=method, headers=headers, params=params,data=data)
    matched = match.get_all_matched(req_info)
    if matched:
        best = best_matched(matched)
        pr = ParserRequestRule(best)
        proxy = pr.proxy
        rule_info = best
        if not proxy:
            status=200
            resp_headers=pr.response_headers
            resp_data=pr.response_data
            if not resp_data:
                return empty_response()
            request_info = organize_history_request(url, method, headers, {"params": params, "data": data})
            response_info = organize_history_response(status, resp_headers, resp_data)
            his_id=''.join(('HIS',time.strftime('%Y%m%d%H%M%S',time.localtime())))
            History.objects.create(id=his_id,rule=json.dumps(rule_info,ensure_ascii=False), request_body=json.dumps(request_info,ensure_ascii=False), response_body=json.dumps(response_info,ensure_ascii=False))
            return Response(data=resp_data, headers=resp_headers, status=status)
        else:
            resp=forward_proxy(request,proxy)
            return HttpResponse(resp)
    else:
        """不匹配"""
        return url_not_matched()

def empty_response():
    result = {
        "status": 404,
        "msg": "the request rule config has not response or response is None"
    }
    return Response(result)

def url_not_matched():
    result = {
        "status": 404,
        "msg": "the request not matched,please check!"
    }
    return Response(result)

