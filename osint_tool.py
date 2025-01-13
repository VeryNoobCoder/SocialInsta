import requests
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from flask import Flask, request

# 1. Scrape Instagram Pictures
def download_instagram_pictures(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Failed to access Instagram profile. HTTP {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all("script", type="text/javascript")
        for script in scripts:
            if "display_url" in script.string:
                # Extract image URLs
                start = script.string.find('display_url') + len('display_url":"')
                end = script.string.find('","', start)
                img_url = script.string[start:end].replace("\\u0026", "&")
                print(f"[+] Found Image: {img_url}")
                
                # Download the image
                img_data = requests.get(img_url).content
                filename = f"{username}_image_{img_url.split('/')[-1]}"
                with open(filename, 'wb') as file:
                    file.write(img_data)
                print(f"[+] Image saved: {filename}")
    except Exception as e:
        print(f"[!] Error scraping Instagram: {str(e)}")

# 2. Extract Metadata (EXIF)
def extract_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if not exif_data:
            print(f"[!] No EXIF data found in {image_path}")
            return
        
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_data = {}
                for key in value:
                    gps_tag = GPSTAGS.get(key, key)
                    gps_data[gps_tag] = value[key]
                metadata["GPSInfo"] = gps_data
            else:
                metadata[tag] = value
        
        print(f"[+] Metadata for {image_path}: {metadata}")
        return metadata
    except Exception as e:
        print(f"[!] Failed to extract EXIF data: {str(e)}")

# 3. Reverse Geolocation (if GPS exists)
def reverse_geocode(lat, lon):
    try:
        api_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(api_url)
        if response.status_code == 200:
            location = response.json().get('display_name', 'Unknown Location')
            print(f"[+] Location: {location}")
        else:
            print(f"[!] Reverse geocoding failed. HTTP {response.status_code}")
    except Exception as e:
        print(f"[!] Error during reverse geolocation: {str(e)}")

# 4. IP Logging Tool
def ip_logger():
    app = Flask(__name__)
    log_file = "ip_logs.txt"

    @app.route('/')
    def home():
        visitor_ip = request.remote_addr
        print(f"[+] Visitor IP Logged: {visitor_ip}")
        with open(log_file, 'a') as file:
            file.write(f"IP: {visitor_ip}\n")
        return "IP Logged Successfully."

    app.run(host="0.0.0.0", port=8080)

# Main Function
if __name__ == "__main__":
    print("[*] Starting OSINT tool...")

    # Step 1: Instagram username
    instagram_user = input("[?] Enter Instagram username: ")
    download_instagram_pictures(instagram_user)

    # Step 2: Analyze saved images
    image_files = [f for f in os.listdir() if f.startswith(instagram_user)]
    for image in image_files:
        exif_data = extract_exif_data(image)
        if exif_data and "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            lat = gps_info.get('GPSLatitude', None)
            lon = gps_info.get('GPSLongitude', None)
            if lat and lon:
                reverse_geocode(lat, lon)

    # Step 3: Start IP logger
    print("[*] Starting IP logger. Open your browser and share the link:")
    ip_logger()
