from tkinter import *
import cv2
from detector import Detector
import logging
from PIL import Image, ImageTk
from Database import *

# Create GUI instance
GUI = Tk()
GUI.title("Lost and Found Detection") 

# Set window size (optional)
GUI.attributes("-fullscreen", True)

GUI.configure(bg="#1e1f1e")

GUI.bind('<Escape>', lambda e: GUI.quit())

# Suppress YOLOv8 output to terminal
logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

# Initializes the detector
detector = Detector(model_path="best.pt")

# Open webcam
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set high resolution
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if not capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

#Text entry box
description_entry = None
item_entry = None
location_entry = None
color_entry = None

# Trackers
label = []
color = []
description = ""

pressed = False
last_detected_frame = None
continue_updating = True

# --- Layout Frame ---
main_frame = Frame(GUI, bg="#1e1f1e")
main_frame.pack(anchor="nw", padx=30, pady=50)

# --- Second Frame ---
second_frame = Frame(GUI, bg="#1e1f1e")

# --- Left Frame ---
left_frame = Frame(main_frame, bg="#1e1f1e")
left_frame.pack(side = LEFT, padx=20, pady=20)

# --- Right Frame ---
right_frame = Frame(main_frame, bg="#1e1f1e")
right_frame.pack(side = RIGHT, fill=Y, padx=20, pady=2)

# --- Camera Preview ---
camera_widget = Label(left_frame, bg="#1e1f1e", width=980, height=720)
camera_widget.pack(expand=True)

# --- Detect Button ---
def change_Press(value):
    global pressed
    pressed = value

detect_button = Button(
    left_frame,
    text="Start Detection",
    command=lambda: change_Press(True),
    font=("Helvetica", 16),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10
)
detect_button.pack(pady= 20)

title = Label(
    right_frame,
    text = "Automated Lost and Found System",
    font=("Helvtica", 19, 'bold'),
    justify = CENTER,
    bg="#1E1F1E",
    fg="white"
)
title.pack(anchor='n', side=TOP, fill=X, pady =25)

instructions_title = Label(
    right_frame,
    text="🔍 How to Use:",
    font=("Helvetica", 14, 'bold'),
    justify=LEFT,
    bg="#1E1F1E",
    fg="white",
    wraplength=300  # ← wrap at 300 pixels (adjust as needed)
)
instructions_title.pack(anchor='n', side=TOP, fill=X, pady = 20)

instructions = Label(
    right_frame,
    text="1. Position object in front of the camera.\n\n\n2. Click 'Start Detection'.\n\n\n3. Review detection on next screen\n\n\n🎯 Tip: Make sure the object is well-lit and centered.",
    font=("Helvetica", 14),
    justify=LEFT,
    bg="#1E1F1E",
    fg="white",
    wraplength=300  # ← wrap at 300 pixels (adjust as needed)
)
instructions.pack(anchor='n', side=TOP, fill=X)

def submit():
    global label
    global color
    global description_entry

    description = description_entry.get()
    inputData(label[0], color[0], description)
    return_to_main()

def return_to_main():
    global label
    global color

    second_frame.pack_forget()

    # Clear second_frame to avoid clutter next time
    for widget in second_frame.winfo_children():
        widget.destroy()

    # Reset flags, etc. if needed
    global pressed, continue_updating
    pressed = False
    continue_updating = True

    label = []
    color = []
    
    main_frame.pack(anchor="nw", padx=30, pady=50)
    update_frame()

