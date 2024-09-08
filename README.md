
```markdown
# Contest Winner Picker 🎉

## Overview
This application, built using Python's `tkinter` library, is designed to help organize and run contests where contestants are added, and winners are selected randomly. The app offers various functionalities such as managing contestant lists, blacklisting participants, displaying rewards, and allowing users to browse prize images.

---

## Features
- **Add Contestants**: Add contestants to the pool for the contest.
- **Pick Random Winner**: Select a random winner from the pool.
- **Blacklist Contestants**: Prevent certain participants from being chosen.
- **Display Contestants**: View the current list of contestants.
- **Save & Load Data**: Contestant data is saved to a file for persistence across sessions.
- **Prize Display**: Optionally display a prize image along with the winner's reward.
- **Reward Information**: The ability to provide details about the prize and show it to the winner.
- **Hidden Menus**: Administrative menus for advanced operations like blacklisting and viewing script details.

---

## Dependencies

Make sure you have the following libraries installed:

- `tkinter` (Python's standard GUI package)
- `Pillow` (for handling images)
  
You can install `Pillow` with the following command:

```bash
pip install Pillow
```

---

## How to Use

### 1. **Adding Contestants**
   - Type the name of the contestant into the entry field.
   - Click the "Add Contestant" button to add them to the list.
   - Contestants are saved in the `contestants.txt` file for future sessions.

### 2. **Viewing Contestants**
   - Click the "Show Contestants" button to display the current list in a pop-up window.
   
### 3. **Picking a Winner**
   - Ensure you have added at least one contestant.
   - Click the "Pick Winner" button to randomly select a winner.
   - The winner is announced with a countdown animation and a final display of the prize information.
   - Winners are logged to `rewards.txt` with details about the prize.

### 4. **Blacklisting Contestants**
   - Type "blacklist" into the contestant entry field and click "Add Contestant".
   - A hidden menu will open, where you can manage blacklisted contestants.

### 5. **Browsing Images for Prizes**
   - Click the "Browse Image" button to select an image from your system.
   - The selected image is displayed alongside the prize announcement.

### 6. **Reward Information**
   - When a winner is selected, you will be prompted to enter details about the prize, such as:
     - **Item Name**
     - **Item Type**
     - **Item Description**

### 7. **Script Information**
   - Type "scriptinfo" in the contestant entry field to view information like:
     - Number of lines of code
     - Number of contestants
     - Total rewards distributed

### 8. **Administrative Menus**
   - Hidden functionalities such as managing the blacklist and script info are triggered by typing specific keywords:
     - "blacklist" – opens the blacklist menu.
     - "scriptinfo" – shows detailed statistics about the script.
     - "instructions" – displays a detailed instruction guide.

---

## Code Breakdown

### 1. **Main Components**
   
- `contestants`: A list that holds all the contestants.
- `blacklist`: A list that holds contestants who are not eligible to win.

### 2. **Functions**

#### `pick_winner()`
This function selects a random contestant (excluding blacklisted ones) as the winner. It prompts a reward information window before proceeding to the winner announcement.

#### `add_contestant()`
Adds a new contestant from the entry field. If the entry is blank, it shows a warning. It also updates the contestant list file (`contestants.txt`).

#### `save_contestants_to_file()` & `load_contestants_from_file()`
These functions handle saving and loading the list of contestants to/from a text file, ensuring the contestant list is persistent across sessions.

#### `show_reward_message()`
Prompts a window for the user to enter details about the prize the winner will receive. These details are then logged along with the winner’s name.

#### `browse_image()` & `load_image()`
Allows the user to browse and select an image for the prize. The image is resized to fit and displayed in a pop-up window.

#### `animate_winner_selection()`
Provides a countdown animation when selecting a winner. A random contestant's name is displayed for a short period, adding suspense to the final winner announcement.

#### `open_hidden_menu()`
A special function that detects specific keywords in the contestant entry to trigger hidden admin menus for managing the blacklist or displaying script information.

### 3. **Admin Menus**

#### Blacklist Menu
Manages blacklisting and unblacklisting contestants via a scrollable text box where names can be selected.

#### Script Information Menu
Shows statistics like:
- Number of lines of code
- Number of contestants added
- Rewards distributed

#### Instructions Menu
Displays the instructions on how to use the script, including hidden functionalities.

---

## File Structure

- `contestants.txt`: Stores the list of contestants.
- `rewards.txt`: Logs the winners and the details of the prizes they have won.

---

## Customization

- **Animation Timing**: Modify `duration_per_name` and `total_duration` in the `animate_winner_selection()` function to control the length of the countdown.
- **File Names**: You can change the file paths for contestants and rewards if needed.
- **Hidden Menus**: Add your own hidden functionality by extending the `open_hidden_menu()` function.

---

## Conclusion

This script provides a simple and interactive way to manage contests and giveaways, allowing administrators to manage contestants, blacklist users, and log results. The interface is intuitive, and the hidden menus offer advanced functionality for those with administrative privileges.
```
