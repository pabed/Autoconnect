# WiFi Captive Portal Auto-Authentication Script

This Python script automatically authenticates your device with a captive portal WiFi network (specifically designed for 7o8 WiFi service). The script detects your current IP address, obtains an authentication token, and submits the required credentials to bypass the captive portal.

## Features

- **Cross-platform support**: Works on macOS, Windows, and Linux
- **Automatic IP detection**: Dynamically finds your current IP address
- **Token-based authentication**: Securely authenticates using bearer tokens
- **Connection verification**: Checks internet connectivity before and after authentication
- **Easy execution**: Includes shell script for one-click execution

## Files Included

- `wifi.py` - Main Python script for WiFi authentication
- `RunPython.command` - Shell script for easy execution on macOS/Linux

## Prerequisites

- Python 3.x installed on your system
- `requests` library (install with `pip install requests`)
- Active connection to the 7o8 WiFi network (but not yet authenticated)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install requests
```

### 2. Configure Your Credentials

Edit the `wifi.py` file and update the following lines with your actual credentials:

```python
payload = {
    "phone_number": "Your Username",  # Replace with your actual username/phone
    "password": "Your Password"       # Replace with your actual password
}
```

### 3. Platform-Specific Setup

#### macOS (Tested and Verified)
1. Update the path in `RunPython.command`:
   ```bash
   cd /Path/Of/YourScript  # Change this to your actual script directory
   ```
2. Make the script executable:
   ```bash
   chmod +x RunPython.command
   ```
3. Double-click `RunPython.command` to run, or execute in terminal:
   ```bash
   ./RunPython.command
   ```

#### Windows
1. **Option 1 - Direct Python execution:**
   ```cmd
   python wifi.py
   ```

2. **Option 2 - Create a batch file:**
   Create `run_wifi.bat` with the following content:
   ```batch
   @echo off
   cd /d "C:\Path\To\Your\Script"
   python wifi.py
   pause
   ```
   Replace `C:\Path\To\Your\Script` with your actual script directory.

3. **Additional Windows requirements:**
   - Ensure Python is added to your system PATH
   - You may need to run as administrator for network operations

#### Linux
1. **Option 1 - Direct Python execution:**
   ```bash
   python3 wifi.py
   ```

2. **Option 2 - Use the shell script:**
   ```bash
   # Make executable
   chmod +x RunPython.command
   
   # Update the script path
   nano RunPython.command
   # Change: cd /Path/Of/YourScript
   # To: cd /path/to/your/script
   
   # Run the script
   ./RunPython.command
   ```

3. **Additional Linux requirements:**
   - Ensure you have network management permissions
   - Some distributions may require `sudo` for network operations

## Usage

### Automatic Execution
1. Connect to the Spash WiFi network
2. Run the script using one of the methods above
3. The script will automatically:
   - Detect your IP address
   - Authenticate with the captive portal
   - Verify your internet connection

### Manual Execution
```bash
# macOS/Linux
python3 wifi.py

# Windows
python wifi.py
```

## How It Works

1. **IP Detection**: The script automatically detects your current IP address using platform-specific commands:
   - **macOS**: Uses `route` and `ifconfig` commands
   - **Windows**: Parses `ipconfig` output
   - **Linux**: Uses `hostname -I` command

2. **Token Authentication**: 
   - Sends credentials to the login endpoint
   - Retrieves a bearer token for authentication

3. **WiFi Authentication**:
   - Uses the token and IP address to authenticate with the captive portal
   - Sends a POST request to the WiFi endpoint

4. **Connection Verification**:
   - Tests internet connectivity before and after authentication
   - Provides feedback on the authentication status

## Troubleshooting

### Common Issues

**"Failed to get current IP address"**
- Ensure you're connected to the network
- Check if your system commands are working properly
- Try running the script with administrator/sudo privileges

**"Failed to get authentication token"**
- Verify your username and password are correct
- Check if the login endpoint is accessible
- Ensure you're connected to the 7o8 wifi ssid

**"Authentication failed"**
- The captive portal might have changed its requirements
- Try updating the request headers or payload format
- Check if the WiFi endpoint URL is still valid

### Debug Mode
The script includes debug output to help troubleshoot issues. Look for lines starting with "Debug -" in the console output.

### Network-Specific Issues

**Windows:**
- Run Command Prompt as Administrator
- Ensure Windows Defender/Firewall isn't blocking the script
- Check if Python scripts are allowed to make network connections

**Linux:**
- Use `sudo` if you encounter permission errors
- Ensure `curl` and network utilities are installed
- Check firewall settings (`ufw`, `iptables`)

## Security Considerations

- Your credentials are stored in plain text in the script file
- Consider using environment variables for sensitive information
- The script makes HTTPS requests, but always verify the endpoints
- Keep the script file permissions restricted (readable only by owner)

## Customization

You can modify the script to work with different captive portals by:
1. Updating the authentication endpoint URLs
2. Modifying the request headers and payload format
3. Adjusting the IP detection method for your network setup

## License

This script is provided as-is for educational and personal use. Please respect the terms of service of your WiFi provider.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your credentials and network connection
3. Review the debug output for specific error messages
4. Ensure all prerequisites are properly installed
