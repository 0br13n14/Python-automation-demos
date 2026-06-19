#importing required libraries
import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import logging
from urllib.parse import urlparse


#####################

def input_handler(url):
    
    if not isinstance(url, str):    # Checking if the inputed url is a string 
        raise TypeError ("URL must be a string")

    # Check if empty after stripping → raise ValueError
    if not url or not url.strip():
        raise ValueError("URL cannot be empty or whitespace")

    # Normalize the URL
    url = url.strip()

    #Check if starts with http:// or https:// 
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("URL must start with http:// or https://")

    print(f"Valid URL: {url}")
    return url

 
################

def fetch(url, retries=3, delay=2):

    # Define the headers dictionary with a realistic User-Agent
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

    for attempt in range(retries):

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200: 
                print("Success!")
                return response

            else:
                # Unexpected status code
                print(f"Unexpected status code: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(delay)

    raise ConnectionError (f"failed to fetch {url} after {retries} attempts")


######################


def load(response):# turn raw response into navigable beautifulsoup object

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    print("HTML loaded successfully")
    return soup


####################


def parse(soup):
    elements = soup.find_all("div", class_="quote")  # this creates a list
    
    if not elements:
        print("Warning: no elements found")
        return []

    number = len(elements)

    print(f"Found {number} elements")

    return elements

###########################


def extract(element):
    # FIND inside element:
    #   text   = span with class "text"   → get its text content#
    text = element.find("span", class_="text").get_text()

    #   author = small with class "author" → get its text content
    author = element.find("small", class_="author").get_text()

    #   tags   = all anchor tags inside div class "tags"
    #             → get text of each, join into comma-separated string
    tag_elements = element.find("div", class_="tags").find_all("a", class_="tag")
    tags = ", ".join([tag.get_text() for tag in tag_elements])
    
    return {"text": text, "author": author, "tags": tags}


############################
def clean(raw_dict):     
    text = raw_dict.get("text", None)
    author = raw_dict.get("author", None)
    tags = raw_dict.get("tags", "")     # Tags being empty is normal and valid. None implies something went wrong. Empty string "" just means no tags

    """
    raw_dict.get("text", None) means:
    
    Look inside raw_dict for the key "text"
    IF it exists → return its value
    IF it doesn't exist → return None (the default)
    """
    
    # using .replace('\u201c', '').replace('\u201d', '').strip() strips outer quotes ("")
    if text:
        text = text.replace('\u201c', '').replace('\u201d', '').strip()
    else:
        text = None

    if author:
        author = author.replace('\u201c', '').replace('\u201d', '').strip()
    else:
        author = None
    
    if tags:
        tags = tags.replace('\u201c', '').replace('\u201d', '').strip()
    else:
        tags = ""

    return {"text": text, "author": author , "tags": tags}     # RETURN: cleaned dict

#############################

def paginate(soup, base_url):
    li_element = soup.find("li", class_="next")

    if not li_element:
        print("Reached last page")
        return None
    
    # getting the href from an anchor tag:
    anchor = li_element.find("a")
    href = anchor["href"]

    full_url = base_url + href

    print(f"Next page: {full_url}")
    return full_url
    

###############################
# Saving the data to a file

def save(data, filename):
    if not data:
        print("Warning: nothing to save")
        return      # Adding return otherwise the function continues even when data is empty

    # Get the folder where file lives
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Build path to any file in the same folder
    filepath = os.path.join(SCRIPT_DIR, filename)

    #  Checking if file exists
    file_exists = os.path.isfile(filepath)

    with open(filepath, "a" if file_exists else "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "author", "tags"]) # csv.DictWriter needs arguments and a variable
         
        # Writing headers only when file is new    
        if not file_exists:       
            writer.writeheader() # Only runs if file is new

        writer.writerows(data) # ALWAYS RUNS, new file or existing 

    print(f"Saved {len(data)} records to {filename}")
    return None
    
##############################


def run(start_url):

    # clean_url = fixed starting point, never touched again.
    # url = moving cursor that walks through pages until the end.

    # 1. Validate url 
    clean_url = input_handler(start_url)

    # 2. Initialise
    url = clean_url

    all_data = []

    parsed = urlparse(clean_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    
    while url:
        response = fetch(url)
        soup = load(response)
        elements = parse(soup)

        for element in elements:
            raw = extract(element)
            cleaned = clean(raw)
            all_data.append(cleaned)
        
        print(f"Page scraped: {len(elements)} records collected") 

        url = paginate(soup, base_url)
        
        time.sleep(2) 

    save(all_data, "quotes.csv")
    print(f"Scraper complete. Total records: {len(all_data)}")

# ENTRY POINT 

if __name__ == "__main__":
    start = input("Provide a valid url: ").strip()
    run(start)


###############################
# https://quotes.toscrape.com
