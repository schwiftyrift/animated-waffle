def handleTechEmail():
    email = email_input.get()
    password = password_input.get()

    if not email.endswith(".@latech.edu"):
        messagebox.showerror("Error", "Email must be a @latech.edu address")
        return
    
    if email == 'rkg007@latech.edu' and password == '12345':
        messagebox.showinfo('Yayyy', 'Login Successful')
    else:
        messagebox.showerror('Error', 'Login Failed')