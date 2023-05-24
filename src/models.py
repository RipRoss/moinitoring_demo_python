from typing import Optional
from pydantic import BaseModel


class Address(BaseModel):
    house_number: int
    house_name: Optional[str]
    street_name: str
    post_code: str


class User(BaseModel):
    first_name: str
    last_name: str
    addresses: list[Address]
    username: str
    password: str  # for the sake of the demonstration, this will be plaintext
    email: str
