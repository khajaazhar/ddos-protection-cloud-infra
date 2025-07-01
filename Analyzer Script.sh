#!/bin/bash
LOG_FILE="/var/log/nginx/access.log"
THRESHOLD=50  # Requests in last 1000 lines
TEMP_FILE="/tmp/ip_counts.txt"

touch "$TEMP_FILE"

while true; do
    ATTACKER_IP=$(cat "$LOG_FILE" "$LOG_FILE.1" 2>/dev/null | tail -n 1000 | awk '{print $1}' | sort | uniq -c | sort -nr | awk -v thresh="$THRESHOLD" '$1 > thresh {print $2}' | head -1)
    if [ ! -z "$ATTACKER_IP" ]; then
        if ! grep -q "$ATTACKER_IP" "$TEMP_FILE"; then
            echo "Blocking IP: $ATTACKER_IP at $(date)"
            sudo iptables -A INPUT -s "$ATTACKER_IP" -j DROP
            echo "$ATTACKER_IP" >> "$TEMP_FILE"
        else
            echo "IP $ATTACKER_IP already blocked"
        fi
    else
        echo "No IPs exceeding threshold at $(date)"
    fi
    echo "Top IPs in last 1000 lines:"
    cat "$LOG_FILE" "$LOG_FILE.1" 2>/dev/null | tail -n 1000 | awk '{print $1}' | sort | uniq -c | sort -nr | head -5
    sleep 60
done