#encoding:utf-8
import ast
import json
import os
import re
from mockserver import log
logger=log.logger()


def string_convert(str_value):
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "0000" => "0000"
         "$var" => "$var"
         '{"name":"jone"}'=>{"name":"jone"}
         '["jone",1233]'=>["jone",1233]
    """
    try:
        res = ast.literal_eval(str_value)
        if str_value.startswith('0') and isinstance(res,int):
            res = str_value
        return res
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def is_dict(content):
    if  not isinstance(content,dict):
        logger.warning("content not be dict ,content : {}".format(content))
        return False
    else:return content

if __name__=='__main__':
    pass