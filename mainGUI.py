from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from kioskGUI import run_kiosk_gui
from searchGUI import run_user_gui
from UserData import login
import sys
import json
import os

def launch_gui():
    if len(sys.argv) > 1:
        user = sys.argv[1]
    else:
        user = "default_user"

    logged_in = False

    root = Tk()
    root.title("Lost and Found System")
    root.attributes("-fullscreen", True)
    root.configure(bg="#1e1f1e")
    root.bind('<Escape>', lambda e: root.quit())

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TNotebook", background="#1e1f1e", borderwidth=2)
    style.configure("TNotebook.Tab",
                    background="#333333",
                    foreground="white",
                    padding=[20, 15],
                    font=('Arial', 14))
    style.map("TNotebook.Tab",
              background=[("selected", "#555555"), ("!selected", "#333333")],
              foreground=[("selected", "white"), ("!selected", "gray")])

    # Top bar frame
    top_bar = Frame(root, bg="#1e1f1e")
    top_bar.pack(side=TOP, fill=X)





    '''
    login_button = Button(top_bar, text="Login for Item Search", command=lambda: open_login_window(), bg='white', font=("Helvetica", 12))
    login_button.pack(side=RIGHT, padx=20, pady=5)
    '''

    logout_button = Button(top_bar, text="Logout", command=lambda: logout(), bg='white', font=("Arial", 12))
    
    def on_tab_changed(event):
        selected_tab = event.widget.index("current")
        if selected_tab == 1:  # Item Search tab index
            if logged_in == False:
                # Prevent switching to the tab
                notebook.tab(1, state="disabled")
                notebook.select(0)
                open_login_window()

    # Notebook underneath
    notebook = ttk.Notebook(root)
    notebook.pack(fill=BOTH, expand=True)
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
    kiosk_frame = Frame(notebook, bg="#1e1f1e")
    user_gui_frame = Frame(notebook, bg="#1e1f1e")

    notebook.add(kiosk_frame, text="Item Detection")
    notebook.add(user_gui_frame, text="Item Search")

    # Disable Item Search tab initially
    #notebook.tab(1, state='disabled')

    run_kiosk_gui(kiosk_frame)

    def logout():
            nonlocal logged_in
            notebook.select(0)
            logout_button.pack_forget()
            logged_in = False

            for widget in user_gui_frame.winfo_children():
                widget.destroy()
            user_gui_frame.pack_forget()

            messagebox.showinfo("Logged Out", "You have been logged out.")

    def open_login_window():

        def open_create_account_window():
            create_win = Toplevel(login_win)
            create_win.title("Create an Account")
            create_win.geometry("400x400")
            create_win.configure(bg="#333333")
            create_win.grab_set()

            Label(create_win, text="CWID", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
            cwid_entry_new = Entry(create_win, font=("Arial", 12))
            cwid_entry_new.pack(pady=5)

            Label(create_win, text="Full Name", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
            name_entry = Entry(create_win, font=("Arial", 12))
            name_entry.pack(pady=5)

            Label(create_win, text="Password", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
            pass_entry_new = Entry(create_win, font=("Arial", 12))
            pass_entry_new.pack(pady=5)

            def save_account():
                cwid = cwid_entry_new.get()
                name = name_entry.get()
                password = pass_entry_new.get()

                if not (cwid and name and password):
                    messagebox.showerror("Error", "All fields are mandatory", parent=create_win)
                    return

                if len(cwid) != 8 or not cwid.isdigit():
                    messagebox.showerror("Error", "CWID must be 8 digits", parent=create_win)
                    return

                from UserData import register_user  # import here to avoid circular imports if necessary
                success = register_user(cwid, password, name)
                if not success:
                    messagebox.showerror("Error", "An account already exists with this CWID", parent=create_win)
                else:
                    messagebox.showinfo("Success", "Account created successfully", parent=create_win)
                    create_win.destroy()

            Button(create_win, text="Create Account", command=save_account, bg="white", font=("Arial", 12)).pack(pady=20)

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
                cwid_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)
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

        login_win = Toplevel(root)
        login_win.title("Login for Item Search")
        login_win.geometry("400x300")
        login_win.configure(bg="#333333")
        login_win.grab_set()

        storedUser, storedPass = load_credentials()
        Label(login_win, text="CWID", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
        cwid_entry = Entry(login_win, font=("Arial", 12))
        cwid_entry.insert(0, storedUser)
        cwid_entry.pack(pady=5)

        Label(login_win, text="Password", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
        pass_entry = Entry(login_win, show="*", font=("Arial", 12))
        pass_entry.insert(0, storedPass)
        pass_entry.pack(pady=5)

        checkValue = tk.IntVar()
        rememberLogin = tk.Checkbutton(login_win, text = "Remember Me", variable = checkValue)
        rememberLogin.configure(bg="#333333", fg="white", activebackground="#333333", selectcolor="#333333")
        rememberLogin.pack()

        if storedUser and storedPass:
            checkValue.set(1)

        def attempt_login():
            nonlocal logged_in
            cwid = cwid_entry.get()
            password = pass_entry.get()
            success = login(cwid, password)
            if success:
                messagebox.showinfo("Login", "Login Successful!")
                run_user_gui(user_gui_frame, cwid)
                save_credentials(cwid, password, checkValue.get())
                notebook.tab(1, state='normal')
                notebook.select(1)
                login_win.destroy()
                logged_in = True
                logout_button.pack(side=RIGHT, padx=20, pady=5)  # Show logout
            else:
                messagebox.showerror("Error", "Invalid CWID or password")
                pass_entry.delete(0, tk.END)
                pass_entry.focus_set()

        Button(login_win, text="Login", command=attempt_login, bg="white", font=("Arial", 12)).pack(pady=20)
        Button(login_win, text="Create Account", command=open_create_account_window, bg="white", font=("Arial", 12)).pack(pady=5)
    root.mainloop()


if __name__ == '__main__':
    launch_gui()