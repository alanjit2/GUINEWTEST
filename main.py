import sqlite3
from tkinter import *
import base64
from tkinter import messagebox

# from cryptography.fernet import Fernet
# # key = Fernet.generate_key() #this is your emcryption key
# key = b'tET6ttrvB_QNhCInCgCI9p7-jbs25MR15QnFq4E2WNI='

# Create/Connect Database
def welcome_scr():
    pass

def connect_table(mycursor):
    mycursor.execute("""CREATE TABLE IF NOT EXISTS users(
      userid INTEGER PRIMARY KEY, 
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      username TEXT UNIQUE,
      password_unhashed TEXT NOT NULL,
      password INTEGER NOT NULL
      )
  """)
    return


def create_user(f_name, l_name, username, password):
    try:
        password_hash = encrypt(password)
        insert_stmt = """INSERT INTO users 
      (first_name, last_name, username, password_unhashed, password) 
      VALUES ('{}', '{}', '{}', '{}', '{}')""".format(f_name, l_name, username, password, password_hash)
        mycursor.execute(insert_stmt)

        mydb.commit()

        """
        Testing
        """
        mycursor.execute(
            """SELECT [first_name], [last_name], [username] as name ,[password_unhashed] ,[password] 
            FROM users order by username"""
        )
        while 1:
            row = mycursor.fetchone()
            if not row:
                break
            print(row)
        messagebox.showinfo("showinfo", "Login Successfully made")
    except:
        messagebox.showerror("showerror", "Username is already in Use")


def check_login(username_input, password_input):
    valid_login = 0
    returned_fname = None
    returned_lname = None
    password_input_hashed = encrypt(password_input)
    sql_statement = '''SELECT first_name, last_name FROM users
    WHERE username = '{}' AND password = '{}'
    '''.format(username_input, password_input_hashed)

    print(sql_statement)
    mycursor.execute(sql_statement)
    while 1:
        row = mycursor.fetchone()
        if not row:
            break
        # print(row)
        valid_login = len(row)
        returned_fname = row[0]
        returned_lname = row[1]
        print(row[0])
        print(row[1])
        # if row[0] == 1:
        #     valid_login = 1
        if len(row) == 0:
            messagebox.showinfo("showinfo", "Username or Password Incorrect")
            return
        else:
            message = f'Login Successful. Welcome {returned_fname} {returned_lname}'
            messagebox.showinfo("showinfo", message)
            welcome_scr()
    return valid_login, returned_fname, returned_lname

def encrypt(password):
    password_bytes = password.encode("ascii")

    base64_bytes = base64.b64encode(password_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def decrypt(password_enc):
    password_enc = password_enc.encode("ascii")

    sample_string_bytes = base64.b64decode(password_enc)
    password_normal = sample_string_bytes.decode("ascii")

    return password_normal


def signin_screen():

    # create window
    root = Tk()
    root.geometry("400x200")

    # Add Title
    root.title("Sign Into GUI")

    # Define Entry Widget variables
    e1 = StringVar()
    e2 = StringVar()

    # Add Label Widgets
    user = Label(root, text="Username:  ")
    user.grid(row=0, column=0)

    password = Label(root, text="Password: ")
    password.grid(row=1, column=0)

    # Add Entry widgets
    user_entry = Entry(root, textvariable=e1)
    user_entry.grid(row=0, column=1)

    password_entry = Entry(root, textvariable=e2)
    password_entry.grid(row=1, column=1)

    # Add Button Widgets
    signin_button = Button(root, text="Login", command=lambda: check_login(user_entry.get(), password_entry.get()))
    signin_button.grid(row=4, column=0)
    signup_button = Button(root, text="Create Login", command=lambda: signup_screen())
    signup_button.grid(row=4, column=1)
    quit_button = Button(root, text="Quit", command=root.destroy)
    quit_button.grid(row=4, column=2)

    root.mainloop()


def signup_screen():
    # create window
    root = Tk()
    root.geometry("400x200")

    # Add Title
    root.title("Make a login")

    # Define Entry Widget variables
    e1 = StringVar()
    e2 = StringVar()
    e3 = StringVar()
    e4 = StringVar()

    # Add Label Widgets
    first_name = Label(root, text="First Name: ")
    first_name.grid(row=0, column=0)

    last_name = Label(root, text="Last Name: ")
    last_name.grid(row=1, column=0)

    user = Label(root, text="Username:  ")
    user.grid(row=2, column=0)

    password = Label(root, text="Password: ")
    password.grid(row=3, column=0)

    # Add Entry widgets
    first_name_entry = Entry(root, textvariable=e1)
    first_name_entry.grid(row=0, column=1)

    last_name_entry = Entry(root, textvariable=e2)
    last_name_entry.grid(row=1, column=1)

    user_entry = Entry(root, textvariable=e3)
    user_entry.grid(row=2, column=1)

    password_entry = Entry(root, textvariable=e4)
    password_entry.grid(row=3, column=1)

    # Add Button Widgets
    signin_button = Button(root, text="Sign Up",
                           command=lambda: create_user(first_name_entry.get(),
                                                       last_name_entry.get(),
                                                       user_entry.get(),
                                                       password_entry.get()))
    signin_button.grid(row=4, column=0)


    root.mainloop()


mydb = sqlite3.connect('mydatabase.db')

mycursor = mydb.cursor()

connect_table(mycursor)
signin_screen()

# Encode/Decode Function

# def encrypt(password):
#   password_bytes = password.encode("ascii")

#   base64_bytes = base64.b64encode(password_bytes)
#   base64_string = base64_bytes.decode("ascii")

#   return base64_string
# def decrypt(password_enc):
#   password_enc = password_enc.encode("ascii")

#   sample_string_bytes = base64.b64decode(password_enc)
#   password_normal = sample_string_bytes.decode("ascii")

#   return password_normal


# Function to add input from user into Table
# def create_user(f_name,l_name,username,password):
#   password_hash=encrypt(password)
#   insert_stmt = """INSERT INTO users
#   (first_name, last_name, username, password, password_hashed)
#   VALUES ('{}', '{}', '{}', '{}', '{}')""".format(f_name, l_name, username, password, password_hash)
#   mycursor.execute(insert_stmt)
#   return


# Add Data

# f_name = "John"
# l_name = "Smith"
# username = "johnsmith"
# password = "12345678"
# create_user(f_name,l_name,username,password)

# password_hash=hash(password)
# txt1 = "My name is {}, I'm {}".format(f_name, username)
# print(txt1)
# # mycursor.execute("""INSERT INTO users
# # (first_name, last_name, username, password, password_hashed)
# # VALUES ('John', 'Smith', 'js@gmail.com', '1234', '1234')""")
# insert_stmt = """INSERT INTO users
# (first_name, last_name, username, password, password_hashed)
# VALUES ('{}', '{}', '{}', '{}', '{}')""".format(f_name, l_name, username, password, password_hash)
# mycursor.execute(insert_stmt)


# Query Data

# mycursor.execute(
#     "SELECT [first_name], [last_name], [username] as name ,[password_unhashed] ,[password] FROM users order by username")
# while 1:
#     row = mycursor.fetchone()
#     if not row:
#         break
#     print(row)
mydb.close()