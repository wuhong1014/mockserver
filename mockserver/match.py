#encoding:utf-8
import datetime
import re
import time
from collections import OrderedDict
from mockserver.log import logger
from mockserver.loader import load_rules
from mockserver.util import is_dict

logger = logger()
class ParserRequestRule(object):
    """
    rule :json file content or part json file content ,format dict
    """

    def __init__(self, rule):
        self.rule = rule
        self.request_body = self.__get_request_body()
        self.response_body = self.__get_response_body()
    @property
    def get_name(self):
        return self.rule.get("name")

    @property
    def get_uid(self):
        return self.rule.get("uid")

    @property
    def get_desc(self):
        return self.rule.get("desc")

    def __get_request_body(self):
        return {} if 'request_body' not in self.rule or not self.rule.get('request_body') else self.rule.get("request_body")

    @property
    def request_url(self):
        return self.request_body.get("url")

    @property
    def request_method(self):
        return self.request_body.get('method')

    @property
    def request_params(self):
        return self.request_body.get('params')

    @property
    def request_data(self):
        return self.request_body.get('data')

    @property
    def request_headers(self):
        return self.request_body.get("headers")

    @property
    def request_cookies(self):
        return self.request_body.get("cookies")
    def __get_response_body(self):
        return {} if 'response_body' not in self.rule or not self.rule.get("response_body") else self.rule.get("response_body")

    @property
    def response_headers(self):
        return self.response_body.get('headers')
    @property
    def response_cookies(self):
        return self.response_body.get("cookies")
    @property
    def response_data(self):
        return  self.response_body.get("response")

    @property
    def priority(self):
        """默认优先级：999"""
        return self.rule.get("priority",999)

    @property
    def proxy(self):
        proxy=self.rule.get("proxy")
        return proxy
def match_str(pattern,string):

    try:
        mat = re.search(pattern, string).group()
        if mat == string:
            return True
        else:
            return False
    except AttributeError:
        return False
    except Exception as e:
        logger.error("match未知异常: \n [{}]".format(str(e)))
        return False
def match_url(request_url,url_re):
    if url_re:
        pattern = re.compile(r'http[s]?://.*({})'.format(url_re), flags=re.M | re.I)
        return match_str(pattern,request_url)
    else:return True
def match_method(request_method,method_re):
    if not method_re or method_re.lower()=="any" :
        return True
    elif method_re.lower() == request_method.lower():
        return True
    else:
        return False

def match_headers(request_headers,headers_re):
    """headers_re only support format as {Content-Type:xxx,user-agent:xxx}"""
    if  not headers_re:
        return True
    elif is_dict(request_headers):
        for k,v in headers_re.items():
            res_header=request_headers.get(k)
            if not res_header or res_header!=v or not  match_str(res_header,v):
                return False
        return True
    else:
        return False
def parse_dot_content(body,content):
    """
    :param body:
    :param content: like "content.request.url"
    :return:
    """
    content_list=content.split(".")
    for ctl in content_list:
        try:
            body=body.get(ctl.strip())
        except Exception as e:
            msg="parse error,content : {0} ,error :{1}".format(content,str(e))
            logger.error(msg)
            return False
    return body

def match_request(request_body,request_re):
    """request_body could be str or dict(json)
        request_re must be list
       if str  :request_re  support method  [contains] ,format like : [{contains:xxx},{contains:ccc}]
       if dict :request_re   support method . format like[{"content.detail.name" : "jone"}，{} ],"content." must be support
    """
    if not request_re :
        return True
    elif isinstance(request_body,(str,dict)):
        for req in request_re:#request_re type list,like [{},{}]
            key,value=req.popitem()
            if isinstance(request_body,str) and "contains" ==key:
                pattern = re.compile(r'.*(value).*', re.DOTALL | re.I)
                if  not match_str(pattern, request_body):
                    return False
            elif is_dict(request_body) and key.startswith("content."):
                new_key = ".".join(key.split(".")[1:])
                request_value=parse_dot_content(request_body,new_key)
                if request_value != value:
                    return False
            else:
                msg = 'content format error ,str only support like  {"contains":"xxx"} or dict(json)only support like {"content.detail.name" : "jone"}'
                logger.warning(msg)
                return False
        return True
    else:
        msg="request_body should be dict(json) or str format!"
        logger.error(msg)
        return False
def get_all_matched(req_info):
    rules = load_rules()
    matched_info=[]
    for rule in rules:
        conf_info = ParserRequestRule(rule)
        conf_url = conf_info.request_url
        conf_method = conf_info.request_method
        conf_headers = conf_info.request_headers
        conf_params = conf_info.request_params
        conf_data = conf_info.request_data
        req_url=req_info.get("url")
        req_method=req_info.get("method")
        req_headers=req_info.get("headers")
        req_params=req_info.get("params")
        req_data = req_info.get("data")

        if not match_url(req_url, conf_url):
            continue
        elif not match_method(req_method, conf_method):
            continue
        elif not match_headers(req_headers, conf_headers):
            continue
        elif not match_request(req_params, conf_params):
            continue
        elif not match_request(req_data, conf_data):
            continue
        else:
            matched_info.append(rule)
    return matched_info
def best_matched(match_list):
    """
    根据设置的mock请求中的priority得到最优匹配，priority越小优先级越高，如果 priority 存在多个最优，获取一个
    :param match_list:
    :return:(dict) configured request info
    """
    content={}
    for each_match in match_list:
        l_request=ParserRequestRule(each_match)
        priority=l_request.priority
        content.update({priority:each_match})
    b_priority= min(content.keys())
    return content.get(b_priority)


