from nwu_report.util import check, sql_exec, report
from json import loads

def solve(uid):
    def func(cursor):
        cursor.execute(f"select passwd, inSchool, geoInfo from user where id='{uid}'")
        return cursor.fetchone()
    passwd, inschool, geoinfo = sql_exec(func)
    geoinfo = loads(geoinfo)
    res = report(uid, passwd, inschool, geoinfo)
    print(uid, ": ", res)

def main():
    def func(cursor):
        cursor.execute("select id from user where active=1")
        return cursor.fetchall()
    for d in sql_exec(func):
        try:
            solve(d[0])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
