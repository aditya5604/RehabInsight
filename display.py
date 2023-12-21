import tkinter as tk
from PIL import Image, ImageTk
import cv2
import subprocess

def sns_analysis():
    selected_text.set("SNS Analysis")
    update_result_label()
    show_sns_options()

def live_video_analysis():
    selected_text.set("Live Video Analysis")
    update_result_label()
    show_live_video_feed()

def update_result_label():
    result_label.config(textvariable=selected_text, font=("Helvetica", int(screen_width * 0.03)), bg="white", fg="black", padx=10, pady=5, relief=tk.GROOVE)

def show_sns_options():
    # Create a new window for SNS options
    sns_options_window = tk.Toplevel(window)
    sns_options_window.title("SNS Analysis Options")

    # Get the screen width and height for the new window
    sns_options_width = sns_options_window.winfo_screenwidth()
    sns_options_height = sns_options_window.winfo_screenheight()

    # Set the window size to fit the screen
    sns_options_window.geometry(f"{sns_options_width}x{sns_options_height}")

    # Create a frame for the design at the top
    design_frame = tk.Frame(sns_options_window, bg="#3498db", height=50)
    design_frame.pack(fill=tk.X)

    # Create a label for the heading
    selected_website = selected_text.get().replace(" Analysis", "")  # Get selected website without " Analysis"
    heading_label = tk.Label(design_frame, text=f"SNS Analysis Options on {selected_website}", font=("Helvetica", 18), bg="#3498db", fg="white")
    heading_label.pack(pady=10)

    # Create buttons for each social media website
    sns_websites = ["Facebook", "Instagram", "Reddit", "Snapchat", "Twitter"]

    # Calculate the spacing between buttons
    spacing = (sns_options_height - 50 - (len(sns_websites) * button_height)) // (len(sns_websites) + 1)

    for i, website in enumerate(sns_websites):
        sns_button = tk.Button(sns_options_window, text=website, command=lambda w=website: analyze_sns(w, sns_options_window), width=button_width, height=button_height, font=("Helvetica", 16))
        sns_button.place(relx=0.5, rely=50 / sns_options_height + (i + 1) * spacing / sns_options_height, anchor=tk.CENTER)

def analyze_sns(website, parent_window):
    if website.lower() == "reddit":
        parent_window.destroy()
        subprocess.run(["python", "reddit.py"])  # Replace "python" with your Python interpreter if needed
    else:
        # Create a new window for SNS analysis result
        sns_result_window = tk.Toplevel(window)
        sns_result_window.title(f"{website} Analysis")

        # Get the screen width and height for the new window
        sns_result_width = sns_result_window.winfo_screenwidth()
        sns_result_height = sns_result_window.winfo_screenheight()

        # Set the window size to fit the screen
        sns_result_window.geometry(f"{sns_result_width}x{sns_result_height}")

        # Create a frame for the design at the top
        design_frame = tk.Frame(sns_result_window, bg="#3498db", height=50)
        design_frame.pack(fill=tk.X)

        # Create a label for the heading
        heading_label = tk.Label(design_frame, text=f"{website} Analysis", font=("Helvetica", 30), bg="#3498db", fg="white")
        heading_label.pack(pady=10)

        # Create entry widget for username with watermark
        username_entry = tk.Entry(sns_result_window, font=("Helvetica", 20), width=40, fg="grey")
        username_entry.insert(0, f"Username on {website}")  # Set watermark text
        username_entry.bind("<FocusIn>", lambda event: on_entry_click(username_entry, f"Username on {website}"))
        username_entry.bind("<FocusOut>", lambda event: on_entry_leave(username_entry, f"Username on {website}"))
        username_entry.pack(pady=15)

        # Create confirm button
        confirm_button = tk.Button(sns_result_window, text="Confirm", command=lambda: process_analysis(website, username_entry.get(), sns_result_window), width=15, height=3, font=("Helvetica", 16))
        confirm_button.pack(pady=10)

        # Create error label
        error_label = tk.Label(sns_result_window, text="", fg="red")
        error_label.pack(pady=5)

