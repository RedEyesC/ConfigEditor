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
        print("识别到未定义数据类型" + type)
        exit(-1)


def TryParseToString(value: str):
    if value == None:
        return ""

    return str(value)


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


def TryParseMode(model, fields, index):
    if model == "map":
        return TryParseToMap(fields, index)
    elif model == "list":
        return TryParseToList(fields, index)
    else:
        print("识别到未定义格式类型" + model)
        exit(-1)


def TryParseToMap(fields, index):
    data = {}
    for key in fields:
        data[key] = GetField(fields, key)

    return data


def TryParseToList(fields, index):
    keys = index.split(",")

    data = CreateNestedDict(keys, fields)

    return data


def CreateNestedDict(keys, fields):
    if not keys:
        data = {}
        for name in fields:
            data[name] = GetField(fields, name)

        return data

    return {GetField(fields, keys[0]): CreateNestedDict(keys[1:], fields)}


def GetField(fields, fieldName: str):
    if fieldName in fields:
        return fields[fieldName]
    else:
        return None
