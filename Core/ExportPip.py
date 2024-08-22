from Core.DataExporter import ExportData
from Core.DataLoader import LoadTableFile, TData
from Core.Utils import StandardizePath


def Run(conf: str, targetPath: str, targets: str, dataTargetPath: str, dataTargets: str):
    # 加载定义文件
    tables: dict = LoadSchema(conf, targetPath, dataTargetPath)

    # 根据定义文件加载配置表
    recordsByTables: list = LoadDatas(tables, targets)

    # 输出配置表
    ProcessDataTarget(recordsByTables, dataTargets)


def LoadSchema(conf: str, targetPath: str, dataTargetPath: str):
    recordType = {
        "name": "str",
        "input": "str",
        "mode": "str",
        "index": "str",
    }

    tables: dict = {}

    records = LoadTableFile(recordType, conf)

    dataTarget = StandardizePath(dataTargetPath)

    for r in records:
        data: TData = r.data
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

    inputFiles = []

    for inputFile in inputFiles:
        # TODO 有需求的话，可以在这扩展多分支合并
        record = LoadTableFile("", "")
        table = tables[inputFile]
        recordsByTables.append([table, record])

    return recordsByTables


def ProcessDataTarget(recordsByTables: list, dataTargets: str):
    dataTargets = []
    for dataTarget in dataTargets:
        for info in recordsByTables:
            ExportData(info[0], info[1], dataTarget)
