import tkinter as tk

def mobile_phone_filter():
    print("Mobile filter clicked")
    # needs to add logic
def tolliverStation_filter():
    print("Tolliver Station filter clicked")
    # needs to add logic

def go_back():
    print("Back Button Clicked")
    # needs to add logic

def claimYourItem_button_action():
    print("Claim button clicked")
    #needs to add logic
 

root = tk.Tk()
root.title("Automated Lost and Found Items")
root.configure(bg = "#0096DC")  # adding bluish bg

### Above section
above_frame = tk.Frame(root, bg = "#0096DC")
above_frame.pack(fill="x", padx=10, pady=10)

mobile_phone_button = tk.Button(above_frame, text="Mobile Phone", command=mobile_phone_filter, bg = 'white', fg='black', relief='flat', padx=10, pady=5)
mobile_phone_button.pack(side="left", padx=(0,5))  # added some right padding

tolliverStation_button = tk.Button(above_frame, text = "Tolliver Station", command=tolliverStation_filter, bg = 'white', fg='black', relief='flat', padx = 10, pady= 5)
tolliverStation_button.pack(side="left", padx=(0,5))

go_back_button = tk.Button(above_frame, text= "Go Back", command=go_back, bg='white', fg='black', relief="flat", padx=10, pady=5)


### mid section

description_frame = tk.Frame(root, bg = "#0096DC", padx=20, pady =10)
description_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)

item_label = tk.Label(description_frame, text="Item: Mobile Phone", bg ='white', fg = 'black', anchor = 'w')
item_label.pack(fill="x", pady = (0,5))

location_label = tk.Label(description_frame, text = "Location Found: Tolliver Station", bg ='white', fg='black', anchor='w')
location_label.pack(fill='x', pady=(0,5))

coloring_label = tk.Label(description_frame, text = "Color: Black", bg ='white', fg='black', anchor='w')
coloring_label.pack(fill='x', pady=(0,5))

moreInfo_label = tk.Label(description_frame, text = "More Info: Samsung", bg ='white', fg='black', anchor='w')
moreInfo_label.pack(fill='x', pady=(0,5))

### image placeholders)
image_frame = tk.Frame(root, bg = "#0096DC", padx= 10, pady=10)
image_frame.pack(side="left", fill="y")

image_placeholderA = tk.Canvas(image_frame, width = 200, height=150, bg="white", highlightthickness=0)
image_placeholderA.pack(pady=(0,10))
# loading of images and displaying will be done here

image_placeholderB = tk.Canvas(image_frame, width = 200, height=150, bg="white", highlightthickness=0)
image_placeholderB.pack(pady=(0,10))
# loading of images and displaying will be done here

### Below section

bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(fill="x", padx=10, pady=10, side ='bottom')

claimYourItem_button = tk.Button(bottom_frame, text="Claiming The Item", command = claimYourItem_button_action, bg='white', fg='white', relief='flat', padx=20, pady=10)
claimYourItem_button.pack(side='bottom', anchor="se")  # anchor is at the below right

root.mainloop()






