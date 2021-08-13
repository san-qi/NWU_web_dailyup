from .aes_crypt import MyAes
from bs4 import BeautifulSoup
from time import time, sleep
import pymysql
import re
import requests


headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def sql_exec(func, host='mysqldb', user='root', password='qwertyuiop', database='test', port=3306):
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database, port=port)
    cursor = db.cursor()
    res = None
    try:
        res = func(cursor)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    db.close()
    return res


def get_session(name, passwd):
    """
    获取认证后的session对象,不保证该对象的认证成功与否,但调用者需要自己手动关闭这个session对象
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/80.0.3987.149 Safari/537.36',
    }
    s = requests.Session()
    s.cookies.set(
        'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE', 'zh_CN')
    s.headers = headers
    index_url = 'http://authserver.nwu.edu.cn/authserver/login?service=https%3A%2F%2Fapp.nwu.edu.cn%2Fa_nwu%2Fapi%2Fsso%2Fcas%3Fredirect%3Dhttps%253A%252F%252Fapp.nwu.edu.cn%252Fsite%252Fncov%252Fdailyup%26from%3Dwap'
    index_page = s.get(index_url)
    data = {'username': name,
            'password': passwd,
            }

    # 提交认证信息
    soup = BeautifulSoup(index_page.text, 'html.parser')
    for tag in soup.select('#casLoginForm > input[type=hidden]'):
        data[tag['name']] = tag['value']
    result = re.search(r'var pwdDefaultEncryptSalt = "(\S*)"', index_page.text)
    key = result.group(1)
    aes = MyAes(key)
    data['password'] = aes.encrypt(data['password'])
    s.post(index_url, data=data, headers=headers)
    return s


def check(name, passwd):
    """
    状态码e为0时表示通过,为10013时表示身份验证未通过,为10037时表示需要填写验证码
    """
    s = get_session(name, passwd)
    # 确认是否需要验证码
    cap_url = f'http://authserver.nwu.edu.cn/authserver/needCaptcha.html?username={name}&pwdEncrypt2=pwdEncryptSalt&_={int(time()*1000)}'
    cap_page = s.get(cap_url)
    if(cap_page.text == 'true'):
        return {'e': 10037, 'm': '需要填写验证码', 'd': {}}

    # 获取个人信息用于展示及其它
    info_url = 'https://app.nwu.edu.cn/ncov/wap/open-report/index'
    page = s.get(info_url, headers=headers)
    s.close()
    res = page.json()
    if not res['e']:
        res['d'] = {
            'realname': res['d']['userinfo']['realname'],
            'sex': res['d']['userinfo']['sex']
        }
    return res


def convert_geo_data(in_school, data):
    """
    将前端给出的高德地图api转换成实际的填报数据,推荐不要直接使用,或者自行构建对应的转换规则
    in_school表示是否在校的选项, data表示高德位置信息
    """
    addr = data["addressComponent"]
    addr_list = []
    addr_list.append(addr["province"])
    addr_list.append(addr["city"])
    addr_list.append(addr["district"])
    converted_data = {
        "address": data["formattedAddress"],
        "area": " ".join(addr_list),
        "city": addr_list[1],
        "geo_api_info": data,
        "province": addr_list[0],
        "qtqk": "",
        "sfcyglq": 0,
        "sfyzz": 0,
        "sfzx": 0,
        "tw": 1,
        "ymtys": ""

    }
    if in_school:
        converted_data["sfzx"] = 1
    # print(converted_data)
    return converted_data


def report(name, passwd, in_school, geo_api_info, __DEBUG=False):
    """
    用于填报用户数据
    """
    if not __DEBUG:
        sleep(4)
    report_data = convert_geo_data(in_school, geo_api_info)
    s = get_session(name, passwd)
    r = s.post('https://app.nwu.edu.cn/ncov/wap/open-report/save',
               headers=headers, json=report_data)
    s.close()
    return r
