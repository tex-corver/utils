import random
import string


def make_string() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))
