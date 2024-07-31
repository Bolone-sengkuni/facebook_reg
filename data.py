from dataclasses import dataclass


@dataclass
class RegisterData:
    first_name: str
    last_name: str
    email: str
    password: str


@dataclass
class Message:
    sender: str
    title: str
    time: str
    text: str    