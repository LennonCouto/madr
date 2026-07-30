import re


def sanitize_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def sanitize_name(name: str) -> str:
    return sanitize_spaces(name).title()


def normalize_title(title: str) -> str:
    return sanitize_spaces(title).title()
