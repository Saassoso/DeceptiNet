import json
import os
from datetime import datetime
from collections import defaultdict, Counter
import re

class DeceptiNetAnalyzer:
    def __init__(self, log_dir="./data/logs"):
        self.log_dir = log_dir
        self.flask_logs = os.path.join(log_dir, "flask-fake-login")
        self.cowrie_logs = os.path.join(log_dir, "cowrie")
        self.dionaea_logs = os.path.join(log_dir, "dionaea")
    
    def analyze_flask_logs(self):
        """Analyze Flask honeypot logs"""
        print("🌐 FLASK HONEYPOT ANALYSIS")
        print("=" * 50)
        
        json_log = os.path.join(self.flask_logs, "login.json")
        text_log = os.path.join(self.flask_logs, "login.log")
        
        if not os.path.exists(json_log):
            print("❌ No Flask JSON logs found")
            return
        
        attempts = []
        ips = Counter()
        user_agents = Counter()
        usernames = Counter()
        passwords = Counter()
        
        try:
            with open(json_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry['event_type'] == 'LOGIN_ATTEMPT':
                            data = entry['data']
                            attempts.append(entry)
                            ips[data.get('ip', 'unknown')] += 1
                            user_agents[data.get('user_agent', 'unknown')] += 1
                            usernames[data.get('username', '')] += 1
                            passwords[data.get('password', '')] += 1
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print("❌ Flask log file not found")
            return
        
        print(f"📊 Total login attempts: {len(attempts)}")
        print(f"\n🔝 Top attacking IPs:")
        for ip, count in ips.most_common(10):
            print(f"   {ip}: {count} attempts")
        
        print(f"\n👤 Top usernames tried:")
        for username, count in usernames.most_common(10):
            if username:
                print(f"   '{username}': {count} times")
        
        print(f"\n🔑 Top passwords tried:")
        for password, count in passwords.most_common(10):
            if password:
                print(f"   '{password}': {count} times")
        
        print(f"\n🤖 Top User Agents:")
        for ua, count in user_agents.most_common(5):
            print(f"   {ua[:80]}{'...' if len(ua) > 80 else ''}: {count}")
    
    def analyze_cowrie_logs(self):
        """Analyze Cowrie SSH honeypot logs"""
        print("\n🐚 COWRIE SSH HONEYPOT ANALYSIS")
        print("=" * 50)
        
        json_log = os.path.join(self.cowrie_logs, "cowrie.json")
        
        if not os.path.exists(json_log):
            print("❌ No Cowrie logs found")
            return
        
        sessions = set()
        commands = Counter()
        ips = Counter()
        
        try:
            with open(json_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if 'src_ip' in entry:
                            ips[entry['src_ip']] += 1
                        if 'session' in entry:
                            sessions.add(entry['session'])
                        if entry.get('eventid') == 'cowrie.command.input':
                            cmd = entry.get('input', '')
                            commands[cmd] += 1
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print("❌ Cowrie log file not found")
            return
        
        print(f"📊 Total SSH sessions: {len(sessions)}")
        print(f"📊 Unique attacking IPs: {len(ips)}")
        
        print(f"\n🔝 Top attacking IPs:")
        for ip, count in ips.most_common(10):
            print(f"   {ip}: {count} events")
        
        print(f"\n💻 Top commands executed:")
        for cmd, count in commands.most_common(15):
            if cmd.strip():
                print(f"   '{cmd}': {count} times")
    
    def analyze_dionaea_logs(self):
        """Analyze Dionaea malware honeypot logs"""
        print("\n🐛 DIONAEA MALWARE HONEYPOT ANALYSIS")
        print("=" * 50)
        
        log_files = []
        if os.path.exists(self.dionaea_logs):
            log_files = [f for f in os.listdir(self.dionaea_logs) if f.endswith('.log')]
        
        if not log_files:
            print("❌ No Dionaea logs found")
            return
        
        print(f"📁 Found {len(log_files)} log files")
        # Basic analysis - Dionaea logs can be complex
        for log_file in log_files[:5]:  # Show first 5 files
            print(f"   📄 {log_file}")
    
    def generate_summary_report(self):
        """Generate overall summary"""
        print("\n📋 DECEPTINET SUMMARY REPORT")
        print("=" * 50)
        print(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Count total log files
        total_files = 0
        for root, dirs, files in os.walk(self.log_dir):
            total_files += len([f for f in files if f.endswith(('.log', '.json'))])
        
        print(f"📁 Total log files: {total_files}")
        
        # Check which honeypots are active
        active_honeypots = []
        if os.path.exists(self.flask_logs) and os.listdir(self.flask_logs):
            active_honeypots.append("Flask Web")
        if os.path.exists(self.cowrie_logs) and os.listdir(self.cowrie_logs):
            active_honeypots.append("Cowrie SSH")
        if os.path.exists(self.dionaea_logs) and os.listdir(self.dionaea_logs):
            active_honeypots.append("Dionaea Malware")
        
        print(f"🎯 Active honeypots: {', '.join(active_honeypots) if active_honeypots else 'None detected'}")
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🐝 DECEPTINET LOG ANALYZER")
        print("🎯 Analyzing honeypot activity...\n")
        
        self.generate_summary_report()
        self.analyze_flask_logs()
        self.analyze_cowrie_logs()
        self.analyze_dionaea_logs()
        
        print("\n" + "=" * 50)
        print("✅ Analysis complete!")
        print("💡 Tip: Run this analyzer periodically to track attacker trends")

def main():
    analyzer = DeceptiNetAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()