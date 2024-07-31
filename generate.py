import random
import string


def generate_password(length=12, use_uppercase=True, 
                      use_lowercase=True, use_digits=True, use_special=True) -> str:
    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    # Create a list of available characters based on the parameters
    available_characters = []
    if use_uppercase:
        available_characters.extend(uppercase_letters)
    if use_lowercase:
        available_characters.extend(lowercase_letters)
    if use_digits:
        available_characters.extend(digits)
    if use_special:
        available_characters.extend(special_characters)

    # Check if at least one character set is selected
    if not available_characters:
        raise ValueError("At least one character set must be selected.")

    password = ''.join(random.choice(available_characters) for _ in range(length))

    # Check if the password contains characters from each selected set
    while use_uppercase and not any(c in uppercase_letters for c in password) or \
          use_lowercase and not any(c in lowercase_letters for c in password) or \
          use_digits and not any(c in digits for c in password) or \
          use_special and not any(c in special_characters for c in password):
        password = ''.join(random.choice(available_characters) for _ in range(length))

    return password