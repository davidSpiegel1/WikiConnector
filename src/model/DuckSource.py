import requests
import tkinter as tk
from bs4 import BeautifulSoup
from tkhtmlview import HTMLLabel
from urllib.parse import quote

def fetch_duckduckgo_html(query):
    # URL encode the query
    query = quote(query)
    # DuckDuckGo search URL
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching data:", response.status_code)
        return None

def display_results():
    # Fetch the query from the input
    query = entry.get()
    # Fetch HTML data from DuckDuckGo
    html_data = fetch_duckduckgo_html(query)
    
    if html_data:
        soup = BeautifulSoup(html_data, 'html.parser')
        
        # Generate HTML content for display
        html_content = f"<h2>Results for: {query}</h2>"
        
        # Loop through search results
        for result in soup.select(".result__body"):
            title = result.select_one(".result__title a")
            snippet = result.select_one(".result__snippet")
            image = result.select_one(".result__icon img")

            # Add title with link
            if title and title['href']:
                html_content += f"<h3><a href='{title['href']}' target='_blank'>{title.get_text()}</a></h3>"
            
            # Add snippet
            if snippet:
                html_content += f"<p>{snippet.get_text()}</p>"

            # Add image if available
            if image and image['src']:
                html_content += f"<img src='{image['src']}' alt='Image' style='max-width:200px;'><br>"

        # Set the HTML content to display
        html_label.set_html(html_content)
    else:
        html_label.set_html("<p>Error fetching data. Please try again.</p>")

# Setup Tkinter GUI
root = tk.Tk()
root.title("DuckDuckGo Search API (HTML View)")
root.geometry("600x800")

# Input for search query
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Button to trigger search
search_button = tk.Button(root, text="Search", command=display_results)
search_button.pack(pady=10)

# HTML display for showing results
html_label = HTMLLabel(root, html="")
html_label.pack(pady=10, fill="both", expand=True)

root.mainloop()

