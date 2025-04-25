from tkinter import *
import cv2
from detector import Detector
import logging
from PIL import Image, ImageTk
from Database import *
import os
from datetime import datetime

img_directory = "images"
os.makedirs(img_directory, exist_ok=True)

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
result_label = None

# buttons
capture_button = None
photo_button = None
toggle_button = None

# Trackers
label = []
color = []
description = ""
boxes = []
pressed = False
last_detected_frame = None
second_detected_frame = None
continue_updating = True
live_preview_running = False
currently_showing_live_capture = True
second_photo = False

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

def get_current_date():
    return datetime.now().strftime("%b %d, %Y").replace(" 0", " ")

def savePhoto(frame, id, boxes = None):
        croppedFrame = None
        if boxes != None:
            for box in boxes:
                if len(box) == 4:  # Ensure valid bounding box
                    x1, y1, x2, y2 = box
                    croppedFrame = frame[y1:y2, x1:x2]
                    cv2.imwrite(f"images/{id}(1).jpg", croppedFrame)
        else:
            cv2.imwrite(f"images/{id}(2).jpg", frame)

        return

def togglePhoto():
    global currently_showing_live_capture, last_detected_frame, second_detected_frame

    if currently_showing_live_capture:
        # Show detection image (last_detected_frame)
        frame_to_show = last_detected_frame
    else:
        # Show live captured image (second_detected_frame)
        frame_to_show = second_detected_frame

    currently_showing_live_capture = not currently_showing_live_capture

    if frame_to_show is not None:
        img = cv2.cvtColor(frame_to_show, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(img)
        photo_image = ImageTk.PhotoImage(image=image)
        result_label.configure(image=photo_image)
        result_label.photo_image = photo_image


def show_caputure_button():
    start_preview()
    toggle_button.pack_forget()
    photo_button.pack_forget()
    capture_button.pack(side=RIGHT)
    photo_button.pack(side=RIGHT, padx = 15)

def start_preview():
    global live_preview_running
    live_preview_running = True
    update_preview_frame()

def update_preview_frame():
    global live_preview_running
    if not live_preview_running:
        return
    
    ret, frame = capture.read()
    if not ret:
        return
    
    preview_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(preview_image)
    photo = ImageTk.PhotoImage(image=img)

    result_label.configure(image=photo)
    result_label.photo_image = photo

    result_label.current_frame = frame.copy()

    GUI.after(10, update_preview_frame)

def takePhoto():
    global second_detected_frame, live_preview_running, second_photo
    live_preview_running = False

    if hasattr(result_label, "current_frame"):
        second_detected_frame = result_label.current_frame.copy()

    
    img = cv2.cvtColor(last_detected_frame, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(img)
    photo_image = ImageTk.PhotoImage(image=image)
    result_label.configure(image=photo_image)
    result_label.photo_image = photo_image

    capture_button.pack_forget()
    photo_button.pack_forget()
    toggle_button.pack(side=RIGHT)

    second_photo = True


def submit():
    global label
    global color
    global description_entry
    global location_entry

    date = get_current_date()

    description = description_entry.get()
    lab = item_entry.get()
    col = color_entry.get()
    loc = location_entry.get()

    id = inputData(lab, col, second_photo, date, description, loc)

    savePhoto(last_detected_frame, id, boxes)
    savePhoto(second_detected_frame, id)
    return_to_main()

def return_to_main():
    global label, color, second_photo

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
    second_photo = False
    
    main_frame.pack(anchor="nw", padx=30, pady=50)
    update_frame()

def show_second_screen():
    # Clear any existing widgets in second_frame
    for widget in second_frame.winfo_children():
        widget.destroy()
    
    global last_detected_frame, description_entry, item_entry, location_entry, color_entry, result_label, capture_button, photo_button, toggle_button

    main_frame.pack_forget()
    second_frame.pack(anchor="nw", fill=BOTH, expand=True, padx=30, pady=50)

    # === LEFT SIDE (Image with Back and Take Photo at bottom) ===
    left_frame2 = Frame(second_frame, bg="#1e1f1e")
    left_frame2.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

    # Top: Image display frame that expands
    image_frame = Frame(left_frame2, bg="#1e1f1e")
    image_frame.pack(side=TOP, fill=BOTH, expand=True)
    try:
        image = Image.fromarray(cv2.cvtColor(last_detected_frame, cv2.COLOR_BGR2RGBA))
        photo_image = ImageTk.PhotoImage(image=image)
    except Exception as e:
        print("Error converting image:", e)
        return
    result_label = Label(image_frame, image=photo_image, bg="#1e1f1e", width=980, height=720)
    result_label.photo_image = photo_image  # Keep reference
    result_label.pack(fill=BOTH, expand=True)

    # Bottom: Button frame for Back & Take Photo
    left_button_frame = Frame(left_frame2, bg="#1e1f1e")
    left_button_frame.pack(side=BOTTOM, fill=X, pady=10)
    back_button = Button(left_button_frame, text="Back ⬅️", command=return_to_main, font=("Helvetica", 14))
    back_button.pack(side = LEFT)

    capture_button = Button(
        left_button_frame,
        text="📸 Capture",
        command=takePhoto,
        font=("Helvetica", 14),
        padx=20)

    toggle_button = Button(
        left_button_frame,
        text="🔄 Toggle Photo",
        command=togglePhoto,
        font=("Helvetica", 14),
        padx=20
        )
    toggle_button.pack(side=RIGHT)

    photo_button = Button(left_button_frame, text="Add Another Photo",
                          command=show_caputure_button,
                          font=("Helvetica", 14), padx=20)
    photo_button.pack(padx = 15, side = RIGHT)

    # === RIGHT SIDE (Form with Submit button at bottom) ===
    right_frame2 = Frame(second_frame, bg="#1e1f1e")
    right_frame2.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

    # Top: Form frame that expands
    form_frame = Frame(right_frame2, bg="#1e1f1e")
    form_frame.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=20)

    # Detection Results Heading
    detect_label = Label(form_frame, text="Detection Results", font=("Helvetica", 20, "bold"),
                         bg="#1E1F1E", fg="white", wraplength=300)
    detect_label.pack(anchor="n", fill=X, pady=10)

    directions_label = Label(form_frame, text="The below input fields are autopopulated based on detection. "
                           "Please correct any mistakes and/or enter a description of the item. Once finished, press the submit button.",
                           font=("Helvetica", 12, "bold"), bg="#1E1F1E", fg="white", wraplength=350)
    directions_label.pack(anchor="n", fill=X, pady=10)

    # Input fields
    item_label = Label(form_frame, text="Item Type", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
    item_label.pack(pady=(10, 2), anchor="w")
    item_entry = Entry(form_frame, width=45, font=("Helvetica", 12))
    item_entry.pack(pady=(0,10), fill=X)

    color_label = Label(form_frame, text="Color", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
    color_label.pack(pady=(10, 2), anchor="w")
    color_entry = Entry(form_frame, width=45, font=("Helvetica", 12))
    color_entry.pack(pady=(0,10), fill=X)

    location_label = Label(form_frame, text="Location", fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
    location_label.pack(pady=(10, 2), anchor="w")
    location_entry = Entry(form_frame, width=45, font=("Helvetica", 12))
    location_entry.pack(pady=(0,10), fill=X)

    description_label = Label(form_frame, text="Description (Brand, markings, case color, etc.)",
                              fg="white", bg="#1e1f1e", font=("Helvetica", 12, "bold"))
    description_label.pack(pady=(10, 2), anchor="w")
    description_entry = Entry(form_frame, width=45, font=("Helvetica", 12))
    description_entry.pack(pady=(0,10), fill=X)

    # Prepopulate entries if desired
    if label:
        item_entry.insert(10, label[0])
    if color:
        color_entry.insert(10, color[0])
    location_entry.insert(10, "Tolliver")

    # Bottom: Submit button frame (anchored at bottom)
    right_button_frame = Frame(right_frame2, bg="#1e1f1e")
    right_button_frame.pack(side=BOTTOM, fill=X, pady=10)
    submit_button = Button(right_button_frame, text="Submit ➡️", command=submit,
                           font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=15)
    submit_button.pack()

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
        global boxes
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