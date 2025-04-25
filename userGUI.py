from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import os
from PIL import Image, ImageTk
from playsound import playsound
import threading
from Database import search_items_by_label, checkout_item
from UserData import change_password, check_old_password
import sys
import json
from tkinter import messagebox

if len(sys.argv) > 1:
    user = sys.argv[1]

def load_user_data():
    with open("user_data.json", "r") as f:
        return json.load(f)

def get_user_name(user):
    user_data = load_user_data()
    return user_data.get(user, {}).get("name", None)

def get_cwid(user):
    user_data = load_user_data()
    return user_data.get(user, {}).get("cwid", None)

username = "Jared" #get_user_name(user)
cwid = "123456" #get_cwid(user)
popup = None

img_directory = "images"

columns = ("Item Type", "Color", "Location Found", "Date Found")

def show_details_popup(item):
    global rightFrame
    for widget in rightFrame.winfo_children():
        widget.destroy()
    rightFrame.pack(side=RIGHT, fill=BOTH, expand=True)

    Label(rightFrame, text=f"Item: {item['label'].title()}", font=("Helvetica", 14, "bold"), bg="#1e1f1e", fg="white").pack(pady=10)
    Label(rightFrame, text=f"Color: {item['color'].title()}", font=("Helvetica", 14), bg="#1e1f1e", fg="white").pack(pady=10)
    Label(rightFrame, text=f"Location Found: {item['location']}", font=("Helvetica", 14), bg="#1e1f1e", fg="white").pack(pady=10)
    Label(rightFrame, text=f"Description: {item['description']}", font=("Helvetica", 14), bg="#1e1f1e", fg="white").pack(pady=10)

    img_paths = []
    if os.path.exists(item.get("image", "")):
        img_paths.append(item["image"])
    if os.path.exists(item.get("secondImage", "")):
        img_paths.append(item["secondImage"])

    if img_paths:
        # Track current image index
        current_index = [0]  # use list to allow inner function access

        img = Image.open(img_paths[current_index[0]])
        img = img.resize((600, 400))
        img_tk = ImageTk.PhotoImage(img)

        img_label = Label(rightFrame, image=img_tk, bg="#2c2c2c")
        img_label.image = img_tk
        img_label.pack(pady=10)

        def toggle_image():
            current_index[0] = (current_index[0] + 1) % len(img_paths)
            new_img = Image.open(img_paths[current_index[0]])
            new_img = new_img.resize((600, 400))
            new_img_tk = ImageTk.PhotoImage(new_img)
            img_label.configure(image=new_img_tk)
            img_label.image = new_img_tk

        if len(img_paths) > 1:
            Button(rightFrame, text="Next Photo", command=toggle_image).pack(pady=5)
    else:
        Label(rightFrame, text="Image not available", font=("Helvetica", 12, "italic"), bg="#2c2c2c", fg="gray").pack(pady=10)

    Button(rightFrame, text="Claim", command=lambda: print("Checkout pressed")).pack(pady=10)

