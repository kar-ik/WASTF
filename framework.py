import re
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import os
import subprocess

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def sql_injection_test(url):
    payload = "' OR '1'='1"
    try:
        response = requests.get(url + payload)
        if "mysql" in response.text.lower() or "syntax" in response.text.lower():
            return True, "SQL Injection vulnerability detected!"
        return False, "No SQL Injection vulnerability detected."
    except Exception as e:
        return False, f"Error: {str(e)}"

def xss_test(url):
    xss_payload = "<script>alert('XSS')</script>"
    try:
        response = requests.get(url + xss_payload)
        if xss_payload in response.text:
            return True, "XSS vulnerability detected!"
        return False, "No XSS vulnerability detected."
    except Exception as e:
        return False, f"Error: {str(e)}"

def csrf_test(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        forms = soup.find_all('form')
        csrf_protected = False
        for form in forms:
            if form.find('input', {'name': 'csrf_token'}):
                csrf_protected = True
        if csrf_protected:
            return False, "CSRF protection found."
        return True, "Potential CSRF vulnerability detected!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def insecure_headers_test(url):
    try:
        response = requests.get(url)
        headers = response.headers
        insecure_headers = []
        if "X-Frame-Options" not in headers:
            insecure_headers.append("X-Frame-Options missing")
        if "Content-Security-Policy" not in headers:
            insecure_headers.append("Content-Security-Policy missing")
        if insecure_headers:
            return True, ", ".join(insecure_headers)
        return False, "No insecure headers detected."
    except Exception as e:
        return False, f"Error: {str(e)}"

def directory_bruteforce(url):
    directories = ['admin', 'login', 'dashboard', 'config', 'uploads']
    found_directories = []
    for directory in directories:
        test_url = f"{url}/{directory}/"
        try:
            response = requests.get(test_url)
            if response.status_code == 200:
                found_directories.append(test_url)
        except Exception:
            pass
    if found_directories:
        return True, f"Accessible directories: {', '.join(found_directories)}"
    return False, "No accessible directories found."

def generate_report(test_results, target):
    sanitized_target = re.sub(r'[^a-zA-Z0-9]', '_', target)
    report_path = f"{REPORT_DIR}/report_{sanitized_target}.html"
    
    with open(report_path, "w") as report:
        report.write(f"<html><head><title>Security Test Report for {target}</title></head><body>")
        report.write(f"<h1>Security Test Report for {target}</h1>")
        report.write("<ul>")
        for test_name, result, message in test_results:
            color = "green" if not result else "red"
            report.write(f"<li style='color:{color};'><strong>{test_name}:</strong> {message}</li>")
        report.write("</ul>")
        report.write("</body></html>")
    
    return report_path
    
def run_tests(url):
    print(colored(f"Running security tests for {url}", "blue"))
    
    test_results = []
    
    sql_injection_result, sql_injection_message = sql_injection_test(url)
    print(colored(sql_injection_message, "green" if not sql_injection_result else "red"))
    test_results.append(("SQL Injection", sql_injection_result, sql_injection_message))
    
    xss_result, xss_message = xss_test(url)
    print(colored(xss_message, "green" if not xss_result else "red"))
    test_results.append(("XSS", xss_result, xss_message))
    
    csrf_result, csrf_message = csrf_test(url)
    print(colored(csrf_message, "green" if not csrf_result else "red"))
    test_results.append(("CSRF", csrf_result, csrf_message))
    
    insecure_headers_result, insecure_headers_message = insecure_headers_test(url)
    print(colored(insecure_headers_message, "green" if not insecure_headers_result else "red"))
    test_results.append(("Insecure Headers", insecure_headers_result, insecure_headers_message))
    
    bruteforce_result, bruteforce_message = directory_bruteforce(url)
    print(colored(bruteforce_message, "green" if not bruteforce_result else "red"))
    test_results.append(("Directory Bruteforcing", bruteforce_result, bruteforce_message))
    
    report_path = generate_report(test_results, url)
    print(f"Report saved to {report_path}")

def update_tool():
    try:

        if not os.path.exists('.git'):
            print("This tool is not a Git repository. Please clone it from the repository.")
            return
        
        print("Checking for updates...")
        subprocess.run(['git', 'fetch'], check=True)

        status = subprocess.run(['git', 'status'], stdout=subprocess.PIPE, text=True, check=True)
        
        if "Your branch is up to date" in status.stdout:
            print("Your tool is already up-to-date.")
        else:
            subprocess.run(['git', 'pull'], check=True)
            print("Tool updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the update process: {str(e)}")

def main_menu():
    print("Security Testing Tool")
    print("1. Run security tests")
    print("2. Update tool")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        target_url = input("Enter the target URL (e.g., http://example.com): ")
        run_tests(target_url)  
    elif choice == "2":
        update_tool()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main_menu()

