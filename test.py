import tkinter as tk
from tkinter import Entry, Text, Scrollbar, Frame
from tkinter.messagebox import showerror, showinfo
import praw
import configparser
import subprocess
import json

def fetch_reddit_data(target_username):
    config = configparser.ConfigParser()
    config.read('config.ini')

    user_id = config['reddit']['user_id']
    api_key = config['reddit']['api_key']
    username = config['reddit']['username']
    password = config['reddit']['password']

    reddit = praw.Reddit(
        client_id=user_id,
        client_secret=api_key,
        username=username,
        password=password,
        user_agent='behavioral analysis model'
    )

    try:
        user = reddit.redditor(target_username)
        data = {'comments': []}

        for submission in user.submissions.new(limit=5):  # Adjust the limit as needed
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_data = {
                    'body': comment.body
                }
                data['comments'].append(comment_data)

        return data

    except praw.exceptions.RedditAPIException as e:
        if 'USER_DOESNT_EXIST' in str(e):
            showinfo("User Not Found", f"No such user '{target_username}' found on Reddit.")
        elif 'private' in str(e):
            showinfo("Private Account", f"The account '{target_username}' is private. Unable to fetch data.")
        else:
            raise Exception(f"Error: {e}")

def on_entry_click(event):
    if username_entry.get() == 'Enter Reddit Username':
        username_entry.delete(0, tk.END)
        username_entry.config(fg='black')  # Change text color to black

def on_submit():
    target_username = username_entry.get()
    if target_username == 'Enter Reddit Username':
        showinfo("Enter a Username", "Please enter a Reddit username.")
        return

    try:
        reddit_data = fetch_reddit_data(target_username)
        save_comments_to_json(reddit_data)
        display_reddit_data(reddit_data)
    except Exception as e:
        showerror("Error", f"An error occurred: {e}")

def on_analyze():
    try:
        # Run sentiment analysis program
        subprocess.run(["python", "sentimentanalysis.py"])
    except Exception as e:
        showerror("Error", f"An error occurred while running sentiment analysis: {e}")

def save_comments_to_json(reddit_data):
    with open('comments_data.json', 'w') as json_file:
        json.dump(reddit_data, json_file, indent=2)

def display_reddit_data(reddit_data):
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear previous results

    for comment_data in reddit_data['comments']:
        result_text.insert(tk.END, f"\nComment: {comment_data['body']}\n")
        result_text.insert(tk.END, "\n---\n")

    result_text.config(state=tk.DISABLED)  # Disable text widget for readonly

# Create the main window
window = tk.Tk()
window.title("Reddit Data Analyser")

# Check the platform and set the window state accordingly
if window.tk.call('tk', 'windowingsystem') == 'win32':
    window.state('zoomed')  # Windows platform
else:
    window.attributes('-zoomed', True)  # Linux platform

# Create and place widgets
username_entry = Entry(window, width=50, fg='grey')
username_entry.insert(0, 'Enter Reddit Username')
username_entry.bind('<FocusIn>', on_entry_click)
username_entry.pack(pady=10, padx=10, anchor='w')

submit_button = tk.Button(window, text="Fetch Comments", command=on_submit, width=20, height=2)
submit_button.pack(pady=10, padx=10, anchor='w')

analyze_button = tk.Button(window, text="Analyze", command=on_analyze, width=20, height=2)
analyze_button.pack(pady=10, padx=10, anchor='w')

# Create a frame to hold the text widget and scrollbars
frame = Frame(window)
frame.pack(pady=10, padx=10, anchor='w')

result_text = Text(frame, wrap=tk.WORD, width=int(window.winfo_screenwidth() * 0.9), height=int(window.winfo_screenheight() * 0.6))
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Vertical scrollbar
vertical_scrollbar = Scrollbar(frame, command=result_text.yview)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=vertical_scrollbar.set)

# Set text widget as read-only
result_text.config(state=tk.DISABLED)

# Start the Tkinter event loop
window.mainloop()
