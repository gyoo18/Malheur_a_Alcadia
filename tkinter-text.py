import tkinter as tk
from tkinter import Canvas,Button,Frame,Label

# Initialize the window
root = tk.Tk()
root.title("Medieval Game Map")
root.geometry("600x550")  # Ensure enough height
root.configure(bg="#d7bd97")  # Parchment-like background

# isFrameVisible = True
# frame = Frame(root,bg="#000000")
# frame2 = Frame(root,bg="#000000")
# 
# # Add a game title
# title_label = tk.Label(
#     frame,
#     text="le jeux",
#     font=("Old English Text MT", 24, "bold"),
#     bg="#d7bd97",
#     fg="#4b2e83"
# )
# title_label.pack(pady=10)
# 
# # Add a canvas
# canvas = Canvas(frame, width=600, height=400, bg="#f4e7c3", relief="ridge", bd=4)
# canvas.pack()
# 
# 
# # Add a player (Knight token)
# player = canvas.create_oval(50, 50, 70, 70, fill="#c62828", outline="#7b1b1b")  # Red Knight
# 
# # Player movement logic
# def move_up():
#     canvas.move(player, 0, -10)
# 
# def move_down():
#     canvas.move(player, 0, 10)
# 
# def move_left():
#     canvas.move(player, -10, 0)
# 
# def move_right():
#     canvas.move(player, 10, 0)
# 
# # Add control buttons
# button_frame = tk.Frame(root, bg="#d7bd97")
# # button_frame.pack(in_=frame,pady=10)
# 
# btn_style = {"font": ("Verdana", 10, "bold"), "bg": "#4b2e83", "fg": "white", "relief": "raised", "width": 5}
# btn_up = tk.Button(button_frame, btn_style, text="Up", command=move_up)
# btn_down = tk.Button(button_frame, btn_style, text="Down", command=move_down)
# btn_left = tk.Button(button_frame, btn_style, text="Left", command=move_left)
# btn_right = tk.Button(button_frame, btn_style, text="Right", command=move_right)
# 
# 
# # Arrange buttons in a grid
# btn_up.grid(row=0, column=1, padx=5, pady=5)
# btn_left.grid(row=1, column=0, padx=5, pady=5)
# btn_down.grid(row=1, column=1, padx=5, pady=5)
# btn_right.grid(row=1, column=2, padx=5, pady=5)
# 
# frame.pack(fill="both",expand=True,padx=10,pady=10)
# 
# def show_hide():
#     global isFrameVisible
#     if isFrameVisible:
#         frame.pack_forget()
#         isFrameVisible = False
#     else:
#         frame.pack(fill="both",expand=True,padx=10,pady=10)
#         isFrameVisible=True
# 
# button_show_hide = Button(root,btn_style, text="Show/Hide", command=show_hide)
# button_show_hide.pack(pady=10)
# 
# # title_label.pack_forget()
# title_label.pack(in_=frame2)
# frame2.pack()

label1 = Label(root,text="Test!")
label2 = Label(root,text="Test2!")
frame1 = Frame(root)
frame2 = Frame(root)
frame1.pack()
frame2.pack()
label1.pack(in_=frame1)
label2.pack(in_=frame1)
label1.pack_forget()
label1.pack(in_=frame2)

# Run the application
root.mainloop()