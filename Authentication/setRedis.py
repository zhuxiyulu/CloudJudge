from django.core.cache import cache
import json

# 设置有效时间
CAPTCHA_VALID_TIME = 5*60

# read cache captcha
def read_from_cache(email):
    key = email
    value = cache.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data

# write cache captcha
def write_to_cache(email, captcha):
    key = email
    cache.set(key, json.dumps(captcha), CAPTCHA_VALID_TIME)
