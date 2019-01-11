#encoding=utf8

# from sklearn.linear_model import LinearRegression
# reg = LinearRegression()
# reg.fit ([[0, 0], [1, 1], [3, 2]], [0, 1, 2])
# LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
# print(reg.coef_)

import urllib
import hashlib
import requests
def gen_url(location_info):
    queryStr = '/geocoder/v2/?address='+location_info+'+&output=json&ak=A7mGEhDp4ROX7IfBEzIqlAYyQ9GdA5V9'
    encodedStr = urllib.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + 'kpYga9mv29Ve1rGxrrnIVhNLIDlH7CRE'
    hashed = hashlib.md5(urllib.quote_plus(rawStr)).hexdigest()
    return 'http://api.map.baidu.com'+encodedStr+'&sn='+hashed

resp = requests.get(gen_url("Mountain View, CA"))


print(resp.text)
