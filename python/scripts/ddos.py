from subprocess import Popen,PIPE
import re
import time
import sqlite3

CONCURRENCY_ALLOWED = 30
OUTDATE_TIME = 86400

# initializing database
db = sqlite3.connect("/tmp/ddos.db3")
c = db.cursor()
#
try:
    c.execute("CREATE TABLE ddos (ip text unique,date integer);")
except:
    print "database exists"

# blocking ips has more than CONCURRENCY_ALLOWED connections
pipe = Popen("netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n > /tmp/ddos.txt", shell=True,bufsize=1024,stdout=PIPE).stdout
ddos = pipe.read()
ddos = open("/tmp/ddos.txt").read()
ct = re.compile(r"(\S+)\s+(\S+).*\n").findall(ddos)

for count,ip in ct:
    if int(count)>CONCURRENCY_ALLOWED and (ip != "127.0.0.1") and (not ip.startswith("192.168")):
        out = Popen("iptables -I INPUT -s %s -j DROP"%ip,shell=True,bufsize=1024,stdout=PIPE).stdout
        print "blocking %s for %s visits" % (ip,count)
        #c.execute('REPLACE INTO ddos VALUES (?,?)',(ip,int(time.time())))
        time.sleep(0.1)

db.commit()

# unblocking outdated blockings
c.execute("SELECT * FROM ddos")
ddos = c.fetchall()

for ip,date in ddos:
    if date + OUTDATE_TIME < time.time():
        c.execute("DELETE FROM ddos WHERE ip=?",(ip,))
        print "unblocking %s" % ip
        out = Popen("iptables -D INPUT -s %s -j DROP"%ip,shell=True,
                     bufsize=1024,stdout=PIPE).stdout
        time.sleep(0.1)

db.commit()
