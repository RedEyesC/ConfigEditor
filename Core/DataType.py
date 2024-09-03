def TryParseValue(value, type):
    if type == "str":
        return TryParseToString(value)
    elif type == "int":
        return TryParseToInt(value)
    elif type == "arrayInt":
        return TryParseToArrayInt(value)
    elif type == "arrayStr":
        return TryParseToArrayString(value)
    else:
        print("识别到未定义类型" + type)
        exit(-1)


def TryParseToString(value: str):
    if value == None:
        return ""

    return value


def TryParseToInt(value: str):
    if value == None:
        return 0

    return int(value)


def TryParseToArrayInt(value: str):
    if value == None:
        return []

    value = value.replace("[", "").replace("]", "")
    arrayInt = []
    for str in value.split(","):
        arrayInt.append(TryParseToInt(str))

    return arrayInt


def TryParseToArrayString(value: str):
    if value == None:
        return []

    value = value.replace("[", "").replace("]", "")
    arrayString = []
    for str in value.split(","):
        arrayString.append(TryParseToString(str))

    return arrayString
