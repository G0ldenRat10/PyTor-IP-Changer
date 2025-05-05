import os
import sys
import time
import subprocess
import random
import re
import socket
import requests

def display_ASCII_intro():

    art = """
      
    ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░               
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓███████▓▒░ ░▒▓██████▓▒░   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░                 
    ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░                     
                                                                  
                                                               
                       Developed by:  G0ldenRat10                                    
    """
    print(art)
    time.sleep(2)

if os.geteuid() != 0:
    print("This script must be run as root.")
    print("\nExiting the program...")
    sys.exit(1)


def install_dependencies():
    try:
        distro = subprocess.check_output("lsb_release -d", shell=True).decode().strip()
        if "Ubuntu" in distro or "Debian" in distro:
            subprocess.run(["apt-get", "update"])
            subprocess.run(["apt-get", "install", "-y", "curl", "tor"])
        elif "Fedora" in distro or "CentOS" in distro or "Red Hat" in distro:
            subprocess.run(["yum", "install", "-y", "curl", "tor"])
        elif "Arch" in distro:
            subprocess.run(["pacman", "-S", "--noconfirm", "curl", "tor"])
        else:
            print("ERROR: Unsupported distribution !")
            print("\n***************************************")
            print("* Supported distributions:            *")
            print("***************************************")
            print("• Ubuntu")
            print("• Debian")
            print("• Fedora")
            print("• CentOS")
            print("• Red Hat")
            print("• Arch")
            print("***************************************")
            sys.exit(1)
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def check_dependencies():
    try:
        subprocess.check_call(["curl", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["tor", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Installing curl and tor...")
        install_dependencies()


def start_tor():
    try:
        tor_status = subprocess.check_output(["systemctl", "is-active", "tor"]).decode().strip()
        if tor_status != "active":
            print("Starting Tor service...")
            subprocess.run(["systemctl", "start", "tor"])
    except Exception as e:
        print(f"Error starting Tor service: {e}")
        sys.exit(1)


def get_ip():
    try:
        url = "https://checkip.amazonaws.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching IP: {e}")
        sys.exit(1)


def change_ip():
    try:
        subprocess.run(["systemctl", "reload", "tor"], check=True)
        time.sleep(5)
        new_ip = get_ip()  
        print(f"\nNew IP address: {new_ip}")
        show_ip_location(new_ip)  

    except subprocess.CalledProcessError as e:
        print(f"Error reloading Tor: {e}")
        sys.exit(1)

def show_ip_location(ip):
    url = f"https://ipapi.co/{ip}/json/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error: Failed to retrieve location data.")
        return

    data = response.json()
    print(f"City: {data.get('city')}")
    print(f"Region: {data.get('region')}")
    print(f"Country: {data.get('country_name')}")
    



def change_ip_loop():
    try:
        while True:
            interval = input("Enter time interval in seconds (type 0 for infinite IP changes): ")
            times = input("Enter number of times to change IP address (type 0 for infinite IP changes): ")
            print("Press CTRL + C to quit program at any time.")
            
            if not interval.isdigit() or not times.isdigit():
                print("Please enter valid numbers.")
                continue

            interval = int(interval)
            times = int(times)

            if interval == 0 or times == 0:
                print("\nStarting infinite IP changes...")
                while True:
                    change_ip()
                    sleep_time = random.randint(10, 20)
                    time.sleep(sleep_time)
            else:
                for i in range(times):
                    change_ip()
                    time.sleep(interval)

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(0)

'''Main'''
if __name__ == "__main__":
    display_ASCII_intro()
    check_dependencies()
    start_tor()
    change_ip_loop()
