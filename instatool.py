import requests
from bs4 import BeautifulSoup
import random
import string
import urllib.parse
import re

# Function to generate a random string for URL masking
def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Function to create a masked URL with a target IP logging link
def create_masked_url(ip_logging_url):
    # Validate the IP logging URL to ensure it's HTTPS
    if not ip_logging_url.startswith("https://"):
        print("[!] Please provide a valid HTTPS URL.")
        return None

    # Generate a random string for the masked URL path
    random_path = generate_random_string(12)

    # Encode the IP logging URL to make it part of the query parameter
    encoded_url = urllib.parse.quote(ip_logging_url)

    # Create the full masked URL
    masked_url = f"https://example.com/{random_path}?redirect={encoded_url}"

    return masked_url

# Function to get Instagram user data and images (OSINT)
def fetch_instagram_data(instagram_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send a request to the Instagram page
    response = requests.get(instagram_url, headers=headers)
    
    if response.status_code != 200:
        print(f"[!] Error: Unable to fetch Instagram page (Status code: {response.status_code})")
        return None

    # Parse the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the Instagram user data and image URLs
    try:
        # Extract username and bio
        username = soup.find("h1").text.strip()
        bio = soup.find("div", class_="-vDIg").span.text.strip()
        
        # Extract image URLs
        image_urls = []
        for img_tag in soup.find_all("img", attrs={"src": re.compile("^https://")}):
            image_urls.append(img_tag['src'])
        
        # Return the extracted data
        return {
            "username": username,
            "bio": bio,
            "image_urls": image_urls
        }

    except AttributeError:
        print("[!] Error: Could not extract user data from Instagram page.")
        return None

# Main program
if __name__ == "__main__":
    print("[*] Social Engineering OSINT Tool with URL Masking")
    
    # Ask user for the target Instagram URL
    instagram_url = input("[?] Enter the Instagram profile URL to gather information: ")
    
    # Fetch Instagram data
    instagram_data = fetch_instagram_data(instagram_url)
    
    if instagram_data:
        print(f"\n[*] Instagram Data for @{instagram_data['username']}:")
        print(f"Bio: {instagram_data['bio']}")
        print("Image URLs:")
        for img_url in instagram_data['image_urls']:
            print(f"- {img_url}")
    else:
        print("[!] Failed to retrieve Instagram data.")
    
    # Ask user for the IP logging URL (HTTPS format)
    ip_logging_url = input("\n[?] Enter the IP logging URL (HTTPS only): ")

    # Create the masked URL
    masked_url = create_masked_url(ip_logging_url)
    
    if masked_url:
        print(f"\n[+] Masked URL: {masked_url}")
