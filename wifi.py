import requests
import subprocess
import platform
import re
import json
import time

def get_current_ip():
    """Get the current IP address of the machine dynamically"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            # Get the default interface
            interface_output = subprocess.check_output("route -n get default | grep interface", shell=True).decode('utf-8')
            interface = interface_output.split(":")[1].strip()
            
            # Get IP from that interface
            ip_output = subprocess.check_output(f"ifconfig {interface} | grep inet | grep -v inet6 | awk '{{print $2}}'", shell=True).decode('utf-8').strip()
            return ip_output
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None
    
    elif system == "Windows":
        try:
            # Windows command to get IP
            output = subprocess.check_output("ipconfig", shell=True).decode('utf-8')
            # Look for WiFi or Ethernet adapter
            for line in output.split('\n'):
                if "IPv4 Address" in line and "192.168" in line:
                    return re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
            return None
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None
    
    elif system == "Linux":
        try:
            # Linux command to get IP
            ip_output = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode('utf-8').strip()
            return ip_output
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None
    
    return None

def get_new_token():
    """Get a new authentication token from the login endpoint"""
    headers = {
        # ... (headers as before)
    }
    
    payload = {
        "phone_number": "Your Username",
        "password": "Your Password"
    }
    
    url = "https://spash-server.darkube.app/auth/login"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Debug - Status Code: {response.status_code}")  # Debugging line
        print(f"Debug - Response Content: {response.text}")    # Debugging line
        
        if response.status_code in [200, 201]:
            json_response = response.json()
            print(f"Debug - JSON Response: {json_response}")  # Debugging line
            token = json_response.get('token')
            if token:
                print("Debug - Token retrieved successfully.")  # Debugging line
                return token
            else:
                print("Debug - 'token' key missing in response.")  # Debugging line
                return None
        else:
            print(f"Failed to get new token. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error getting new token: {e}")
        return None
def authenticate_wifi():
    """Authenticate the WiFi connection using the captive portal"""
    # Get current IP address
    current_ip = get_current_ip()
    if not current_ip:
        print("Failed to get current IP address!")
        return False
    
    print(f"Current IP address: {current_ip}")
    
    # Get a new token
    auth_token = get_new_token()
    if not auth_token:
        print("Failed to get authentication token!")
        return False
    
    # Headers based on your captured request
    headers = {
        "Sec-Ch-Ua-Platform": "macOS",
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://spash.space",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://spash.space/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    # Request payload with the current IP
    payload = {"ip": current_ip}
    
    # API endpoint
    url = "https://spash-server.darkube.app/user/wifi"
    
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("Successfully authenticated WiFi connection!")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"Authentication failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"Error authenticating WiFi: {e}")
        return False

def check_internet_connection():
    """Check if there is an active internet connection"""
    try:
        # Try to connect to Google's DNS server
        response = requests.get("https://8.8.8.8", timeout=2)
        return True
    except:
        return False

def main():
    print("WiFi Authentication Script Started")
    
    # Check if already connected
    if check_internet_connection():
        print("Internet is already connected!")
        return
    
    # Try to authenticate
    success = authenticate_wifi()
    
    if success:
        # Wait a moment for the connection to establish
        print("Waiting for connection to establish...")
        time.sleep(3)
        
        # Verify connection is working
        if check_internet_connection():
            print("Internet connection verified!")
        else:
            print("Internet connection still not working. You may need to update the auth token.")
    else:
        print("Failed to authenticate WiFi.")

if __name__ == "__main__":
    main()

