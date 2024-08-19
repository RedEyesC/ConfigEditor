def CheckType(value, type):
    if type == "string":
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


def TryParseToString(value):
    pass


def TryParseToInt(value):
    pass


def TryParseToArrayInt(value):
    pass


def TryParseToArrayString(value):
    pass
