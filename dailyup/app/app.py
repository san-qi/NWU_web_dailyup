from flask import Flask, request
from flask_cors import CORS
from nwu_report.util import check, sql_exec
from json import loads
import hmac
app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/check', methods=["POST"])
def check_api():
    user_id = request.form["sid"]
    passwd = request.form["psw"]
    return check(user_id, passwd)


@app.route('/saveid', methods=["POST"])
def save_id_api():
    uid = request.form["sid"]
    passwd = request.form["psw"]

    def func(cursor):
        cursor.execute(f"select passwd from user where id='{uid}'")
        if cursor.fetchone():
            cursor.execute(
                f"update user set passwd='{passwd}' where id='{uid}'")
            return {'e': 0, 'm': '用户密码已更新'}
        else:
            cursor.execute(
                f"insert into user (id, passwd, active, inSchool) values ('{uid}', '{passwd}', 0, 0)")
            return {'e': 0, 'm': '用户信息已保存'}
    return sql_exec(func)


@app.route('/islogin', methods=["GET"])
def islogin_api():
    uid = request.cookies.get('id', None)
    logined = request.cookies.get('logined', None)
    if uid and logined:
        def get_pw(cursor):
            cursor.execute(f"select passwd from user where id='{uid}'")
            return cursor.fetchone()[0]
        pw = sql_exec(get_pw)
        if pw:
            pw = pw.encode()
        else:
            return {'e': 1, 'm': '操作失败'}
        uid = uid.encode()
        md_code = hmac.new(uid, pw, digestmod='MD5').hexdigest()
        if md_code == logined:
            return {'e': 0, 'm': '操作成功'}
        else:
            return {'e': 1, 'm': '操作失败'}
    else:
        return {'e': 1, 'm': '操作失败'}


@app.route('/userinfo', methods=["GET"])
def userinfo_api():
    uid = request.cookies.get('id', None)
    if uid:
        def select(cursor):
            cursor.execute(f"select * from user where id='{uid}'")
            return cursor.fetchone()
        res = sql_exec(select)
        if res[4]:
            return {'e': 0, 'm': '操作成功', 'd': {'id': uid, 'active': res[2], 'inschool': res[3], 'geoinfo': loads(res[4])['formattedAddress']}}
        else:
            return {'e': 0, 'm': '操作成功', 'd': {'id': uid, 'active': res[2], 'inschool': res[3], 'geoinfo': res[4]}}
    else:
        return {'e': 1, 'm': '操作失败'}


@app.route('/changest', methods=["POST"])
def changest_api():
    uid = request.cookies.get('id', None)
    field = request.form["field"]
    stat = request.form["stat"]
    if uid:
        def func(cursor):
            cursor.execute(f"update user set {field}={stat} where id='{uid}'")
        sql_exec(func)
        return {'e': 0, 'm': '操作成功'}
    else:
        return {'e': 1, 'm': '操作失败'}


@app.route('/savegeo', methods=["POST"])
def savegeo_api():
    uid = request.cookies.get('id', None)
    info = request.form["info"]
    if uid:
        def func(cursor):
            cursor.execute(
                f"update user set geoInfo='{info}' where id='{uid}'")
        sql_exec(func)
        return {'e': 0, 'm': '操作成功'}
    else:
        return {'e': 1, 'm': '操作失败'}


if __name__ == '__main__':
    app.run(port=8082, debug=True)
