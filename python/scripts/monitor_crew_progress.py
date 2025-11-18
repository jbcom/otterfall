
#!/usr/bin/env python3
"""Monitor CrewAI task progress and log status"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

def monitor_progress():
    """Monitor crew execution progress"""
    log_dir = Path("./logs/crewai")
    status_file = log_dir / "status.json"
    
    print("🔍 CrewAI Progress Monitor Started")
    print(f"📊 Monitoring log directory: {log_dir}")
    print("-" * 70)
    
    while True:
        try:
            # Check if status file exists
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
                
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Status Update:")
                for task, info in status.items():
                    print(f"  {task}: {info.get('status', 'unknown')}")
            
            # Check log files for errors
            if log_dir.exists():
                for log_file in log_dir.glob("*.log"):
                    # Check last 10 lines for errors
                    try:
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                            error_lines = [l for l in lines[-10:] if 'ERROR' in l or 'Exception' in l]
                            if error_lines:
                                print(f"\n⚠️  Errors in {log_file.name}:")
                                for line in error_lines:
                                    print(f"    {line.strip()}")
                    except Exception as e:
                        pass
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Monitor error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    monitor_progress()
