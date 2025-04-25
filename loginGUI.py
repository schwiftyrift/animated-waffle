import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from PIL import ImageTk, Image
import json
from UserData import *
import subprocess
import sys
import os

def save_credentials(username, password, remember_me):
    if remember_me:
        data = {
            "username": username,
            "password": password,
            "remember_me": True
        }
        with open("credentials.json", "w") as f:
            json.dump(data, f)
    else:
        if os.path.exists("credentials.json"):
            os.remove("credentials.json")  # Remove the file if "Remember Me" is unchecked
        # Clear the entries
        email_input.delete(0, tk.END)
        password_input.delete(0, tk.END)
        checkValue.set(0)  # Uncheck the checkbox

def load_credentials():
    try:
        with open("credentials.json", "r") as f:
            data = json.load(f)
            if data.get("remember_me"):
                return data["username"], data["password"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return "", ""  # Return empty if not remembered

def openGUI(username):
    subprocess.Popen(["python", "userGUI.py", username])
    sys.exit()

def handle_login(event=None):
    email = email_input.get()   # storing the email given from user
    password = password_input.get()  # storing the password given from user

    if not email or not password:
        messagebox.showerror("Error", "Both email and password are required")
        return
    
    if not email.endswith("@latech.edu"):
        messagebox.showerror("Error", "Your email must be a @latech.edu address")
        return
    
    try: 
        with open("user_data.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    successLogin = login(email, password)
    if not successLogin:
        messagebox.showerror("Error", "Invalid email or password")
    else:
        messagebox.showinfo("", f"Login Successful! Welcome {users[email]['name']}!")
        save_credentials(email, password, checkValue.get())  # Save with checkbox value
        openGUI(email)

# creating account button and new window GUI
def openCreateAccountWindow():
    createWindow = tk.Toplevel(root)
    createWindow.title("Create an Account")
    createWindow.geometry("350x500")
    createWindow.configure(background = '#0096DC')
    
    # StudentId (CWID)
    cwidLabel = Label(createWindow, text='Enter CWID', fg = 'white', bg = '#0096DC', font=('helvetica', 14))
    cwidLabel.pack(pady=(20,5))
    cwidInput = Entry(createWindow, width = 50)
    cwidInput.pack(ipady = 6, pady = (1,10))
    
    # For Name
    nameLabel = Label(createWindow, text = "Enter Your Full Name", fg = 'white', bg = '#0096DC', font = ('helvetica', 14))
    nameLabel.pack(pady = (10,5))
    nameInput = Entry(createWindow, width = 50)
    nameInput.pack(ipady = 6, pady = (1,10))

    # for Email
    emailLabel = Label(createWindow, text='Enter Your Email Address (@latech.edu)', fg = 'white', bg = '#0096DC', font=('helvetica', 14))
    emailLabel.pack(pady=(10,5))
    emailInputNew = Entry(createWindow, width = 50)
    emailInputNew.pack(ipady = 6, pady = (1,10))

    # for passkey
    passKeyLabel = Label(createWindow, text='Enter Pass Key', fg='white', bg='#0096DC', font=('helvetica', 14))
    passKeyLabel.pack(pady=(10, 5))
    passKeyInputNew = Entry(createWindow, width=50)
    passKeyInputNew.pack(ipady=6, pady=(1, 10))

    # save button
    def saveAccount():
        cwid = cwidInput.get()
        name = nameInput.get()
        email = emailInputNew.get()
        passKey = passKeyInputNew.get()

        if not (cwid and name and email and passKey):
            messagebox.showerror("Error", "All fields are mandatory")
            return
        if not email.endswith("@latech.edu"):
            messagebox.showerror("Error", "Your email must be a @latech.edu address")
            return

        else:
            success = register_user(email, passKey, cwid, name)
            if (success == False):
                messagebox.showerror("Error", "The account already exists with this email")
            
            messagebox.showinfo("Create user", "Account created successfully")
            createWindow.destroy()

    createBtn = Button(createWindow, text = "Create Account", bg = 'white', fg = 'black', width = 20, height = 2, command = saveAccount)
    createBtn.pack(pady=10)

# creating main window
root = tk.Tk()
root.title("Login Page")
root.bind('<Escape>', lambda e: root.quit())

# loading the icon image (in .png file)
icon = tk.PhotoImage(file = "icon1.png")

# setting the window icon
root.iconphoto(False, icon)

#root.minsize(100, 100)
#root.maxsize(400,400)

# fixing the size of the screen (seems not working)
root.attributes("-fullscreen", True)

# setting the background color with the code
root.configure(background = '#0096DC')

img = Image.open('icon1.png')

# setting the size of the image
resized_img = img.resize((160, 70))

#opening and bringing logo to the screen
img = ImageTk.PhotoImage(resized_img)

img_label = Label(root, image = img)
img_label.pack(pady=(10, 10))

text_label = Label(root, text = 'Automated Lost & Found', fg = 'white', bg = '#0096DC')
text_label.pack()
text_label.config(font=('helvetica', 12))


email_label = Label(root, text='Enter Email', fg='white', bg='#0096DC')
#setting the position
email_label.pack(pady=(20,5))
email_label.config(font=('helvetica', 10))

storedUser, storedPass = load_credentials()

# entry so that user can type their email
email_input = Entry(root, width = 50, font=('helvetica', 14))    # needed to import Entry class, Label class individually, I don't why this all get install while importing the tkinter
email_input.insert(0, storedUser)
# in order to manage y axis (height), we should use ipady
email_input.pack(ipady = 6, pady = (1,15))

### creating the password label

password_label = Label(root, text='Enter Password', fg='white', bg='#0096DC')
#setting the position
password_label.pack(pady=(20,5))
password_label.config(font=('helvetica', 10))

# entry so that user can type their password
password_input = Entry(root, width=50, show="*", font=('helvetica', 14))    # needed to import Entry class, Label class individually, I don't why this all get install while importing the tkinter
# in order to manage y axis (height), we should use ipady
password_input.insert(0, storedPass)
password_input.pack(ipady = 6, pady = (1,15))
password_input.bind("<Return>", handle_login)

checkValue = tk.IntVar()
rememberLogin = tk.Checkbutton(root, text = "Remember Me", variable = checkValue)
rememberLogin.pack()

if storedUser and storedPass:
    checkValue.set(1)  # If there are stored credentials, check the box

### using BUTTON CLASS to add LOGIN button
login_btn = Button(root, text = 'Login', bg = 'white', fg = 'black', width = 20,height=2, command = handle_login)  # command is callilng the function handle_login
login_btn.pack(pady=(10,20))

#adding more buttons
createAccountBtn = Button(root, text = "Create an Account", bg = 'white', fg = 'black', width = 20, height = 2, command=openCreateAccountWindow)
createAccountBtn.pack(pady = (0,20))
createAccountBtn.config(font=('helvetica', 10))


# designing the font
login_btn.config(font=('helvetica', 10))


# let's run the application
root.mainloop()


