from framework import send_request, log_to_report

def test_xss(url):
    xss_payload = "<script>alert('XSS')</script>"
    response = send_request(url + xss_payload)
    
    if response and xss_payload in response.text:
        log_to_report(f"[!] Possible XSS vulnerability detected at {url}")
        print(f"[!] XSS detected at {url}")
    else:
        log_to_report(f"[*] No XSS vulnerability detected at {url}")
        print(f"[*] No XSS detected at {url}")

