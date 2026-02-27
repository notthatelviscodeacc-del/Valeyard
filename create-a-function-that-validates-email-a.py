```python
import re

def validate_email(email: str) -> bool:
    """
    Validates an email address using regex pattern matching.
    
    Args:
        email: The email address string to validate.
    
    Returns:
        True if the email is valid, False otherwise.
    """
    if not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email) is None:
        return False

    local, domain = email.rsplit('@', 1)

    if local.startswith('.') or local.endswith('.'):
        return False

    if '..' in local or '..' in domain:
        return False

    if domain.startswith('-') or domain.endswith('-'):
        return False

    return True


if __name__ == "__main__":
    test_emails = [
        ("user@example.com", True),
        ("user.name+tag@domain.co.uk", True),
        ("user123@sub.domain.org", True),
        ("invalid-email", False),
        ("missing@domain", False),
        ("@nodomain.com", False),
        ("noatsign.com", False),
        (".startdot@domain.com", False),
        ("enddot.@domain.com", False),
        ("double..dot@domain.com", False),
        ("user@-domain.com", False),
        ("user@domain-.com", False),
        ("", False),
        (None, False),
    ]

    for email, expected in test_emails:
        result = validate_email(email)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] validate_email({email!r}) = {result} (expected {expected})")
```