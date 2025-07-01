# DDoS Protection System for Cloud Infrastructure

This project demonstrates a practical approach to mitigating Layer 7 (HTTP Flood) DDoS attacks using a cloud-native infrastructure on AWS. It involves deploying multiple EC2 instances behind a load balancer, implementing access control and rate limiting, and dynamically analyzing and blocking malicious traffic through custom Python scripts.

---

##  Project Overview

- Deploys **two EC2 instances** configured with DDoS protection mechanisms.
- Uses an **Application Load Balancer (ALB)** to distribute traffic and apply initial filtering via **Access Control Lists (ACL)**.
- Each EC2 server runs two key scripts:
  - **Analyzer script:** Parses access logs to detect suspicious patterns.
  - **Blocking script:** Dynamically blocks detected malicious IPs using `iptables`.

---

##  Key Features

- Load-balanced architecture using AWS ALB.
- ACL-based request filtering at the edge.
- Real-time log analysis and dynamic IP blocking.
- Simulation of DDoS attacks for testing defense effectiveness.
- Fully configurable and deployable using AWS Free Tier.

---

##  Technologies Used

- **Cloud Platform:** AWS EC2, ALB, ACL
- **Web Server:** Nginx (rate limiting, logging)
- **Scripting:** Python for automation, `iptables` for blocking
- **Monitoring:** Custom log analysis
- **Security:** CAPTCHA (optional), ACLs, Rate Limiting

##  Deployment Steps

### 1. Launch EC2 Instances (2)
- OS: Ubuntu Server (Free Tier eligible)
- Open ports: HTTP (80), SSH (22)
- Use the same security group for both instances.

### 2. Configure Application Load Balancer
- Create ALB with a target group containing both EC2 instances.
- Set up **ACL** to apply basic access control rules (rate limits, IP deny/allow).
- Health checks: Use HTTP or TCP on port 80.

### 3. Set Up Nginx on Each Server
```bash
sudo apt update
sudo apt install nginx
sudo cp nginx.conf /etc/nginx/nginx.conf  # from this repo
sudo systemctl restart nginx

### 4. Upload Analyzer and Blocking Scripts to Each Instance
analyzer.py: Analyzes Nginx logs for suspicious IPs.
blocker.sh: Takes a list of IPs and blocks them using iptables
These scripts should be run periodically or triggered based on log volume.

### 5. Simulate a DDoS Attack
python3 botnet_simulator.py --target http://<alb-dns> --bots 50
