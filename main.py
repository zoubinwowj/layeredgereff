import requests
import json
import random
import time
import string
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Function to generate random wallet addresses
def generate_random_wallet_address():
    chars = string.hexdigits
    address = '0x' + ''.join(random.choice(chars) for _ in range(40)).lower()
    return address

# Check for referral code
ref_file = "ref.txt"
if os.path.exists(ref_file):
    with open(ref_file, "r") as file:
        referral_code = file.read().strip()
    print(Fore.LIGHTGREEN_EX + f"Referral code loaded from {ref_file}: {referral_code}")
else:
    referral_code = input(Fore.LIGHTCYAN_EX + "Enter referral code: ").strip()
    with open(ref_file, "w") as file:
        file.write(referral_code)
    print(Fore.LIGHTGREEN_EX + f"Referral code saved to {ref_file}.")

# Load proxy settings if enabled
proxy_file = "proxy.txt"
use_proxy = input(Fore.LIGHTCYAN_EX + "Do you want to use a proxy? (y/n): ").strip().lower()
proxies = None

if use_proxy == 'y':
    if os.path.exists(proxy_file):
        with open(proxy_file, "r") as file:
            proxy_address = file.read().strip()
        proxies = {
            "http": f"http://{proxy_address}",
            "https": f"https://{proxy_address}",
        }
        print(Fore.LIGHTGREEN_EX + f"Proxy loaded from {proxy_file}: {proxy_address}")
    else:
        print(Fore.LIGHTRED_EX + f"{proxy_file} not found. Please create the file and add your proxy address (IP:Port).")
        exit()

# Referral API URL
url = f"https://referral.layeredge.io/api/referral/register-wallet/{referral_code}"

# Headers for the request
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# Main loop for making requests
while True:
    wallet_address = generate_random_wallet_address()
    payload = json.dumps({"walletAddress": wallet_address})

    try:
        response = requests.post(url, headers=headers, data=payload, proxies=proxies)
        print(Fore.LIGHTGREEN_EX + f"[{response.status_code}] " + Fore.LIGHTWHITE_EX + f"Wallet: {wallet_address} | Response: {response.text}")
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error: {str(e)}")

    delay = random.randint(6, 10)
    print(Fore.LIGHTYELLOW_EX + f"Next request in {delay} seconds...")
    time.sleep(delay)