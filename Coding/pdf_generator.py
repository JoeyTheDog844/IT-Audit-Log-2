from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from system_information2 import (
    generate_system_report,
    get_system_info,
    get_network_details,
    get_last_windows_update,
    get_desktop_files,
    get_system_identity,
    get_all_user_accounts,
)
from log_manager import (
    get_security_logs,
    get_system_logs,
    get_application_logs,
    get_dns_logs,
    get_usb_logs,
)
from security_logs import (
    get_antivirus_status,
    get_last_scan_time,
    get_usb_device_control_status,
    get_autoplay_status,
    get_rdp_status,
    get_telnet_status,
    get_default_share_status,
    get_shared_folder_status,
    check_saved_passwords,
    get_bios_password_status,
    get_login_password_status,
    get_password_policy_status,
    get_lockout_policy_status,
)
import datetime

def generate_pdf_report():
    filename = "System_Audit_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Start position for text

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y_position, "System Audit Report")
    y_position -= 40

    def check_page_break():
        """ Ensures text does not overflow onto the next page """
        nonlocal y_position
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40

    def add_section(title, content):
        """ Handles adding sections properly with spacing """
        nonlocal y_position
        check_page_break()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, title)
        y_position -= 20
        c.setFont("Helvetica", 10)

        content = content if content else "No Data Available"

        for line in content.split("\n"):
            c.drawString(60, y_position, line)
            y_position -= 15
            check_page_break()

        y_position -= 10  # Space between sections

    # ✅ Generate Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Collect system data
    add_section("System Info", "\n".join([f"{k}: {v}" for k, v in get_system_info().items()]))
    add_section("Network Details", "\n".join([f"{k}: {v}" for k, v in get_network_details().items()]))
    add_section("Users Accounts", get_all_user_accounts())
    add_section("Last Windows Update", get_last_windows_update())

    desktop_files = get_desktop_files()
    if isinstance(desktop_files, (tuple, list)):
        desktop_files = "\n".join(map(str, desktop_files))

    add_section("Desktop Files", desktop_files)

    # ✅ Collect log data
    add_section("Security Logs", get_security_logs())
    add_section("System Logs", get_system_logs())
    add_section("Application Logs", get_application_logs())
    add_section("DNS Logs", get_dns_logs())
    add_section("USB Logs", get_usb_logs())

    # ✅ Antivirus Details
    antivirus_content = (
        f"Timestamp: {timestamp}\n"
        f"Antivirus Installed: {get_antivirus_status()}\n"
        f"Last Windows Defender Scan Time: {get_last_scan_time()}"
    )
    add_section("Antivirus", antivirus_content)

    # ✅ Other Security Features
    add_section("USB Storage Device Access", get_usb_device_control_status())
    add_section("AutoPlay Status", get_autoplay_status())
    add_section("Remote Desktop Protocol (RDP)", get_rdp_status())
    add_section("Telnet", get_telnet_status())
    add_section("Default Share Status", get_default_share_status())
    add_section("Shared Folder Status", get_shared_folder_status())

    # ✅ Password Security (Now Without Emojis)
    add_section("Passwords not saved in web/system", check_saved_passwords())
    add_section(
        "Password Security",
        "\n".join(
            [
                f"BIOS Password: {get_bios_password_status()}",
                f"Windows Login Password: {get_login_password_status()}",
            ]
        ),
    )

    add_section("Password Policy", get_password_policy_status())

    # ✅ System Lockout Policy (Now Always Displays Properly)
    add_section("System Lockout Policy", get_lockout_policy_status())

    # ✅ Save the PDF
    c.save()
    print(f"✅ PDF Report Generated: {filename}")

# ✅ Run the script
if __name__ == "__main__":
    generate_pdf_report()
