import os
import sys
import time
import subprocess
import random
import re
import socket
import requests

def display_ASCII_intro():

    color_start = "\033[38;5;93m"
    color_end = "\033[0m"

    art = """

   ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░               
   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓███████▓▒░ ░▒▓██████▓▒░   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░                 
   ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░
                        
                                                                                                        
                    Developed by: \033[38;2;255;215;0mG0ldenRat10\033[0m
              \033[38;5;93mGithub:\033[0m \033[34mhttps://github.com/G0ldenRat10\033[0m                           
    
    """
    print(f"{color_start}{art}{color_end}")
    time.sleep(2)

if os.geteuid() != 0:
    print("\033[1;31mERROR:\033[0m This script must be run as root.")
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
            print("\033[1;31mERROR:\033[0m Unsupported distribution!")
            print("\033[1;33m***************************************")
            print("* Supported distributions:            *")
            print("***************************************")
            print("• Ubuntu")
            print("• Debian")
            print("• Fedora")
            print("• CentOS")
            print("• Red Hat")
            print("• Arch")
            print("***************************************\033[0m")
            sys.exit(1)
    except Exception as e:
        print(f"\033[1;31mERROR:\033[0m Failed installing dependencies: {e}")
        sys.exit(1)


def check_dependencies():
    try:
        subprocess.check_call(["curl", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["tor", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("\033[33mInstalling curl and tor...\033[0m")
        install_dependencies()


def start_tor():
    try:
        tor_status = subprocess.check_output(["systemctl", "is-active", "tor"]).decode().strip()
        if tor_status != "active":
            print("\033[33mStarting Tor service...\033[0m")
            subprocess.run(["systemctl", "start", "tor"])
    except Exception as e:
        print(f"\033[1;31mERROR:\033[0m Failed starting Tor service: {e}")
        sys.exit(1)


def get_ip():
    primary_url = "https://checkip.amazonaws.com"
    secondary_url = "https://api.ipify.org"
    tertiary_url = "https://icanhazip.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    try:
        response = requests.get(primary_url, headers=headers, proxies=proxies, timeout=10)
        return response.text.strip()
    except requests.RequestException:
        print("\033[1;31mERROR:\033[0m Primary IP service failed.")
        print("\033[1;33mWARNING:\033[0m Switching to secondary IP service...")
        try:
            response = requests.get(secondary_url, headers=headers, proxies=proxies, timeout=10)   
            return response.text.strip()
        except requests.RequestException:
            print("\033[1;31mERROR:\033[0m Secondary IP service failed.")
            print("\033[1;33mWARNING:\033[0m Switching to tertiary IP service...")
            try:
                response = requests.get(tertiary_url, headers=headers, proxies=proxies, timeout=10)
                return response.text.strip() 
            except requests.RequestException as e:
                print(f"\033[1;31mERROR:\033[0m Failed fetching IP: {e}")
                sys.exit(1)
        

def change_ip():
    try:
        subprocess.run(["systemctl", "reload", "tor"], check=True)
        time.sleep(5)
        new_ip = get_ip()  
        print(f"\n\033[1;32mNew IP address:\033[0m {new_ip}")
        show_ip_location(new_ip)  

    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mERROR:\033[0m Failed reloading Tor: {e}")
        sys.exit(1)


def show_ip_location(ip):
    api_services = [
        (f"https://ipapi.co/{ip}/json/", ["city", "region", "country_name"]),
        (f"http://ip-api.com/json/{ip}", ["city", "regionName", "country"]),
        (f"https://ipwhois.app/json/{ip}", ["city", "region", "country"]),
                   ]
    
    random.shuffle(api_services)  

    for url, fields in api_services:
        try:
            response = requests.get(url, timeout=random.randint(5, 10))
            if response.status_code == 200:
                data = response.json()
                print(f"\033[1;36mCity:\033[0m {data.get(fields[0], 'Unknown')}")
                print(f"\033[1;36mRegion:\033[0m {data.get(fields[1], 'Unknown')}")
                print(f"\033[1;36mCountry:\033[0m {data.get(fields[2], 'Unknown')}")
                return
        except requests.RequestException as e:
            print(f"\033[1;31mERROR:\033[0m Failed with {url}: {e}")
    
    print("\033[1;31mERROR:\033[0m All geolocation services failed.")
    

def change_ip_loop():
    try:
        while True:
            interval = input("\033[1;36mEnter time interval in seconds\033[0m (type \033[1;33m0\033[0m for infinite IP changes): ")
            times = input("\033[1;36mEnter amount of times to change IP address\033[0m (type \033[1;33m0\033[0m for infinite IP changes): ")
            print("\n\033[1;35mPress CTRL + C to quit program at any time.\033[0m")
            
            if not interval.isdigit() or not times.isdigit():
                print("\n\033[1;31mERROR:\033[0m Please enter valid numbers.")
                continue

            interval = int(interval)
            times = int(times)

            if interval == 0 or times == 0:
                print("\n\033[33mStarting ∞ IP changes...\033[0m")
                while True:
                    change_ip()
                    sleep_time = random.randint(10, 20)
                    time.sleep(sleep_time)
            else:
                for i in range(times):
                    change_ip()
                    time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\033[33mScript interrupted by user:\033[0m \033[1;31mExiting...\033[0m")
        sys.exit(0)


'''Main'''
if __name__ == "__main__":
    display_ASCII_intro()
    check_dependencies()
    start_tor()
    change_ip_loop()
