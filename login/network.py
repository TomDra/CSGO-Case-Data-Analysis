import sqlite3
from argon2 import PasswordHasher
ph = PasswordHasher()
sqliteConnection = sqlite3.connect('logins.db')
cursor = sqliteConnection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logins (userID,username string,hashpass string);")
#cursor.execute(f'INSERT INTO logins VALUES (1,"test", "{ph.hash("teststring")}");')
print(cursor.execute("SELECT * FROM logins").fetchall())

class Account:
  def __init__(self,username):
    self.username = username
    try:
      if str(cursor.execute(f'SELECT username FROM logins WHERE username="{self.username}"').fetchall()[0]).split("'")[1] != None:
        self.account = True
        self.password_hash = str(cursor.execute(f'SELECT hashpass FROM logins WHERE username="{username}"').fetchall()[0]).split("'")[1]
    except IndexError:
      self.account = False

  def valid_account(self):
    return self.account

  def check_pass(self, given_pass):
    try:
      if ph.verify(self.password_hash, given_pass):
        return True
    except Exception:
      return [False,'Invalid Password']


def login(account_username, password):  
  user = Account(account_username)
  if user.valid_account():
    result = user.check_pass(password)
  else:
    result = [False,'Invalid Username']
  return result



print(login('test','teststring'))


sqliteConnection.commit()
sqliteConnection.close()