def show_second_screen():
    for widget in second_frame.winfo_children():
        widget.destroy()
    
    global last_detected_frame
    global description_entry
    global item_entry
    global location_entry
    global color_entry


    main_frame.pack_forget()
    second_frame.pack(anchor="nw", padx=30, pady=50)

    # --- Left Frame ---
    left_frame2 = Frame(second_frame, bg="#1e1f1e")
    left_frame2.pack(side = LEFT, padx=20, pady=20)

    # --- Right Frame ---
    right_frame2 = Frame(second_frame, bg="#1e1f1e")
    right_frame2.pack(side = RIGHT, fill=Y, padx=20, pady=30)

    # Convert the clean last frame to Tkinter-compatible image
    image = Image.fromarray(cv2.cvtColor(last_detected_frame, cv2.COLOR_BGR2RGBA))
    photo_image = ImageTk.PhotoImage(image=image)

    result_label = Label(left_frame2, image=photo_image, bg="#1e1f1e", width=980, height=720)
    result_label.photo_image = photo_image  # Keep reference
    result_label.pack(expand=True)

    # back button
    back_button = Button(left_frame2, text="Back", command=return_to_main, font=("Helvetica", 14))
    back_button.pack(pady=20)

    # detection results
    detect_label = Label(
    right_frame2,
    text="Detection Results",
    font=("Helvetica", 20, 'bold'),
    justify=CENTER,
    bg="#1E1F1E",
    fg="white",
    wraplength=300  # ← wrap at 300 pixels (adjust as needed)
    )
    detect_label.pack(anchor='n', side=TOP, fill=X, pady =25, padx= 20)

    directions_label = Label(
    right_frame2,
    text="The below input fields are autopopulated based on detection. Please correct any mistakes and/or enter a description of the item. Once finished, press the sumbit button.",
    font=("Helvetica", 12, 'bold'),
    justify=LEFT,
    bg="#1E1F1E",
    fg="white",
    wraplength=350  # ← wrap at 300 pixels (adjust as needed)
    )
    directions_label.pack(anchor='n', side=TOP, fill=X, pady =25, padx= 20)

    item_label = Label(right_frame2, text="Item Type", fg="white", bg="#1e1f1e", font=("Helvetica", 12, 'bold'))
    item_label.pack(pady=(10, 2), anchor='w', padx= 20 )
    item_entry = Entry(right_frame2, width=45, font=("Helvetica", 12))
    item_entry.pack(pady=(0,10), fill=X, padx= 20)

    color_label = Label(right_frame2, text="Color", fg="white", bg="#1e1f1e", font=("Helvetica", 12, 'bold'))
    color_label.pack(pady=(10, 2), anchor='w', padx= 20)
    color_entry = Entry(right_frame2, width=45, font=("Helvetica", 12))
    color_entry.pack(pady=(0,10), fill=X, padx=20)

    location_label = Label(right_frame2, text="Location", fg="white", bg="#1e1f1e", font=("Helvetica", 12, 'bold'))
    location_label.pack(pady=(10, 2), anchor='w', padx= 20)
    location_entry = Entry(right_frame2, width=45, font=("Helvetica", 12))
    location_entry.pack(pady=(0,10), fill=X, padx= 20)

    description_label = Label(right_frame2, text="Description (Brand, markings, case color, etc.)", fg="white", bg="#1e1f1e", font=("Helvetica", 12, 'bold'))
    description_label.pack(pady=(10, 2), anchor='w', padx= 20)
    description_entry = Entry(right_frame2, width=45, font=("Helvetica", 12))
    description_entry.pack(pady=(0,10), fill=X, padx= 20)

    item_entry.insert(10, label[0])
    color_entry.insert(10, color[0])
    location_entry.insert(10, "Tolliver")


    submit_button = Button(right_frame2,
        text="Submit",
        command=submit,
        font=("Helvetica", 12),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10)
    submit_button.pack(pady= 20)

    

# --- Frame Updater ---
def update_frame():
    global pressed, label, color, last_detected_frame, continue_updating

    if not continue_updating:
        return

    ret, frame = capture.read()
    if not ret:
        print("Failed to grab frame.")
        GUI.after(10, update_frame)
        return
    
    cleanFrame = frame.copy()
    
    if pressed:
        frame_with_boxes, labels, boxes = detector.detectObject(frame)
        last_detected_frame = cleanFrame.copy()  # clean version for later

        if labels:
            for lbl in labels:
                if len(label) < 20:
                    label.append(lbl)
            print("Detected Object:", label)

        if boxes:
            colors = detector.detectColor(frame, boxes)
            for col in colors:
                if len(color) < 20:
                    color.append(col)
            print("Detected Colors:", color)

        # Show the image with boxes *right now*
        opencv_image = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)
        camera_widget.photo_image = photo_image
        camera_widget.configure(image=photo_image)

        # Schedule transition *after* preview is shown
        continue_updating = False
        GUI.after(2000, show_second_screen)
        return

    # Convert OpenCV frame to Tkinter image
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    photo_image = ImageTk.PhotoImage(image=captured_image)

    camera_widget.photo_image = photo_image
    camera_widget.configure(image=photo_image)

    GUI.after(10, update_frame)

# Start updating frames

GUI.after(0, update_frame)
GUI.mainloop()