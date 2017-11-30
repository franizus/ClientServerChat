import socket
import sys
import pymysql


def send(dbcon, connection, address, line, i):
    connection.send(line.encode('ascii'))
    add = addr[0] + ':' + str(addr[1])
    insertToDB(dbcon, "server_code.txt", add, i)

def connectToDB():
    try:
        con = pymysql.connect(host="localhost", user="root", passwd="uizmxrhxl", db="server_log_py")
        print("Database was connected successfully")
    except:
        print("Database error")
    return con

def insertToDB(con, filename, address, linea):
    cursor = con.cursor()
    sql = ("insert into log(filename, address, linea) VALUES ('%s', '%s', '%d')" % (filename, address, linea))
    cursor.execute(sql)
    con.commit()

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port
CONDB = connectToDB()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print('Socket now listening')

connectToDB()

(conn, addr) = s.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))

file = open("server_code.txt", "r")
i = 0

for line in file:
    send(CONDB, conn, addr, line, i)
    i += 1
else:
    conn.send("file finished".encode('ascii'))

file.close()
s.close()
