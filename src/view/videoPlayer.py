import tkinter as tk
from tkinter import messagebox
import requests
import html

import subprocess
import sys
try:
    import webview
    print("webview is already installed")
except:
    print("webview not found. Using pip to install")
    subprocess.check_call([sys.executable,"-m","pip","install","pywebview"])
    import webview

def get_youtube_oembed(video_url):
    oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
    
    try:
        # Send a GET request to the oEmbed endpoint
        response = requests.get(oembed_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        video_data = response.json()
        
        # Decode HTML entities
        embed_html = html.unescape(video_data['html'])
        return embed_html

    except requests.RequestException as e:
        print("Error fetching oEmbed data:", e)
        return None

"""def get_tumblr_oembed(video_url):
    oembed_url = f"https://www.tumblr.com/oembed/1.0?url={video_url}"

    try:
        response = requests.get(oembed_url)
        response.raise_for_status()

        video_data = response.json()
        
        embed_html = html.unescape(video_data['html'])
        return embed_html
    except requests.RequestException as e:
        print("Error fetching oEmbed data:",e)
        return None"""


def get_dailyMotion_oembed(video_url):
    oembed_url = f"https://www.dailymotion.com/services/oembed?url={video_url}&format=json"

    try:
        # Send get request
        response = requests.get(oembed_url)
        response.raise_for_status()

        video_data = response.json()

        embed_html = html.unescape(video_data['html'])
        return embed_html
    except requests.RequestException as e:
        print("Error fetching oEmbed data:",e)
        return None

def load_video(htmlType):
    """Load the YouTube video in a PyWebview window."""
    video_url = url_entry.get()  # Get the URL from the user input
    embed_html = None
    if video_url:
        if htmlType == "Y":
            embed_html = get_youtube_oembed(video_url)
        elif htmlType == "DM":
            embed_html = get_dailyMotion_oembed(video_url)
        elif htmlType == "T":
            embed_html = get_tumblr_oembed(video_url)
        if embed_html:
            # Extract the src from the embed HTML
            start_index = embed_html.find('src="') + 5
            end_index = embed_html.find('"', start_index)
            video_src = embed_html[start_index:end_index]

            # Open the video in a web view
            wv = webview.create_window('Video', video_src)
            webview.start()  # Start the PyWebview window
            #return wv
        else:
            messagebox.showerror("Error", "Failed to load video. Please check the URL.")
    else:
        messagebox.showerror("Error", "Please enter a YouTube URL.")

# Create the main application window
root = tk.Tk()
root.title("YouTube Video Loader")

# Create a label and entry to input the YouTube URL
url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create a button to load the video
n = len(sys.argv)
finalStr = ""
for word in range(1,n-1):
    finalStr += sys.argv[word]

finalStr += sys.argv[n-1]
print("The final string: ",finalStr)
load_button = tk.Button(root, text="Load Video", command= lambda e = finalStr: load_video(e))
load_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

