import psycopg2
import config.config as c

def insert_user(user_name:str,password:str,tg_id:int):
    conn = psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE ,port=c.PORT)
    cur = conn.cursor()
    cur.execute("INSERT into users (username,password_user,id_tg) values(%s,%s,%s);", (user_name,password,tg_id))
    conn.commit()
    cur.close()
    conn.close()

def user_info(id_tg:int):
    conn = psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE ,port=c.PORT)
    cur = conn.cursor()
    cur.execute("Select username,password_user from users where id_tg=%s and payment is TRUE",(id_tg,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows[0]


# print(user_info(945376146)[0])