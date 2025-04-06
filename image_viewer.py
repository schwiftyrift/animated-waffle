from tkinter import *
from PIL import ImageTk,Image
import os # using os module we can navigate inside folders and fiels

def rotate_image():  # creating the function rotate image
    global counter
    img_label.config(image=img_array[counter%len(img_array)])
    counter = counter + 1

counter = 1
root = Tk()
root.title('Image Viewer')

root.geometry('250x400')
root.configure(background='black')

files = os.listdir('images')
#print(files)

img_array = [] # creating arrays to load images one by one
for file in files:
    img = Image.open(os.path.join('images', file))
    resized_img = img.resize((200,300))
    img_array.append(ImageTk.PhotoImage(resized_img))

#print(img_array)

img_label = Label(root, image=img_array[0])
img_label.pack(pady = (15, 10))  # fitting the image on the screen

next_btn = Button(root, text = 'Next', bg ='white', fg= 'black', width=25, height=2, command=rotate_image) # command will call the function
next_btn.pack()
root.mainloop()