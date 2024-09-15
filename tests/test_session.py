from framework import send_request, log_to_report

def test_session_management(url):
    response = send_request(url)
    
    if response:
        cookies = response.cookies
        for cookie in cookies:
            if not cookie.secure:
                log_to_report(f"[-] Session cookie '{cookie.name}' is not marked Secure")
                print(f"[-] Session cookie '{cookie.name}' is not marked Secure")
            if not cookie.has_nonstandard_attr('HttpOnly'):
                log_to_report(f"[-] Session cookie '{cookie.name}' is not marked HttpOnly")
                print(f"[-] Session cookie '{cookie.name}' is not marked HttpOnly")
    else:
        log_to_report(f"[!] Could not retrieve cookies for {url}")


