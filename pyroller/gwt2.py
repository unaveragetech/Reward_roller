import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
import random
import json
from PIL import ImageTk, Image

contestants = []
blacklist = []

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


def show_image_popup():
    image_popup = tk.Toplevel(root)
    image_popup.title("Prize Image")

    prize_image_label = tk.Label(image_popup, image=prize_image)
    prize_image_label.pack()

def load_image(filepath):
    global prize_image
    prize_image = Image.open(filepath)
    prize_image.thumbnail((400, 400))  
    prize_image = ImageTk.PhotoImage(prize_image)
    show_image_popup()  


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
        winner = random.choice([c for c in contestants if c not in blacklist])
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
            name = random.choice([c for c in contestants if c not in blacklist])
            animation_label.configure(text=name)
            animation_label.configure(bg="yellow")
            countdown -= 1
            countdown_label.configure(text=str(countdown))
            root.after(duration_per_name, flash_name)

    flash_name()

def open_hidden_menu():
    contestant = contestant_entry.get().strip().lower()
    if contestant == "blacklist":
        open_blacklist_menu()
    elif contestant == "scriptinfo":
        open_script_info_menu()
    elif contestant == "instructions":
        open_instructions_menu()
    else:
        add_contestant()

def open_blacklist_menu():
    hidden_menu = tk.Toplevel(root)
    hidden_menu.title("Blacklist Menu")

    scroll_text = scrolledtext.ScrolledText(hidden_menu, width=60, height=30)
    scroll_text.pack()

    for contestant in contestants:
        scroll_text.insert(tk.END, contestant + "\n")

    def blacklist_selected():
        selected_text = scroll_text.get("sel.first", "sel.last")
        selected_names = selected_text.strip().split("\n")
        for name in selected_names:
            if name not in blacklist:
                blacklist.append(name)
        messagebox.showinfo("Blacklist", "Selected contestants have been blacklisted.")

    def unblacklist_names():
        unblacklist_menu = tk.Toplevel(hidden_menu)
        unblacklist_menu.title("Unblacklist Menu")

        unblacklist_text = scrolledtext.ScrolledText(unblacklist_menu, width=30, height=10)
        unblacklist_text.pack()

        for name in blacklist:
            unblacklist_text.insert(tk.END, name + "\n")

        def unblacklist_selected():
            selected_text = unblacklist_text.get("sel.first", "sel.last")
            selected_names = selected_text.strip().split("\n")
            for name in selected_names:
                if name in blacklist:
                    blacklist.remove(name)
            messagebox.showinfo("Unblacklist", "Selected contestants have been unblacklisted.")
            unblacklist_menu.destroy()

        unblacklist_button = tk.Button(unblacklist_menu, text="Unblacklist", command=unblacklist_selected)
        unblacklist_button.pack()

    blacklist_button = tk.Button(hidden_menu, text="Blacklist", command=blacklist_selected)
    blacklist_button.pack()

    unblacklist_button = tk.Button(hidden_menu, text="Unblacklist", command=unblacklist_names)
    unblacklist_button.pack()

def open_script_info_menu():
    hidden_menu = tk.Toplevel(root)
    hidden_menu.title("Script Information Menu")

    info_text = f"Number of Lines of Code: {count_lines_of_code()}\n"
    info_text += f"Number of Contestants: {len(contestants)}\n"
    info_text += f"Rewards So Far: {count_rewards()}"

    info_label = tk.Label(hidden_menu, text=info_text)
    info_label.pack()

    root.wait_window(hidden_menu)

def open_instructions_menu():
    instructions = """
    Script Operation Instructions:
    
    1. Adding Contestants:
       - Enter the name of the contestant in the contestant entry field.
       - Click 'Add Contestant' button to add the contestant to the pool.
    
    2. Picking a Winner:
       - Ensure that at least one contestant is added.
       - Click the 'Pick Winner' button to randomly select a winner.
    
    3. Viewing Contestants:
       - Click the 'Show Contestants' button to display the list of current contestants.
    
    4. Blacklisting/Unblacklisting:
       - To blacklist a contestant, type 'blacklist' as a contestant and click 'Add Contestant'.
       - To unblacklist a contestant, open the hidden menu and use the 'Unblacklist' button.
    
    5. Script Information:
       - To view information about the script, type 'scriptinfo' as a contestant and click 'Add Contestant'.
       
    6. General informaition 
       -To see all general information about the script, type 'information' as a contestant and click 'Add Contestant'.
       
    7. Tldr
       -This script was made by Beelzebub4883 for doing random givaways on diffrent platforms'.  
    
    Note: Only the administrator should operate the script and have access to the hidden menu options.
    """

    lines = instructions.strip().split('\n')
    max_line_length = max(len(line) for line in lines)

    instructions_popup = tk.Toplevel(root)
    instructions_popup.title("Instructions")

    instructions_text = tk.Text(
        instructions_popup,
        width=max_line_length + 4,  # Adding extra space on both sides of the text
        height=35
    )
    instructions_text.insert(tk.END, instructions)
    instructions_text.config(state=tk.DISABLED)
    instructions_text.pack()

    root.wait_window(instructions_popup)

def count_lines_of_code():
    line_count = 0
    with open(__file__, "r") as file:
        for line in file:
            if line.strip():
                line_count += 1
    return line_count

def count_rewards():
    try:
        with open("rewards.txt", "r") as file:
            rewards = file.readlines()
            return len(rewards)
    except FileNotFoundError:
        return 0


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

add_contestant_button = tk.Button(add_contestant_frame, text="Add Contestant", command=open_hidden_menu)
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