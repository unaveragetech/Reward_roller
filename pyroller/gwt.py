import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import random
import json
from PIL import ImageTk, Image

contestants = []

def pick_winner():
    if len(contestants) == 0:
        messagebox.showwarning("No Contestants", "Please add contestants before picking a winner.")
        return

    show_reward_message()

def show_contestants():
    contestants_text = "\n".join(contestants)
    messagebox.showinfo("Contestants", contestants_text)

def add_contestant():
    new_contestant = contestant_entry.get().strip()
    if new_contestant:
        contestants.append(new_contestant)
        contestant_entry.delete(0, tk.END)
        messagebox.showinfo("Contestant Added", "Contestant has been added successfully.")
        save_contestants_to_file()
    else:
        messagebox.showwarning("Missing Information", "Please enter a contestant name.")

def save_contestants_to_file():
    with open("contestants.txt", "w") as file:
        for contestant in contestants:
            file.write(contestant + "\n")

def load_contestants_from_file():
    try:
        with open("contestants.txt", "r") as file:
            contestants.clear()
            for line in file:
                contestant = line.strip()
                contestants.append(contestant)
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "Contestants file not found. Creating a new one.")

def browse_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if filepath:
        load_image(filepath)

def load_image(filepath):
    global prize_image
    prize_image = ImageTk.PhotoImage(Image.open(filepath))
    prize_image_label.configure(image=prize_image)

def show_reward_message():
    reward_message = tk.Toplevel(root)
    reward_message.title("Reward Information")

    item_name_label = tk.Label(reward_message, text="Item Name:")
    item_name_label.grid(row=0, column=0, sticky="e")

    item_name_entry = tk.Entry(reward_message, width=30)
    item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    item_type_label = tk.Label(reward_message, text="Item Type:")
    item_type_label.grid(row=1, column=0, sticky="e")

    item_type_entry = tk.Entry(reward_message, width=30)
    item_type_entry.grid(row=1, column=1, padx=10, pady=5)

    item_description_label = tk.Label(reward_message, text="Item Description:")
    item_description_label.grid(row=2, column=0, sticky="e")

    item_description_entry = tk.Text(reward_message, width=30, height=5)
    item_description_entry.grid(row=2, column=1, padx=10, pady=5)

    submit_button = tk.Button(reward_message, text="Submit",
                              command=lambda: submit_reward(reward_message,
                                                            item_name_entry.get().strip(),
                                                            item_type_entry.get().strip(),
                                                            item_description_entry.get("1.0", tk.END).strip()))
    submit_button.grid(row=3, columnspan=2, pady=10)

def submit_reward(reward_message, item_name, item_type, item_description):
    if item_name and item_type and item_description:
        reward_message.destroy()
        winner = random.choice(contestants)
        animate_winner_selection(winner, item_name, item_type, item_description)
        save_winner_to_file(winner, item_name, item_type, item_description)
    else:
        messagebox.showwarning("Missing Information", "Please fill in all the fields.")

def save_winner_to_file(winner, item_name, item_type, item_description):
    reward = {
        "winner": winner,
        "item_name": item_name,
        "item_type": item_type,
        "item_description": item_description
    }

    with open("rewards.txt", "a") as file:
        json.dump(reward, file)
        file.write("\n")

def show_winner_message(winner, item_name, item_type, item_description):
    message = f"Congratulations, {winner}!\n\nYou have won:\n\nItem Name: {item_name}\nItem Type: {item_type}\nItem Description: {item_description}"
    messagebox.showinfo("Winner Announcement", message)

def animate_winner_selection(winner, item_name, item_type, item_description):
    duration_per_name = 500  # Time in milliseconds to display each name
    total_duration = 10000  # Time in milliseconds for the total animation
    countdown_interval = 1000  # Time in milliseconds for countdown update

    countdown = 10

    def flash_name():
        nonlocal countdown
        if countdown == 0:
            animation_label.configure(text=winner)
            animation_label.configure(bg="light green")
            show_winner_message(winner, item_name, item_type, item_description)
        else:
            name = random.choice(contestants)
            animation_label.configure(text=name)
            animation_label.configure(bg="yellow")
            countdown -= 1
            countdown_label.configure(text=str(countdown))
            root.after(duration_per_name, flash_name)

    flash_name()

root = tk.Tk()
root.title("Contest Winner Picker")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

animation_label = tk.Label(root, text="Animation goes here", font=("Arial", 16), bg="white")
animation_label.pack(pady=20)

countdown_label = tk.Label(root, text="10", font=("Arial", 16))
countdown_label.pack()

pick_button = tk.Button(root, text="Pick Winner", command=pick_winner, bg="blue", fg="white")
pick_button.pack()

contestants_button = tk.Button(root, text="Show Contestants", command=show_contestants)
contestants_button.pack(pady=10)

winner_label = tk.Label(root, text="", font=("Arial", 16))
winner_label.pack(pady=20)

add_contestant_frame = tk.Frame(root)
add_contestant_frame.pack(pady=20)

contestant_entry = tk.Entry(add_contestant_frame, width=20, font=("Arial", 12))
contestant_entry.pack(side=tk.LEFT)

add_contestant_button = tk.Button(add_contestant_frame, text="Add Contestant", command=add_contestant)
add_contestant_button.pack(side=tk.LEFT, padx=10)

prize_frame = tk.Frame(root)
prize_frame.pack(pady=20)

browse_button = tk.Button(prize_frame, text="Browse Image", command=browse_image)
browse_button.pack()

prize_image = None

prize_image_label = tk.Label(prize_frame)
prize_image_label.pack()

load_contestants_from_file()

root.mainloop()

