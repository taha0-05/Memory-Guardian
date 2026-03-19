
import os
import sys
import subprocess
import time

def create_shortcut():
    # Constants
    APP_NAME = "Memory Guardian"
    AUMID = "MemoryGuardian.App.1.0"
    
    # Paths
    current_dir = os.getcwd()
    target_exe = sys.executable
    script_path = os.path.join(current_dir, "main.py")
    
    start_menu_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
    shortcut_path = os.path.join(start_menu_path, f"{APP_NAME}.lnk")
    
    ps_content = f"""
    $lnkPath = "{shortcut_path}"
    $target = "{target_exe}"
    $args = '"{script_path}"'
    $wDir = "{current_dir}"
    
    $ws = New-Object -ComObject WScript.Shell
    $s = $ws.CreateShortcut($lnkPath)
    $s.TargetPath = $target
    $s.Arguments = $args
    $s.WorkingDirectory = $wDir
    $s.Save()
    Write-Host "Shortcut created at $lnkPath"
    """
    
    ps_file = "create_shortcut.ps1"
    with open(ps_file, "w") as f:
        f.write(ps_content)
        
    print("Running PowerShell script...")
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], check=True)
        print("Shortcut created successfully.")
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
    finally:
        if os.path.exists(ps_file):
            os.remove(ps_file)
            
    print(f"IMPORTANT: Ensure BackgroundMonitor uses AUMID: {AUMID}")

if __name__ == "__main__":
    create_shortcut()
