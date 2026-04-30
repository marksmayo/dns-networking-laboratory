#!/usr/bin/env python3
"""
Simplified build script for DNS Benchmark Laboratory
"""

import subprocess
import sys

def main():
    """Simple build without version info that was causing issues"""
    
    print("Building DNS Benchmark Laboratory (Simplified)")
    
    cmd = [
        "pyinstaller",
        "--name", "DNS-Benchmark-Laboratory",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--add-data", "src;src",
        "main.py"
    ]
    
    print("Building executable...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print("Executable location: dist/DNS-Benchmark-Laboratory.exe")
        print("\nYou can now run the standalone executable!")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code: {e.returncode}")
        print("Try installing missing dependencies or check the error above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)