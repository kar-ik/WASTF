from framework import send_request, log_to_report

def test_sql_injection(url):
    sql_payload = "' OR '1'='1"
    response = send_request(url + sql_payload)
    
    if response and ("mysql" in response.text.lower() or "syntax" in response.text.lower()):
        log_to_report(f"[!] Possible SQL Injection vulnerability detected at {url}")
        print(f"[!] SQL Injection detected at {url}")
    else:
        log_to_report(f"[*] No SQL Injection vulnerability detected at {url}")
        print(f"[*] No SQL Injection detected at {url}")


