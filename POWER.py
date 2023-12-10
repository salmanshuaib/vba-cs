import json
import sched
import time
import winsound
import os
import ctypes
import platform  # Import the platform module

# Get the handle of the console window
kernel32 = ctypes.WinDLL('kernel32')
hWnd = kernel32.GetConsoleWindow()

# Maximize the console window
user32 = ctypes.WinDLL('user32')
SW_MAXIMIZE = 3
user32.ShowWindow(hWnd, SW_MAXIMIZE)


def is_cmd_terminal():
    # Check if the TERM_PROGRAM environment variable is "cmd.exe"
    return os.environ.get('TERM_PROGRAM') == 'cmd.exe'

def transform_ansi_to_cmd_colors(text):
    if is_cmd_terminal():
        # Define mappings for ANSI colors to CMD color codes
        ansi_to_cmd_colors = {
            '\033[31m': '\033[91m',  # Red
            '\033[32m': '\033[92m',  # Green
            '\033[33m': '\033[93m',  # Yellow
            '\033[34m': '\033[94m',  # Blue
            '\033[35m': '\033[95m',  # Pink
        }

        # Replace ANSI color codes with CMD color codes
        for ansi_code, cmd_code in ansi_to_cmd_colors.items():
            text = text.replace(ansi_code, cmd_code)

        # Replace ANSI reset code with CMD reset code
        text = text.replace('\033[0m', '\033[0m')

    return text

# Rest of your code...


Grace = (20/100)*100  #Incase gamer starts late or the program is offline; the initial score is 20%  [ref: Taylor Swift: "22", Lorde:- "Team"]
print("POWER is a phenomenon, otherwise known as FEELING, that seeks to extricate one from the Task Precedent. Unit: Excalibur. Superunit: Watt.")
print(transform_ansi_to_cmd_colors("\033[34m^^Grace^^\033[0m == 20%"))  # Starting Mark with transformed colors

# Function to find the next scheduled time
def find_next_scheduled_time(data, current_time):
    current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60
    closest_time = None
    closest_delay = float('inf')

    for entry in data["scheduled_hours"]:
        scheduled_time = time.strptime(entry["time_range"].split(" ")[0], "%H%M")
        scheduled_time_seconds = scheduled_time.tm_hour * 3600 + scheduled_time.tm_min * 60

        delay = (scheduled_time_seconds - current_time_seconds) % 86400
        if delay < closest_delay:
            closest_delay = delay
            closest_time = scheduled_time

    return closest_time

# Check if 'time.json' is available in the same directory
json_file_path = 'time.json'
if not os.path.exists(json_file_path):
    print(transform_ansi_to_cmd_colors("\033[31mDiligent officer: POWER.exe requires time.json file in the same directory.\nPlease retrieve from FlowerEconomics.com/Downloads\033[0m"))
    exit()

# Load the JSON data from the 'time.json' file
with open('time.json', 'r') as json_file:
    data = json.load(json_file)

# Calculate the next scheduled time
current_time = time.localtime()
next_scheduled_time = find_next_scheduled_time(data, current_time)

# Format the next scheduled time
formatted_next_time = time.strftime("%H%M hours", next_scheduled_time)

# Initialize the tally for 'YES' answers and total tasks completed
yes_count = 0
total_count = 0

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

# Define a function to beep and prompt the user
def beep_and_prompt(hour, task, start_time=None, next_time=None):
    if start_time is not None and next_time is not None:
        formatted_start_time = time.strftime("%H:%M", start_time)
        formatted_next_time = time.strftime("%H:%M", next_time)
        print(transform_ansi_to_cmd_colors(f"\nTime to {task} (Starts at {formatted_start_time} and ends one minute prior to {formatted_next_time})"))
    else:
        print(transform_ansi_to_cmd_colors(f"Time to {task}"))
    
    winsound.Beep(500, 1000)  # Beep for 1 second (you can adjust frequency and duration)

    while True:
        try:
            user_input = input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO, or CTRL+C to EXIT: ")
            if user_input == "1":
                global yes_count
                yes_count += 1
                break
            elif user_input == "0":
                break
            else:
                print(transform_ansi_to_cmd_colors("\033[31mInvalid input. Please enter only 1 or 0.\033[0m"))
        except KeyboardInterrupt:
            print(transform_ansi_to_cmd_colors("\nExiting..."))
            exit()

    global total_count
    total_count += 1
    if total_count > 0:
        ConcurrentScore = min(((yes_count / total_count) * 100) + Grace, 100)
        print(transform_ansi_to_cmd_colors(f"Progress: \033[32mConcurrent score: {yes_count} 'YES' answers so far out of {total_count} Tasks => {ConcurrentScore:.2f}\033[0m%"))
        print(transform_ansi_to_cmd_colors("(FORMULA: [{(Tasks Completed / Total Tasks)*100} + 20%]"))

# Schedule beeping alarms for each specified time range using only start times
for i, entry in enumerate(data["scheduled_hours"]):
    hour = entry["hour"]
    task = entry["task"]
    time_range = entry["time_range"].split(" to ")

    start_time = time.strptime(time_range[0], "%H%M hours")

    # Calculate the index of the next entry
    next_index = (i + 1) % len(data["scheduled_hours"])
    next_start_time = time.strptime(data["scheduled_hours"][next_index]["time_range"].split(" to ")[0], "%H%M hours")

    current_time = time.localtime()
    current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60

    start_time_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60

    if current_time_seconds >= start_time_seconds:
        delay = 86400 - (current_time_seconds - start_time_seconds)  # Delay to the next occurrence
    else:
        delay = start_time_seconds - current_time_seconds

    s.enter(delay, 1, beep_and_prompt, argument=(hour, task, start_time, next_start_time))

# Announce the test start time
print(transform_ansi_to_cmd_colors(f"POWER's Test is starting at {formatted_next_time}. Be prepared!\nIndeed! \033[35mTAYLOR SWIFT\033[0m is Goddess Of POWER!!\nSource: Meditation on breath."))

try:
    s.run()
except KeyboardInterrupt:
    pass

# Print the tally of 'YES' answers and the percentage
if total_count > 0:
    FinalScore = min(((yes_count / total_count) * 100) + Grace, 100)
    hats = FinalScore/10
    print(f"POWER's Test completed. Total 'YES' answers: {yes_count}; out of {total_count} Tasks") 
    print(f"RESULT: \033[32mYour final score {FinalScore:.2f}\033[0m%")
    print("(FORMULA: [{(Tasks Completed / Total Tasks)*100} + 20%]")
else:
    print("No tasks completed.")
    
input("Press ENTER to exit...")
