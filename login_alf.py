import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from PIL import ImageTk, Image

def handle_login():
    email = email_input.get()   # storing the email given from user
    password = password_input.get()  # storing the password given from user
    print(email, password)

    if email == 'rkg007@latech.edu' and password == '12345':
        messagebox.showinfo('Yayyy', 'Login Successful')
    else:
        messagebox.showerror('Error','Login Failed')


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

# designing the font
login_btn.config(font=('helvetica', 10))

# let's run the application
root.mainloop()



