# MIT License -> LISCENCE.mit

from string import ascii_letters, digits, punctuation
import random
from uuid import UUID

def password_gen(lenght: int):
    return "".join(random.sample(ascii_letters + digits + punctuation, lenght))

def uuid_to_hex(uuid: str) -> str:
    return UUID(uuid).hex
