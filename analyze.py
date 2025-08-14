# Same Analyser as IN : https://github.com/Saassoso/honeypot-log-analyzer 
#!/usr/bin/env python3

import json
import os
from collections import Counter
from datetime import datetime

def analyze_web_logs():
    """Analyze web honeypot logs"""
    log_file = './logs/web/attacks.json'
    
    if not os.path.exists(log_file):
        print("No web logs found")
        return
    
    attacks = []
    ips = Counter()
    usernames = Counter()
    passwords = Counter()
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    attack = json.loads(line.strip())
                    attacks.append(attack)
                    ips[attack['ip']] += 1
                    
                    if attack['event'] == 'LOGIN_ATTEMPT':
                        data = attack['data']
                        usernames[data.get('username', '')] += 1
                        passwords[data.get('password', '')] += 1
                except:
                    continue
    except FileNotFoundError:
        print("No web attack logs found")
        return
    
    print("=== WEB HONEYPOT ANALYSIS ===")
    print(f"Total attacks: {len(attacks)}")
    print(f"Unique IPs: {len(ips)}")
    
    print("\nTop Attacking IPs:")
    for ip, count in ips.most_common(10):
        print(f"  {ip}: {count}")
    
    print("\nTop Usernames Attempted:")
    for username, count in usernames.most_common(10):
        if username:
            print(f"  {username}: {count}")
    
    print("\nTop Passwords Attempted:")
    for password, count in passwords.most_common(10):
        if password:
            print(f"  {password}: {count}")

def analyze_ssh_logs():
    """Analyze SSH honeypot logs"""
    log_file = './logs/ssh/cowrie.json'
    
    if not os.path.exists(log_file):
        print("\nNo SSH logs found")
        return
    
    ips = Counter()
    commands = Counter()
    sessions = set()
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if 'src_ip' in entry:
                        ips[entry['src_ip']] += 1
                    if 'session' in entry:
                        sessions.add(entry['session'])
                    if entry.get('eventid') == 'cowrie.command.input':
                        commands[entry.get('input', '')] += 1
                except:
                    continue
    except FileNotFoundError:
        print("\nNo SSH logs found")
        return
    
    print("\n=== SSH HONEYPOT ANALYSIS ===")
    print(f"Total SSH sessions: {len(sessions)}")
    print(f"Unique IPs: {len(ips)}")
    
    print("\nTop Attacking IPs:")
    for ip, count in ips.most_common(10):
        print(f"  {ip}: {count}")
    
    print("\nTop Commands:")
    for cmd, count in commands.most_common(10):
        if cmd.strip():
            print(f"  {cmd}: {count}")

def main():
    print("Simple Honeypot Log Analyzer")
    print(f"Analysis time: {datetime.now()}")
    print("=" * 40)
    
    analyze_web_logs()
    analyze_ssh_logs()
    
    print("\n" + "=" * 40)
    print("Analysis complete!")

if __name__ == "__main__":
    main()