import subprocess

def disable_dns_client():
    service_name = "Dnscache"
    try:
        # PowerShell command to stop and disable DNS Client service
        command = f'powershell -Command "Set-Service -Name \'{service_name}\' -StartupType Disabled; Stop-Service -Name \'{service_name}\' -Force"'
        
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return f"✅ DNS Client ('{service_name}') has been successfully disabled."
        else:
            return f"❌ Failed to disable DNS Client. Error: {result.stderr.strip()}"

    except Exception as e:
        return f"❌ Error disabling DNS Client: {str(e)}"

# Run the function
print(disable_dns_client())
