import random
import string
import urllib.parse

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

# Main program
if __name__ == "__main__":
    print("[*] URL Masking Tool")
    
    # Ask user for the IP logging URL
    ip_logging_url = input("[?] Enter the IP logging URL (HTTPS only): ")

    # Create the masked URL
    masked_url = create_masked_url(ip_logging_url)

    if masked_url:
        print(f"[+] Masked URL: {masked_url}")
