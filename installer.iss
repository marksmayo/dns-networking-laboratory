[Setup]
AppName=DNS Benchmark Pro
AppVersion=1.0.0
AppPublisher=DNS Benchmark Pro
AppPublisherURL=https://github.com/yourusername/dns-benchmark-pro
DefaultDirName={autopf}\DNS Benchmark Pro
DefaultGroupName=DNS Benchmark Pro
UninstallDisplayIcon={app}\DNS-Benchmark-Pro.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=DNS-Benchmark-Pro-Setup

[Files]
Source: "dist\DNS-Benchmark-Pro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DNS Benchmark Pro"; Filename: "{app}\DNS-Benchmark-Pro.exe"
Name: "{group}\Uninstall DNS Benchmark Pro"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DNS Benchmark Pro"; Filename: "{app}\DNS-Benchmark-Pro.exe"

[Run]
Filename: "{app}\DNS-Benchmark-Pro.exe"; Description: "Launch DNS Benchmark Pro"; Flags: nowait postinstall skipifsilent
