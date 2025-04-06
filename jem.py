# ###Jem
# import tkinter as tk

# def cell_phone_filter():
#     print("Cell Phone filter applied")
#     # Add your logic to filter by "Cell Phone" here

# def tolliver_filter():
#     print("Tolliver filter applied")
#     # Add your logic to filter by "Tolliver" here

# def back_button_action():
#     print("Back button clicked")
#     # Add your logic for the back button here

# def claim_button_action():
#     print("Claim button clicked")
#     # Add your logic for the claim button here

# root = tk.Tk()
# root.title("Lost and Found Items")
# root.configure(bg="#333333") # Dark background

# # --- Top Section (Filters and Back Button) ---
# top_frame = tk.Frame(root, bg="#333333")
# top_frame.pack(fill="x", padx=10, pady=10)

# cell_phone_button = tk.Button(top_frame, text="Cell Phone", command=cell_phone_filter, bg="#555555", fg="white", relief="flat", padx=10, pady=5)
# cell_phone_button.pack(side="left", padx=(0, 5)) # Add some right padding

# tolliver_button = tk.Button(top_frame, text="Tolliver", command=tolliver_filter, bg="#555555", fg="white", relief="flat", padx=10, pady=5)
# tolliver_button.pack(side="left", padx=(0, 5))

# back_button = tk.Button(top_frame, text="Back", command=back_button_action, bg="#555555", fg="white", relief="flat", padx=10, pady=5)
# back_button.pack(side="right")

# # --- Middle Section (Item Details) ---
# details_frame = tk.Frame(root, bg="#333333", padx=20, pady=10)
# details_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)

# item_label = tk.Label(details_frame, text="Item: Cell Phone", bg="#333333", fg="white", anchor="w")
# item_label.pack(fill="x", pady=(0, 5))

# location_label = tk.Label(details_frame, text="Location Found: Tolliver", bg="#333333", fg="white", anchor="w")
# location_label.pack(fill="x", pady=(0, 5))

# color_label = tk.Label(details_frame, text="Color: Black", bg="#333333", fg="white", anchor="w")
# color_label.pack(fill="x", pady=(0, 5))

# additional_info_label = tk.Label(details_frame, text="Additional Info: Samsung", bg="#333333", fg="white", anchor="w")
# additional_info_label.pack(fill="x", pady=(0, 10))

# # --- Left Section (Image Placeholders) ---
# image_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
# image_frame.pack(side="left", fill="y")

# image_placeholder1 = tk.Canvas(image_frame, width=200, height=150, bg="#dddddd", highlightthickness=0)
# image_placeholder1.pack(pady=(0, 10))
# # You would load and display images here

# image_placeholder2 = tk.Canvas(image_frame, width=200, height=150, bg="#dddddd", highlightthickness=0)
# image_placeholder2.pack()
# # You would load and display images here

# # --- Bottom Section (Claim Button) ---
# bottom_frame = tk.Frame(root, bg="#333333")
# bottom_frame.pack(fill="x", padx=10, pady=10, side="bottom")

# claim_button = tk.Button(bottom_frame, text="Claim", command=claim_button_action, bg="#555555", fg="white", relief="flat", padx=20, pady=10)
# claim_button.pack(side="bottom", anchor="se") # Anchor to the bottom-right

# root.mainloop()
