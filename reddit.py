import tkinter as tk
from tkinter import Entry, Text, Scrollbar, Frame, Toplevel
from tkinter.messagebox import showerror, showinfo
import praw
import configparser
from datetime import datetime
from sentimentanalysis import perform_sentiment_analysis, read_ngrams_from_file, read_words_from_file

# Read positive and negative words from text files
positive_unigrams = read_words_from_file('positive_words.txt')
negative_unigrams = read_words_from_file('negative_words.txt')

# Read positive and negative bigrams from text files
positive_bigrams = read_ngrams_from_file('positive_bigrams.txt')
negative_bigrams = read_ngrams_from_file('negative_bigrams.txt')

# Read positive and negative trigrams from text files
positive_trigrams = read_ngrams_from_file('positive_trigrams.txt')
negative_trigrams = read_ngrams_from_file('negative_trigrams.txt')

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
        data = {'submissions': []}

        for submission in user.submissions.new(limit=5):  # Adjust the limit as needed
            submission_data = {
                'title': submission.title,
                'created_utc': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'comments': []
            }

            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_data = {
                    'body': comment.body,
                    'created_utc': datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                }
                submission_data['comments'].append(comment_data)

            data['submissions'].append(submission_data)

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
        display_reddit_data(reddit_data)
    except Exception as e:
        showerror("Error", f"An error occurred: {e}")

def on_analyze():
    target_username = username_entry.get()
    if target_username == 'Enter Reddit Username':
        showinfo("Enter a Username", "Please enter a Reddit username.")
        return

    try:
        reddit_data = fetch_reddit_data(target_username)

        # Create a new window for analysis results
        analysis_window = Toplevel(window)
        analysis_window.title("Sentiment Analysis Results")

        # Set the size of the new window to fill the screen
        analysis_window.geometry("{0}x{1}+0+0".format(analysis_window.winfo_screenwidth(), analysis_window.winfo_screenheight()))

        # Create and place widgets
        result_text_analysis = Text(analysis_window, wrap=tk.WORD, width=int(analysis_window.winfo_screenwidth() * 0.9), height=int(analysis_window.winfo_screenheight() * 0.9))
        result_text_analysis.pack(pady=10, padx=10, anchor='w')

        # Iterate over comments and perform sentiment analysis
        for submission in reddit_data['submissions']:
            for comment in submission['comments']:
                comment_text = comment['body']
                sentiment = perform_sentiment_analysis(comment_text, positive_unigrams, negative_unigrams,
                                                       positive_bigrams, negative_bigrams,
                                                       positive_trigrams, negative_trigrams)
                comment['sentiment'] = sentiment

                # Display the analyzed data in the new window
                result_text_analysis.insert(tk.END, f"\nComment: {comment['body']}\n")
                result_text_analysis.insert(tk.END, f"Sentiment: {sentiment}\n")
                result_text_analysis.insert(tk.END, f"Posted on: {comment['created_utc']}\n")
                result_text_analysis.insert(tk.END, "\n---\n")

    except Exception as e:
        showerror("Error", f"An error occurred: {e}")

def display_reddit_data(reddit_data):
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear previous results

    for submission in reddit_data['submissions']:
        result_text.insert(tk.END, f"\nSubmission: {submission['title']}\n")
        result_text.insert(tk.END, f"Posted on: {submission['created_utc']}\n")

        for comment in submission['comments']:
            result_text.insert(tk.END, f"\nComment: {comment['body']}\n")
            result_text.insert(tk.END, f"Posted on: {comment['created_utc']}\n")
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

# Horizontal scrollbar
horizontal_scrollbar = Scrollbar(window, orient='horizontal', command=result_text.xview)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
result_text.config(xscrollcommand=horizontal_scrollbar.set)

# Set text widget as read-only
result_text.config(state=tk.DISABLED)

# Start the Tkinter event loop
window.mainloop()
