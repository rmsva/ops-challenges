# Define settings for automatic updates
$updateSettings = @{
    "AutoDownloadInstall" = 4  # 4 - Download and install updates automatically
    "InstallEveryDay" = 0  # 0 - Install updates every day
    "InstallAtTime" = 3  # 3 - Install updates at 3:00 AM (adjust as necessary)
}

# Configure registry keys for Windows Update
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\" -Name "AUOptions" -Value $updateSettings["AutoDownloadInstall"]
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\" -Name "ScheduledInstallDay" -Value $updateSettings["InstallEveryDay"]
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\" -Name "ScheduledInstallTime" -Value $updateSettings["InstallAtTime"]

# Restart the Windows Update service to apply the new settings
Restart-Service -Name wuauserv -Force
