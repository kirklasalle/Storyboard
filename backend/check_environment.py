import sys
import os
import subprocess
import socket
import sqlite3
import shutil

def print_status(message, success=True):
    symbol = "✓" if success else "✗"
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol} {message}{reset}")

def check_python():
    print("Checking Python environment...")
    if sys.version_info < (3, 8):
        print_status(f"Python 3.8+ required (Found {sys.version})", False)
        return False
    print_status(f"Python {sys.version.split()[0]} found")
    return True

def check_dependencies():
    print("\nChecking backend dependencies...")
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print_status("requirements.txt not found", False)
        return False
    
    try:
        # Simple way to check if basics are installed
        import fastapi
        import uvicorn
        import sqlalchemy
        import openai
        print_status("Core backend dependencies found")
        return True
    except ImportError as e:
        print_status(f"Missing dependency: {e.name}. Run 'pip install -r requirements.txt'", False)
        return False

def check_database():
    print("\nChecking database health...")
    db_path = "database/storyboard.db"
    if not os.path.exists(db_path):
        # Check root too
        if os.path.exists("storyboard.db"):
            db_path = "storyboard.db"
        else:
            print_status("Database file not found. It will be initialized on first run.", True)
            return True
            
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print_status(f"Database connected (Found tables: {', '.join(tables)})")
        conn.close()
        return True
    except Exception as e:
        print_status(f"Database error: {e}", False)
        return False

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

def check_node():
    print("\nChecking node environment...")
    try:
        if shutil.which("node"):
            version = subprocess.check_output(["node", "--version"], shell=True, stderr=subprocess.STDOUT).decode().strip()
            print_status(f"Node.js {version} found")
        else:
            print_status("Node.js not found. Frontend will not be able to run.", False)
            return False
            
        if shutil.which("npm"):
            version = subprocess.check_output(["npm", "--version"], shell=True, stderr=subprocess.STDOUT).decode().strip()
            print_status(f"npm {version} found")
        else:
            print_status("npm not found", False)
            return False
    except Exception as e:
        print_status(f"Error checking Node/npm: {e}", False)
        return False
    return True

def main():
    print("=== Storyboard AI System Health Check ===\n")
    all_ok = True
    
    if not check_python(): all_ok = False
    if not check_dependencies(): all_ok = False
    if not check_database(): all_ok = False
    if not check_node(): 
        # Node failure is non-fatal for backend but we warn
        pass
        
    print("\nChecking port availability...")
    if check_port(8000):
        print_status("Port 8000 (Backend) is available")
    else:
        print_status("Port 8000 is BUSY. Is another instance running?", False)
        # Non-fatal if we are restarting
    
    if all_ok:
        print("\n\033[94mSystem ready for launch! 🚀\033[0m")
        sys.exit(0)
    else:
        print("\n\033[93mSome issues were found. Attempting to launch anyway...\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
