__author__ = 'luke'

import psycopg2
def insert_private_subnet():
    psyconn = psycopg2.connect(database="cmdbuild", host="10.200.200.233", user="postgres", password="000000")
    cur = psyconn.cursor()
    subnet='10.201.40.'
    location='铜牛天坛机房'
    for i in range(1,255):
        ip=subnet+str(i)
        sql ='''insert into ip("Ipaddress","Isused","Location","Isprivate","Isreserved") VALUES ('%s','f','%s','t','f')'''%(ip,location)
        cur.execute(sql)
    #rows = cur.fetchall()  # all rows in table
    psyconn.commit()
    #return rows;
    cur.close()
    psyconn.close()

def update_ip_used(iplist):
    psyconn = psycopg2.connect(database="cmdbuild", host="10.200.200.233", user="postgres", password="000000")
    cur = psyconn.cursor()
    for ip in iplist:
        sql =''' update ip set "Isused"='t' where "Ipaddress"='%s' '''%(ip)
        cur.execute(sql)
    #rows = cur.fetchall()  # all rows in table
    psyconn.commit()
    #return rows;
    cur.close()
    psyconn.close()

#insert_private_subnet()
def get_all_ip():
    psyconn = psycopg2.connect(database="cmdbuild", host="10.200.200.201", user="postgres", password="abcd123!")
    cur = psyconn.cursor()
    sql =''' update ip set "Isused"='t' where "Ipaddress"='%s' '''%(ip)
    cur.execute(sql)
    #rows = cur.fetchall()  # all rows in table
    psyconn.commit()
    #return rows;
    cur.close()
    psyconn.close()

if __name__ == '__main__':
    iplist=[]
    update_ip_used(iplist)