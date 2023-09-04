def to_camel_case(string: str) -> str:
    string = "".join(word.capitalize() for word in string.split("_"))
    string = string[0].lower() + string[1:]
    return string
