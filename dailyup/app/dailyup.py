from nwu_report.util import check, sql_exec, report
from json import loads

def solve(uid):
    def func(cursor):
        cursor.execute(f"select passwd, inSchool, geoInfo from user where id='{uid}'")
        return cursor.fetchone()
    passwd, inschool, geoinfo = sql_exec(func)
    geoinfo = loads(geoinfo)
    res = report(uid, passwd, inschool, geoinfo)
    print(uid, ": ", res.text)
    return res

def is_success(res):
    code = res.json()["e"]
    return code!=10013

def main():
    def func(cursor):
        cursor.execute("select id from user where active=1")
        return cursor.fetchall()
    fail_user = []
    for d in sql_exec(func):
        try:
            res = solve(d[0])
            if not is_success(res):
                fail_user.append(d[0])
        except Exception as e:
            print(e)
    while fail_user:
        try:
            uid = fail_user[0]
            fail_user = fail_user[1:]
            res = solve(uid)
            if not is_success(res):
                fail_user.append(uid)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
