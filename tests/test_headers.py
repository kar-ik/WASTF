from framework import send_request, log_to_report

def test_security_headers(url):
    response = send_request(url)
    
    if response:
        headers = response.headers
        log_to_report(f"[*] Checking security headers for {url}")
        
        required_headers = ["X-Content-Type-Options", "X-Frame-Options", "Strict-Transport-Security"]
        for header in required_headers:
            if header in headers:
                log_to_report(f"[+] {header} is present")
                print(f"[+] {header} is present")
            else:
                log_to_report(f"[-] {header} is missing")
                print(f"[-] {header} is missing")
    else:
        log_to_report(f"[!] Could not fetch headers for {url}")


