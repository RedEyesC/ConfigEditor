def TryParseValue(value, type):
    if type == "str":
        return TryParseToString(value)
    elif type == "int":
        return TryParseToInt(value)
    elif type == "arrayInt":
        return TryParseToInt(value)
    elif type == "arrayStr":
        return TryParseToInt(value)
    else:
        print("识别到未定义类型" + type)
        exit(-1)


def TryParseToString(value: str):
    return value


def TryParseToInt(value: str):
    return int(value)


def TryParseToArrayInt(value: str):
    pass


def TryParseToArrayString(value: str):
    pass
