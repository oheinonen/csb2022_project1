from db import db
from flask import session
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash

def register(username,password, name):
    # TO FIX FLAW 2 uncomment this:
    # hash_value = generate_password_hash(password)

    # and comment this
    hash_value = hashlib.md5(password.encode()).hexdigest()
    try:
        sql = "INSERT INTO users (username,password, backup) VALUES (:username,:password, :backup)"
        db.session.execute(sql, {"username":username,"password":hash_value, "backup": name})
        db.session.commit()
    except:
        return False
    return login(username,password)

def delete_user(user_id):
    # TO FIX FLAW 3 uncomment these:
    # id = session["user_id"]
    # if id == user_id:

    # TO FIX FLAW 3 comment next line:
    if user_id == user_id:
        sql = "DELETE FROM users WHERE id=:user_id"
        db.session.execute(sql, {"user_id": user_id})
        db.session.commit()
        return True
    else:
        return False


def login(username,password):
    sql = "SELECT password, id  FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    # TO FIX FLAW 2 comment next line
    hash_value = hashlib.md5(password.encode()).hexdigest()
    if user == None:
        return False
    else:
        # TO FIX FLAW 2 comment next line
        if user.password == hash_value:
            # TO FIX FLAW 2 uncomment this
            # if check_password_hash(user.password, password):
            session["user_id"] = user[1]
            session["username"] = username
            return True
        else:
            return False

# TO FIX FLAW 5 do not use this function for password recovery. Instead, eg. have MFA  
def login_without_pass(username,password,name):
    sql = "SELECT backup, id  FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if user.backup == name:
            # TO FIX FLAW 2 uncomment this
            # hash_value = generate_password_hash(password)
            # TO FIX FLAW 2 comment next line
            hash_value = hashlib.md5(password.encode()).hexdigest()
            sql = "UPDATE users SET password=:password WHERE id=:id"
            result = db.session.execute(sql, {"password":hash_value, "id":user.id})
            db.session.commit()
            session["user_id"] = user[1]
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id",0)
