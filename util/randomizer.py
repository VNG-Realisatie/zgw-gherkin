import random
import string


def create_random_string(size=12):
    return "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(size)
    )


def create_random_letter(size=12):
    return "".join(
        random.SystemRandom().choice(string.ascii_letters) for _ in range(size)
    )


def create_random_number(size=9):
    return "".join(random.SystemRandom().choice(string.digits) for _ in range(size))
