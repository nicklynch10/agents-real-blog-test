"""
Utility functions for validating common data types in the Flask API.
"""

import re
from typing import Tuple

# Email validation regex pattern
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

# Password requirements:
# - Minimum 8 characters
# - At least one uppercase letter
# - At least one lowercase letter
# - At least one digit
# - At least one special character
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate an email address format.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"

    if not EMAIL_REGEX.match(email):
        return False, "Invalid email format"

    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate a password against security requirements.
    
    Args:
        password (str): The password to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not PASSWORD_REGEX.match(password):
        return False, (
            "Password must contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character"
        )

    return True, ""

__all__ = ['validate_email', 'validate_password']
