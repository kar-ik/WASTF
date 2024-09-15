from framework import send_request, log_to_report

def test_https(url):
    if not url.startswith("https://"):
        log_to_report(f"[-] {url} is not using HTTPS")
        print(f"[-] {url} is not using HTTPS")
    else:
        log_to_report(f"[+] {url} is using HTTPS")
        print(f"[+] {url} is using HTTPS")


