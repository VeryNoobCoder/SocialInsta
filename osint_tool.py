import requests
from flask import Flask, redirect, request

app = Flask(__name__)

# Example function to download Instagram images and find metadata
def download_instagram_images(instagram_user):
    # In a real scenario, you would use Instagram's API or scraping techniques to download images.
    # This is a placeholder to indicate functionality.
    print(f"Downloading images for {instagram_user}...")

# Route to handle the masked URL
@app.route('/masked-url/<token>')
def masked_url(token):
    # Example mapping of tokens to real URLs
    ip_logging_urls = {
        "sampletoken1": "http://127.0.0.1:8080",  # Example HTTP URL
        "sampletoken2": "https://example.com/ip-logger",  # Example HTTPS URL
    }
    
    real_url = ip_logging_urls.get(token)
    
    if real_url:
        return redirect(real_url)
    else:
        return "Invalid URL", 404

# Main function to handle the social engineering OSINT tool
def social_engineering_osint_tool():
    print("Welcome to the Social Engineering OSINT Tool")
    
    # Get Instagram username from user
    instagram_user = input("Enter the Instagram username to gather OSINT data: ")
    
    # Download Instagram images
    download_instagram_images(instagram_user)
    
    # You could add more OSINT collection methods here as needed (e.g., email address lookup, etc.)
    
    # Mask URL functionality
    print("Generating Masked URL for IP logging...")
    token = input("Enter a unique token for the URL masking: ")
    
    # Redirect user to the masked URL
    masked_url = f"http://127.0.0.1:5000/masked-url/{token}"
    print(f"Send this masked URL to the target: {masked_url}")

# Start the Flask web server
if __name__ == '__main__':
    social_engineering_osint_tool()  # Run the OSINT tool to gather info and generate the masked URL
    app.run(debug=True)  # Start the web server
