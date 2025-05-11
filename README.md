# PyTor IP Changer
PyTor is a Python-based script designed to help you rotate your IP address via the Tor network, ensuring enhanced anonymity and privacy. The tool uses the Tor service to change your IP address and provides a simple way to verify the IP change and fetch geolocation information based on the new IP.

![My Image](https://github.com/G0ldenRat10/PrivatePictures/blob/main/Screenshot_2025-05-11_13_44_44.png?raw=true)

# Features

-  Rotates your IP address using the Tor network.

-  Fetches and displays the new IP address.

-  Retrieves geolocation information (city, region, country) based on the new IP.

-  Configurable intervals for IP rotation.

-  Can run in an infinite loop for continuous IP changes.

# How to Run the Script 

1. Clone the repository 

       git clone https://github.com/G0ldenRat10/PyTor-IP-Changer.git
       cd PyTor-IP-Changer
2. Run the script

       sudo python3 pytor.py


# Requirements

The script automatically installs any necessary dependencies (such as curl, tor, and requests) when it runs, so no manual installation is required.

However, make sure that Tor is installed and running on your system. The script will check for the required dependencies and install them if they are missing.

Also it's important to have python3 and pip installed to run this program !

      sudo apt install python3 python3-pip -y

# New Version 1.2.0 
- Version upgrade from 1.1.0  ---->  1.2.0
- Upgraded get_ip() function  ---->  It now has secondary and tertiary services if primary one fails.
- Upgraded show_ip_location()  ---->  Now it randomly selects one of three geolocation APIs to provide the location information. More resilient to service failures.
- Better code organization, error handling, user interactivity and feedback.

          

# Youtube Tutorial

How to make it work for Firefox or other web browsers, connect to port 9050, enable SOCKS5, code explanation and much more:

[Youtube Video Link](https://www.youtube.com/watch?v=lH5h_PO5hFI&lc=UgylLkXPRhuqQEwbb5h4AaABAg)
