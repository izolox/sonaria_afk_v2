from PIL import Image
import requests
import json
import mss

DEFAULT_EMBED = { 
    "author": {
        "name": "Sonaria AFK",
        "icon_url": "https://static.wikia.nocookie.net/creatures-of-agartha-official/images/e/e6/Site-logo.png"
    },
    "title": "Sonaria AFK Telemetry",
    "description": "Recieved script telemetry",
    "color": 0x87CEEB,
    "image": {
        "url": ""
    },
    "footer": {
        "text": "Sonaria AFK"
    }
}

class TelemetryHandler:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        
        # Send a init message to discord (just so we know the webhook works and the module initialized)
        self.send_discord_embed({
            "title": "Sonaria AFK Telemetry",
            "description": "Initialized telemetry handler",
            "color": 0x87CEEB,
            "footer": {
                "text": "This is just the initialization message"
            },
        })
        
        print("Telemetry handler initialized")
        
    def __capture_screen(self) -> Image:
        with mss.mss() as sct:
            # Capture screen (all monitors)        
            screenshot = sct.grab(sct.monitors[0]) 
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            
            return img
        
    def send_telemetry(self) -> None:
        try:
            # Capture the screen and save it
            img = self.__capture_screen()
            img.save("screenshot.png")
            
            # Send a telemetry message to discord
            self.send_discord_embed({
                "image": "screenshot.png"
            })
            
            img.close()
            
        except Exception as e:
            print(f"Error while sending telemetry: {e}")
            
    def send_discord_embed(self, data: dict) -> None:
        try:
            embed_copy = DEFAULT_EMBED.copy()
            
            embed_copy["author"] = data.get("author", DEFAULT_EMBED["author"])
            embed_copy["title"] = data.get("title", DEFAULT_EMBED["title"])
            embed_copy["description"] = data.get("description", DEFAULT_EMBED["description"])
            embed_copy["color"] = data.get("color", DEFAULT_EMBED["color"])
            embed_copy["footer"] = data.get("footer", DEFAULT_EMBED["footer"])
            
            if data.get("image"):
                image = data["image"]
                
                with open(image, "rb") as f:
                    embed_copy["image"]["url"] = f"attachment://{image}"
                    payload = json.dumps({
                        "username": "Sonaria AFK",
                        "avatar_url": "https://static.wikia.nocookie.net/creatures-of-agartha-official/images/e/e6/Site-logo.png",
                        "embeds": [embed_copy]
                    })
                    
                    response = requests.post(self.webhook_url, 
                        files = {"file": (image, f, "image/png")}, 
                        data = {"payload_json": payload}
                    )
            
                    if not response.status_code in [200, 204]:
                        print(f"Failed to send telemetry, status code: {response.status_code}")
                        print("Did you forget to configure the webhook URL?")
            else:
                payload = json.dumps({
                    "username": "Sonaria AFK",
                    "avatar_url": "https://static.wikia.nocookie.net/creatures-of-agartha-official/images/e/e6/Site-logo.png",
                    "embeds": [embed_copy]
                })
                
                response = requests.post(self.webhook_url, 
                    headers = {"Content-Type": "application/json"},
                    data = payload
                )
                
                if not response.status_code in [200, 204]:
                    print(f"Failed to send telemetry, status code: {response.status_code}")
                    print("Did you forget to configure the webhook URL?")
                
        except Exception as e:
            print(f"Error while sending telemetry: {e}")