import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from PIL import ImageTk, Image
import json

def handle_login():
    email = email_input.get()   # storing the email given from user
    password = password_input.get()  # storing the password given from user

    if not email or not password:
        messagebox.showerror("Error", "Both email and password are required")
        return
    
    if not email.endswith("@latech.edu"):
        messagebox.showerror("Error", "Your email must be a @latech.edu address")
        return
    
    try: 
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if email in users and users[email]["passKey"] == password:
        messagebox.showinfo("Yayyy", f"Login Successfull! Welcome {users[email]['name']}!")
    else:
        messagebox.showerror("Error", "Invalid email or password")


# creating account button and new window GUI
def openCreateAccountWindow():
    createWindow = tk.Toplevel(root)
    createWindow.title("Create an Account")
    createWindow.geometry("350x500")
    createWindow.configure(background = '#0096DC')
    
    # StudentId (CWID)
    cwidLabel = Label(createWindow, text='Enter CWID', fg = 'white', bg = '#0096DC', font=('helvetica', 10))
    cwidLabel.pack(pady=(20,5))
    cwidInput = Entry(createWindow, width = 50)
    cwidInput.pack(ipady = 6, pady = (1,10))
    
    # For Name
    nameLabel = Label(createWindow, text = "Enter Your Full Name", fg = 'white', bg = '#0096DC', font = ('helvetica', 10))
    nameLabel.pack(pady = (10,5))
    nameInput = Entry(createWindow, width = 50)
    nameInput.pack(ipady = 6, pady = (1,10))

    # for Email
    emailLabel = Label(createWindow, text='Enter Your Email Address (@latech.edu)', fg = 'white', bg = '#0096DC', font=('helvetica', 10))
    emailLabel.pack(pady=(10,5))
    emailInputNew = Entry(createWindow, width = 50)
    emailInputNew.pack(ipady = 6, pady = (1,10))


    # for passkey
    passKeyLabel = Label(createWindow, text='Enter Pass Key', fg = 'white', bg = '#0096DC', font=('helvetica', 10))
    passKeyLabel.pack(pady=(10,5))
    passKeyInputNew = Entry(createWindow, width = 50)
    passKeyInputNew.pack(ipady = 6, pady = (1,10))

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
        
        # saving it to the JSON file
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}

        if email in users:
            messagebox.showerror("Error", "The account already exists with this email")
        else:
            users[email] = {
                "cwid": cwid,
                "name": name,
                "passKey": passKey
            }

            with open("users.json", "w") as f:
                json.dump(users, f, indent = 4)
            messagebox.showinfo("Yayyy", "The account is created successfully")
            createWindow.destroy()


    createBtn = Button(createWindow, text = "Create an Account", bg = 'white', fg = 'black', width = 20, height = 2, command = saveAccount)
    createBtn.pack(pady=10)



# creating main window
root = tk.Tk()
root.title("Login Page")

# loading the icon image (in .png file)
icon = tk.PhotoImage(file = "icon1.png")

# setting the window icon
root.iconphoto(False, icon)

#root.minsize(100, 100)
#root.maxsize(400,400)

# fixing the size of the screen (seems not working)
root.geometry('350x500')

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

# entry so that user can type their email
email_input = Entry(root, width = 50)    # needed to import Entry class, Label class individually, I don't why this all get install while importing the tkinter
# in order to manage y axis (height), we should use ipady
email_input.pack(ipady = 6, pady = (1,15))

### creating the password label

password_label = Label(root, text='Enter Password', fg='white', bg='#0096DC')
#setting the position
password_label.pack(pady=(20,5))
password_label.config(font=('helvetica', 10))

# entry so that user can type their password
password_input = Entry(root, width = 50)    # needed to import Entry class, Label class individually, I don't why this all get install while importing the tkinter
# in order to manage y axis (height), we should use ipady
password_input.pack(ipady = 6, pady = (1,15))


### using BUTTON CLASS to add LOGIN button
login_btn = Button(root, text = 'Login Here Bulldog', bg = 'white', fg = 'black', width = 20,height=2, command = handle_login)  # command is callilng the function handle_login
login_btn.pack(pady=(10,20))

#adding more buttons
createAccountBtn = Button(root, text = "Create an Account", bg = 'white', fg = 'black', width = 20, height = 2, command=openCreateAccountWindow)
createAccountBtn.pack(pady = (0,20))
createAccountBtn.config(font=('helvetica', 10))


# designing the font
login_btn.config(font=('helvetica', 10))


# let's run the application
root.mainloop()



