#encoding:utf-8
from api.models import RuleInfo
from mockserver.util import string_convert, is_dict

def load_rules():
    rules = RuleInfo.objects.all().values_list('uid','name','desc','request_body','response_body','proxy','priority')
    format_rules=[]
    if rules:
        for rule in rules:
            rule = list(rule)
            rule[2] = rule[2] if  rule[2] else ''
            rule[3] = is_dict(string_convert(rule[3]))
            rule[4] = is_dict(string_convert(rule[4]))
            rule[5] = rule[5] if  rule[5] else ''
            rule[6] = string_convert(rule[6])
            keys = ['uid','name','desc','request_body','response_body','proxy','priority']
            single=dict(zip(keys,rule))
            format_rules.append(single)
    return format_rules
