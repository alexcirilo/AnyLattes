from MySQLdb import Error
import mysql.connector


'''
heroku access
'''
'''
user= 'b96e08051c345f'
pwd= '2503c6ba'
host= 'us-cdbr-east-06.cleardb.net'
database= 'heroku_34fb507d853ce4f'
'''
'''
local access
'''
user = 'root'
pwd = 'Qwer@1234'
host = 'localhost'
database = 'lattes4web'

def conexao():
    try:
        db = mysql.connector.connect(user=user,password= pwd,host=host, database=database)
    except:
        print("YOU SHALL NOT PASS!")
    return db

