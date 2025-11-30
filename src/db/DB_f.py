import psycopg2
import config.config as c

def init_user_ticket_details_flight(id:int,flight:str):
    conn = psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE ,port=c.PORT)
    cur = conn.cursor()
    cur.execute("UPDATE user_ticket_details SET flight = %s WHERE id=%s", (flight,id))
    conn.commit()
    cur.close()
    conn.close()