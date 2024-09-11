import json


def ExportData(table, records, dataTarget):
    if dataTarget == "json":
        ExportJson(table, records)
    elif dataTarget == "bin":
        ExportBin(table, records)


def ExportJson(table, records):
    x = {}
    for record in records:
        DataMerge(record.data, x)

    with open(table["output"] + ".json", "w", encoding="utf-8") as file:
        json.dump(x, file, indent=2, ensure_ascii=False)


def DataMerge(data, x: dict):
    for key in data:
        value = data[key]

        if isinstance(value, dict):
            sub = x[key] if key in x else {}

            x[key] = DataMerge(value, sub)
        else:
            x[key] = value

    return x


def ExportBin(table, records):
    offset: int = 0

    # 插入版本标志(以00为结尾)
    byteArray: bytearray = bytearray("DE1.0", "utf-8")
    byteArray += b"\x00"
    offset = offset + len(byteArray)

    # 合并好数据
    x = {}
    for record in records:
        DataMerge(record.data, x)

    binMap: dict = {}
    # 生成入口dict

    data2Bin(x, binMap, byteArray)

    # 生成文件
    with open(table["output"] + ".bin", "wb") as file:
        file.write(byteArray)
        file.close()


def data2Bin(data, binMap, byteArray: bytearray):
    offset = len(byteArray)

    if isinstance(data, dict):

        # 2进制字典结构由1字节的类型定义,2字节的长度定义,4字节的键合集定义，字典长度x(4字节键值索引) 组成
        binData = b"\x01" + len(data).to_bytes(2, byteorder="big", signed=True)

        binLen = 7 + len(data) * 4

        # 预填充
        byteArray[offset:offset] = bytearray(binLen)

        binData = binData + data2Bin(list(data.keys()), binMap, byteArray)

        for key in data:
            binData = binData + data2Bin(data[key], binMap, byteArray)

        # 删除预填充
        del byteArray[offset : offset + binLen]

    if isinstance(data, list):
        # 2进制列表结构由1字节的类型定义,2字节的长度定义,列表长度x4字节值索引 组成
        binData = b"\x02" + len(data).to_bytes(2, byteorder="big", signed=True)
        binLen = 3 + len(data) * 4

        # 预填充
        byteArray[offset:offset] = bytearray(binLen)

        for value in data:
            binData = binData + data2Bin(value, binMap, byteArray)

        # 删除预填充
        del byteArray[offset : offset + binLen]

    elif isinstance(data, int):
        # 2进制int结构由1字节的类型定义,8字节的值定义
        binData = b"\x03" + data.to_bytes(8, byteorder="big", signed=True)

    elif isinstance(data, str):
        # 2进制str结构由1字节的类型定义,2字节的长度定义,utf8编码的字符串长度组成
        strData = data.encode("utf-8")
        binData = b"\x04" + len(strData).to_bytes(2, byteorder="big", signed=False)
        binData = binData + strData

    if binData in binMap:
        return binMap[binData]
    else:
        byteArray[offset:offset] = bytearray(binData)
        binOffset = offset.to_bytes(4, byteorder="big", signed=False)
        binMap[binData] = binOffset

        return binOffset