def on_entry_click(entry, watermark_text):
    if entry.get() == watermark_text:
        entry.delete(0, "end")  # delete all the text in the entry
        entry.config(fg="black")

def on_entry_leave(entry, watermark_text):
    if entry.get() == "":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, watermark_text)
        entry.config(fg="grey")

def process_analysis(website, username, parent_window):
    if username == "" or username.startswith("Username on "):
        print("No username given")
    else:
        if website.lower() == "reddit":
            # Close the current window
            parent_window.destroy()

            # Open a new window for Reddit analysis
            reddit_analysis_window = tk.Toplevel(window)
            reddit_analysis_window.title(f"Reddit Analysis of u/{username}")

            # Get the screen width and height for the new window
            reddit_analysis_width = reddit_analysis_window.winfo_screenwidth()
            reddit_analysis_height = reddit_analysis_window.winfo_screenheight()

            # Set the window size to fit the screen
            reddit_analysis_window.geometry(f"{reddit_analysis_width}x{reddit_analysis_height}")

            # Create a frame for the design at the top
            design_frame = tk.Frame(reddit_analysis_window, bg="#3498db", height=50)
            design_frame.pack(fill=tk.X)

            # Create a label for the heading, spanning the complete width
            heading_label = tk.Label(design_frame, text=f"Reddit Analysis of u/{username}", font=("Helvetica", 30), bg="#3498db", fg="white")
            heading_label.pack(fill=tk.X, pady=10)

        else:
            # Add your analysis logic for other social media platforms
            print(f"Analyzing {website} for user {username}")

def show_live_video_feed():
    # Create a new window for live video feed
    live_video_window = tk.Toplevel(window)
    live_video_window.title("Live Video Feed")

    # Get the screen width and height for the new window
    live_video_width = live_video_window.winfo_screenwidth()
    live_video_height = live_video_window.winfo_screenheight()

    # Set the window size to fit the screen
    live_video_window.geometry(f"{live_video_width}x{live_video_height}")

    # Create a canvas to display the live video feed
    canvas = tk.Canvas(live_video_window, width=live_video_width, height=live_video_height, bg="black")
    canvas.pack()

    # Open the video capture
    cap = cv2.VideoCapture(0)

    def update_video_feed():
        ret, frame = cap.read()
        if ret:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Resize the frame to fit the window
            frame = cv2.resize(frame, (live_video_width, live_video_height))

            # Convert the OpenCV frame to a PIL image
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)

            # Update the canvas with the new image
            canvas.img = img  # To prevent garbage collection
            canvas.create_image(0, 0, anchor=tk.NW, image=img)

            # Repeat the update after a delay
            canvas.after(5, update_video_feed)

    # Start updating the video feed
    update_video_feed()

# Create the main window
window = tk.Tk()
window.title("Analysis Options")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to fit the screen
window.geometry(f"{screen_width}x{screen_height}")

# Create a label to display the selected option
selected_text = tk.StringVar()
result_label = tk.Label(window, textvariable=selected_text, font=("Helvetica", int(screen_width * 0.03)), bg="white", fg="black", padx=10, pady=5, relief=tk.GROOVE)
result_label.pack(pady=20)

# Create buttons
button_width = 30
button_height = 5

# Center both buttons more to the right with increased spacing between them
sns_button = tk.Button(window, text="SNS Analysis", command=sns_analysis, width=20, height=5, font=("Helvetica", 16))
sns_button.pack(side=tk.LEFT, padx=(screen_width // 3, 20))

live_video_button = tk.Button(window, text="Video Analysis", command=live_video_analysis, width=20, height=5, font=("Helvetica", 16))
live_video_button.pack(side=tk.LEFT, padx=(20, screen_width // 3))

# Start the Tkinter event loop
window.mainloop()
