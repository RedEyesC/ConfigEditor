from Core.DataExporter import ExportData
from Core.DataLoader import LoadTableFile
from Core.Utils import SplitFileAndSheetName, StandardizePath


def Run(conf: str, targetPath: str, targets: str, dataTargetPath: str, dataTargets: str):
    # 加载定义文件
    tables: dict = LoadSchema(conf, targetPath, dataTargetPath)

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
        temp["output"] = dataTarget + "/config_" + name
        temp["input"] = StandardizePath(targetPath + "/" + data.GetField("input"))
        temp["mode"] = data.GetField("mode")
        temp["index"] = data.GetField("index")
        tables[name] = temp

    return tables


def LoadDatas(tables: dict, targets: str):
    recordsByTables: list = []

    files = targets.split("|")

    for file in files:
        table = tables[file]
        [actualFile, sheetName] = SplitFileAndSheetName(table["input"])
        record = LoadTableFile(table, actualFile, sheetName)

        recordsByTables.append([table, record])

    return recordsByTables


def ProcessDataTarget(recordsByTables: list, dataTargets: str):
    fonts = dataTargets.split("|")
    for font in fonts:
        for info in recordsByTables:
            ExportData(info[0], info[1], font)
