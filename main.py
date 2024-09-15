from tests.test_sql_injection import test_sql_injection
from tests.test_xss import test_xss
from tests.test_headers import test_security_headers
from tests.test_https import test_https
from tests.test_session import test_session_management

def run_all_tests(target):
    print(f"Running security tests for {target}")
    test_sql_injection(target)
    test_xss(target)
    test_security_headers(target)
    test_https(target)
    test_session_management(target)