def open_settings(username):
    popup = Toplevel(GUI)
    popup.title("User Settings")
    popup.geometry("600x400")
    popup.configure(bg="#2c2c2c")

    def changePassword():
        pass_popup = Toplevel(GUI)
        pass_popup.title("Change Password")
        pass_popup.geometry("600x400")
        pass_popup.configure(bg="#2c2c2c")

        # Make the popup modal
        pass_popup.grab_set()

        old_label = Label(pass_popup, text="Old Password", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
        old_label.pack(pady=(10, 2), anchor="w")
        old_entry = Entry(pass_popup, width=15, font=("Helvetica", 12))
        old_entry.pack(pady=(0,10), fill=X)

        new_label = Label(pass_popup, text="New Password", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
        new_label.pack(pady=(10, 2), anchor="w")
        new_entry = Entry(pass_popup, width=15, font=("Helvetica", 12))
        new_entry.pack(pady=(0,10), fill=X)

        new2_label = Label(pass_popup, text="Retype New Password", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
        new2_label.pack(pady=(10, 2), anchor="w")
        new2_entry = Entry(pass_popup, width=15, font=("Helvetica", 12))
        new2_entry.pack(pady=(0,10), fill=X)

        def changePass():
            oldPass = old_entry.get()
            newPass = new_entry.get()
            newPass2 = new2_entry.get()

            # First, check if the old password is correct
            old_correct = check_old_password(user, oldPass)
            if not old_correct:
                messagebox.showerror("Error", "Old password is incorrect")
                return

            # Check if new passwords match
            if newPass != newPass2:
                messagebox.showerror("Error", "New passwords must match")
                return
                
            if old_correct and newPass == newPass2:
                if not newPass or not newPass2:
                    messagebox.showerror("Error", "Passwords cannot be blank")
                    return
                else:
                    change_password(user, oldPass, newPass)
                    messagebox.showinfo("", f"Password for {user} changed successfully")
                    pass_popup.destroy()  # Only destroy the popup after success

        # Add buttons for changing and exiting
        Button(pass_popup, text="Change Password", command=changePass).pack(pady=(10, 5))
        Button(pass_popup, text="Exit", command=pass_popup.destroy).pack(pady=(10, 5))


    Label(popup, text=username, font=("Helvetica", 14), bg="#2b2b2b", fg="white").pack(pady=10)
    Label(popup, text=f"CWID: {cwid}", font=("Helvetica", 14), bg="#2b2b2b", fg="white").pack(pady=10)
    emailFrame = Frame(popup, bg="#2b2b2b")
    emailFrame.pack(pady=(0, 10))

    emailLabel = Label(emailFrame, text=user, font=("Helvetica", 14), bg="#2b2b2b", fg="white")
    emailLabel.pack(side=LEFT, padx=(0, 10))

    changeEmailButton = Button(emailFrame, text="Change Email", command=popup.destroy)
    changeEmailButton.pack(side=LEFT, padx=10)
    changePassButton = Button(emailFrame, text="Change Password", command=changePassword)
    changePassButton.pack(side=LEFT)

    bottomFrame = Frame(popup, bg="#2b2b2b")
    bottomFrame.pack(pady = 20)

    Button(bottomFrame, text="Logout", command = popup.destroy).pack(side = LEFT, padx=10)
    Button(bottomFrame, text="Exit", command = popup.destroy).pack(side= LEFT)

def on_item_click(event):
    selected_item = search_results.focus()
    if not selected_item:
        return

    index = search_results.index(selected_item)

    # Ensure we have the full data stored
    if hasattr(search_results, "full_data") and index < len(search_results.full_data):
        full_item_data = search_results.full_data[index]

        # Only show details if "Details" column was clicked
        region = search_results.identify("region", event.x, event.y)
        column = search_results.identify_column(event.x)

        if region == "cell" and column in ("#4", "#1"):  # Allow click on Item Type or Details
            show_details_popup(full_item_data)

def play_sound():
        playsound('omni.mp3')
    
def submitSearch(event=None):
    global searchBar, popup, search_results
    search = searchBar.get()

    '''
    if popup is None or not popup.winfo_exists():
        popup = Toplevel(GUI)
        popup.title(search)
        
        if search in ("Josh", "David"):
            with open("omni.txt", "r", encoding="utf-8") as file:
                ascii_art = file.read()
            easterEgg = Label(popup, text=ascii_art, font=("Helvetica", 50))
            easterEgg.pack()
            threading.Thread(target=play_sound).start()
        
        close_button = Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=5)
    else:
        popup.lift()
        popup.focus()
    '''

    # Refresh results regardless of popup state
    results = search_items_by_label(search)
    for row in search_results.get_children():
        search_results.delete(row)

    for index, item in enumerate(results):
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        values = (item["label"].title(), item["color"], item["location"], item.get("date", "Unknown"))
        search_results.insert("", "end", values=values, tags=(tag,))

    search_results.full_data = results
    return search

def show_details(item):
    pass

##############################################################################################

GUI = Tk()
GUI.title("Lost and Found System")
GUI.attributes("-fullscreen", True)
GUI.configure(bg="#1e1f1e")
GUI.bind('<Escape>', lambda e: GUI.quit())

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", rowheight=30, background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white")
style.map("Treeview", background=[('selected', '#4a6984')])

# --- Layout Frame ---
main_frame = Frame(GUI, bg="#1e1f1e")
main_frame.pack(fill = BOTH, expand= True)

titleFrame = Frame(main_frame, bg="#1e1f1e")
titleFrame.pack(side = TOP)

titleLabel = Label(titleFrame, text = "Lost and Found", font=("Helvetica", 18), bg="#1e1f1e", fg = "white")
titleLabel.pack(side = RIGHT, pady=10)

searchFrame = Frame(main_frame, bg="#1e1f1e")
searchFrame.pack(side=TOP, fill=X, padx=20, pady=20)

divideFrame = Frame(main_frame, bg="#1e1f1e")
divideFrame.pack(fill = BOTH, expand = True)

leftFrame = Frame(divideFrame, bg="#1e1f1e")
leftFrame.pack(side = LEFT, fill = BOTH)

rightFrame = Frame(divideFrame, bg="#1e1f1e")
rightFrame.pack(side = RIGHT, fill = BOTH)

searchBar = Entry(searchFrame, width = 63, font=("Helvetica", 16))
searchBar.pack(pady = 15, side=LEFT)
searchBar.bind("<Return>", submitSearch)
searchButton = Button(searchFrame, text="Search 🔎", font=("Helvetica", 11), command=submitSearch)
searchButton.pack(pady = 15, padx= 5, side= LEFT)
userSettings = Button(searchFrame, text="⚙️ Settings", font=("Helvetica", 11), command= lambda:open_settings(username))
userSettings.pack(side = RIGHT)
userLabel = Label(searchFrame, text = f"{username}", font=("Helvetica", 18), bg="#1e1f1e", fg = "white")
userLabel.pack(side = RIGHT, padx =5)

search_results = Treeview(leftFrame, columns = columns, show="headings")
search_results.tag_configure("oddrow", background="#2b2b2b")
search_results.tag_configure("evenrow", background="#333333")

for col in columns:
    search_results.heading(col, text=col, anchor="center")
    search_results.column(col, anchor="center", width = 200)

scrollbar = Scrollbar(leftFrame, orient="vertical", command=search_results.yview)
search_results.configure(yscrollcommand=scrollbar.set)

search_results.pack(side=LEFT, fill=BOTH, padx = 20)
scrollbar.pack(side= RIGHT, fill=Y)

search_results.bind("<ButtonRelease-1>", on_item_click)


GUI.mainloop()