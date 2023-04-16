import secrets
import string


def generate(use_letters, use_digits, use_punctuation, pass_length):
    alphabet = ''

    if use_letters:
        letters = string.ascii_letters
        alphabet += letters
    if use_digits:
        digits = string.digits
        alphabet += digits
    if use_punctuation:
        punctuation = string.punctuation
        alphabet += punctuation

    pwd = ''
    for i in range(pass_length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd