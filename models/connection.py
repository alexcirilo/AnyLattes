import mysql.connector

#railway access:
user='root'
pwd='MB4EAozSfFx5BWmetk67'
host='containers-us-west-54.railway.app'
database='railway'
port=6574
'''
'''



'''
local access
'''

'''
user = 'root'
pwd = 'Qwer@1234'
host = 'localhost'
database = 'lattes4web'
'''

'''
container access
user = 'root'
pwd = 'qwe123'
host = '172.17.0.2'
database = 'lattes4web'
'''

def conexao():
    try:
        db = mysql.connector.connect(user=user,password= pwd,host=host, database=database,port=port)
        # print("Connected!")
    except:
        print("YOU SHALL NOT PASS!")
    return db

