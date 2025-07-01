import subprocess
import time
from collections import Counter

LOG_FILE = "/var/log/nginx/access.log"
THRESHOLD = 20  # Max requests per minute
UNBLOCK_AFTER = 300  # Unblock after 5 minutes (300 seconds)

blocked_ips = {}  # Track blocked IPs and their block time

def get_top_ip():
    result = subprocess.run(['tail', '-n', '1000', LOG_FILE], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    ips = [line.split()[0] for line in lines]
    ip_counts = Counter(ips)
    for ip, count in ip_counts.items():
        if count > THRESHOLD and ip not in blocked_ips:
            return ip
    return None

def block_ip(ip):
    print(f"Blocking IP: {ip}")
    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
    blocked_ips[ip] = time.time()  # Record block time

def unblock_ip(ip):
    print(f"Unblocking IP: {ip}")
    subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'])
    blocked_ips.pop(ip, None)  # Remove from tracking

while True:
    # Block new attackers
    attacker_ip = get_top_ip()
    if attacker_ip:
        block_ip(attacker_ip)

    # Check for IPs to unblock
    current_time = time.time()
    for ip, block_time in list(blocked_ips.items()):
        if current_time - block_time > UNBLOCK_AFTER:
            unblock_ip(ip)

    time.sleep(60)  # Check every minute