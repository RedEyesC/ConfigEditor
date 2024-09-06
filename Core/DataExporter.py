def ExportData(table, records, dataTarget):
    if dataTarget == "json":
        ExportJson(table, records)
    elif dataTarget == "bin":
        ExportBin(table, records)


def ExportJson(table, records):
    x = ""
    for record in records:
        pass


class BinData:
    type: int
    value: any

    def __init__(self, type, value):
        self.type = type
        self.value = value


def ExportBin(table, records):
    # 插入版本标志
    byteArray: bytes = "DE1.0".encode("utf-8")
    byteArray += b"\x00"

    # 存放实际含有的数据
    binMap: dict[str, int] = {}
    binList: list[BinData] = []

    # 统计需要存放的数据
    for record in records:
        data = record.data

    # 生成2进制表头，用于记录索引对应的偏移

    # 生成保存的数组

    # 生成文件
    with open(table["output"] + ".bin", "wb") as file:
        file.write(byteArray)
        file.close()
