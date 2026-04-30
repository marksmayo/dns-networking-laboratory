#!/usr/bin/env python3
"""
Build script to create standalone executables for DNS Benchmark Pro
Supports Windows (.exe), macOS (.app), and Linux (binary)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_executable():
    """Create standalone executable using PyInstaller"""
    
    # Get platform-specific settings
    system = platform.system().lower()
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "DNS-Benchmark-Pro",
        "--onefile",
        "--windowed",  # Hide console on Windows/macOS
        "--clean",
        "--noconfirm",
        "main.py"
    ]
    
    # Add icon if available
    icon_file = None
    if system == "windows":
        icon_file = "assets/icon.ico"
        if os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])
    elif system == "darwin":  # macOS
        icon_file = "assets/icon.icns"
        if os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])
    
    # Add hidden imports for dependencies that might not be detected
    hidden_imports = [
        "customtkinter",
        "matplotlib.backends.backend_tkagg",
        "dnspython",
        "PIL._tkinter_finder",
        "tkinter",
        "tkinter.ttk",
        "numpy",
        "threading",
        "concurrent.futures",
        "statistics",
        "queue",
    ]
    
    for import_name in hidden_imports:
        cmd.extend(["--hidden-import", import_name])
    
    # Add data files
    data_files = [
        ("src", "src"),
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    # Platform-specific adjustments
    if system == "windows":
        # Add version info for Windows
        cmd.extend([
            "--version-file", "version_info.txt"
        ])
    elif system == "darwin":
        # macOS specific options
        cmd.extend([
            "--osx-bundle-identifier", "com.dnsbenchmarkpro.app",
        ])
    
    print(f"Building executable for {system}...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\\n✅ Executable built successfully!")
        print(f"📁 Output location: dist/DNS-Benchmark-Pro{'.exe' if system == 'windows' else ''}")
        
        # Additional instructions
        if system == "darwin":
            print("\\n📝 Note for macOS users:")
            print("   You may need to run: xattr -cr dist/DNS-Benchmark-Pro.app")
            print("   This removes quarantine attributes that might prevent execution.")
        elif system == "linux":
            print("\\n📝 Note for Linux users:")
            print("   Make sure the executable has run permissions:")
            print("   chmod +x dist/DNS-Benchmark-Pro")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error code: {e.returncode}")
        return False
    
    return True

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = '''# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'DNS Benchmark Pro'),
        StringStruct('FileDescription', 'Advanced DNS Performance Testing Tool'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'DNS-Benchmark-Pro'),
        StringStruct('LegalCopyright', 'Copyright (c) 2024 DNS Benchmark Pro'),
        StringStruct('OriginalFilename', 'DNS-Benchmark-Pro.exe'),
        StringStruct('ProductName', 'DNS Benchmark Pro'),
        StringStruct('ProductVersion', '1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)'''
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)

def create_installer_script():
    """Create platform-specific installer scripts"""
    system = platform.system().lower()
    
    if system == "windows":
        # Create Windows installer script (Inno Setup)
        inno_script = '''[Setup]
AppName=DNS Benchmark Pro
AppVersion=1.0.0
AppPublisher=DNS Benchmark Pro
AppPublisherURL=https://github.com/yourusername/dns-benchmark-pro
DefaultDirName={autopf}\\DNS Benchmark Pro
DefaultGroupName=DNS Benchmark Pro
UninstallDisplayIcon={app}\\DNS-Benchmark-Pro.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=DNS-Benchmark-Pro-Setup

[Files]
Source: "dist\\DNS-Benchmark-Pro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\DNS Benchmark Pro"; Filename: "{app}\\DNS-Benchmark-Pro.exe"
Name: "{group}\\Uninstall DNS Benchmark Pro"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\DNS Benchmark Pro"; Filename: "{app}\\DNS-Benchmark-Pro.exe"

[Run]
Filename: "{app}\\DNS-Benchmark-Pro.exe"; Description: "Launch DNS Benchmark Pro"; Flags: nowait postinstall skipifsilent
'''
        
        with open("installer.iss", "w") as f:
            f.write(inno_script)
        
        print("\\n📦 Windows installer script created: installer.iss")
        print("   Use Inno Setup to compile the installer")
    
    elif system == "darwin":
        # Create macOS disk image script
        dmg_script = '''#!/bin/bash
# Create macOS DMG installer

APP_NAME="DNS Benchmark Pro"
APP_PATH="dist/DNS-Benchmark-Pro.app"
DMG_NAME="DNS-Benchmark-Pro-1.0.0.dmg"

if [ ! -d "$APP_PATH" ]; then
    echo "App not found at $APP_PATH"
    exit 1
fi

# Create temporary directory
mkdir -p dist/dmg

# Copy app to dmg directory
cp -R "$APP_PATH" dist/dmg/

# Create DMG
hdiutil create -volname "$APP_NAME" -srcfolder dist/dmg -ov -format UDZO "dist/$DMG_NAME"

# Cleanup
rm -rf dist/dmg

echo "DMG created: dist/$DMG_NAME"
'''
        
        with open("create_dmg.sh", "w") as f:
            f.write(dmg_script)
        
        os.chmod("create_dmg.sh", 0o755)
        print("\\n📦 macOS DMG script created: create_dmg.sh")

def main():
    """Main build function"""
    print("🚀 DNS Benchmark Pro - Build Script")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.architecture()[0]}")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create version info for Windows
    if platform.system().lower() == "windows":
        create_version_info()
    
    # Create the executable
    if not create_executable():
        return False
    
    # Create installer scripts
    create_installer_script()
    
    print("\\n🎉 Build process completed successfully!")
    print("\\nNext steps:")
    print("1. Test the executable in dist/")
    print("2. Create installer using the generated scripts")
    print("3. Distribute to users")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)