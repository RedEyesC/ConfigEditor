from Core.DataExporter import ExportData
from Core.DataLoader import LoadFileTag, LoadTableFile
from Core.Utils import SplitFileAndSheetName, StandardizePath


def Run(*args):

    targetPath = args[0]
    targets = args[1]
    dataTargetPath = args[2]
    dataTargets = args[3]

    tables: dict
    if len(args) >= 5:
        # 加载定义文件
        conf = args[4]
        tables: dict = LoadSchema(conf, targetPath, dataTargetPath)
    else:
        tables: dict = LoadSchemaBytarget(targets, targetPath, dataTargetPath)

    # 根据定义文件加载配置表
    recordsByTables: list = LoadDatas(tables, targets)

    # 输出配置表
    ProcessDataTarget(recordsByTables, dataTargets)


def LoadSchema(conf: str, targetPath: str, dataTargetPath: str):
    recordType = {
        "name": "table",
        "output": "",
        "mode": "list",
        "index": "name",
    }

    tables: dict = {}

    [actualFile, sheetName] = SplitFileAndSheetName(StandardizePath(conf))
    records = LoadTableFile(recordType, actualFile, sheetName)

    dataTarget = StandardizePath(dataTargetPath)

    for data in records:
        temp: dict[str, str] = {}
        name: str = data.GetField("name")
        temp["name"] = name
        temp["output"] = dataTarget + "/" + name
        temp["input"] = StandardizePath(targetPath + "/" + data.GetField("input"))
        temp["mode"] = data.GetField("mode")
        temp["index"] = data.GetField("index")
        tables[name] = temp

    return tables


def LoadSchemaBytarget(targets: str, targetPath: str, dataTargetPath: str):
    dataTarget = StandardizePath(dataTargetPath)

    tables: dict = {}

    targetList = targets.split("|")
    for targe in targetList:

        input = StandardizePath(targetPath + "/" + targe + ".xlsx")
        mode = ""
        index = ""

        # 获取配置表的定义格
        attrs = LoadFileTag(input)

        for attr in attrs:
            if attr == "map":
                mode = "map"
            elif attr == "list":
                mode = "list"
            elif attr.startswith("key_"):
                indexs: str = attr[4:]
                index = indexs.replace("|", ",")

        temp: dict[str, str] = {}
        name: str = targe
        temp["name"] = targe
        temp["output"] = dataTarget + "/" + targe
        temp["input"] = input
        temp["mode"] = mode
        temp["index"] = index
        tables[name] = temp

    return tables


def LoadDatas(tables: dict, targets: str):
    recordsByTables: list = []

    files = targets.split("|")

    for file in files:
        table = tables[file]
        [actualFile, sheetName] = SplitFileAndSheetName(table["input"])
        datas = LoadTableFile(table, actualFile, sheetName)

        recordsByTables.append([table, datas])

    return recordsByTables


def ProcessDataTarget(recordsByTables: list, dataTargets: str):
    fonts = dataTargets.split("|")
    for font in fonts:
        for info in recordsByTables:
            ExportData(info[0], info[1], font)
