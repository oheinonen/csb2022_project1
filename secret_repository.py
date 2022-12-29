from db import db
from flask import session

def add_secret(secret):
    # TO FIX FLAW 4 comment next line
    db.session.execute("INSERT INTO secrets (secret) VALUES ('" + secret + "');")
    # TO FIX FLAW 4 uncomment next lines
    # db.session.execute("INSERT INTO secrets (secret) VALUES (:secret);")
    #db.session.execute(sql, {"secret":secret})
    db.session.commit()
    return True

def remove_secret(id):
    try:
        sql = "DELETE from secrets WHERE id=:id;"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True
