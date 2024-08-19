from Core.DataExporter import ExportJson
from Core.DataLoader import LoadTableFile, TData


class TableDataInfo:
    table: any
    records: any

    def __init__(self, table: any, records: any):
        self.table = table
        self.records = records


def Main():
    LoadSchema()
    LoadDatas()
    ProcessDataTarget()


def LoadSchema():
    recordType = {
        "name": "string",
        "input": "string",
        "mode": "string",
        "index": "string",
    }

    records = LoadTableFile(recordType, "", "")

    for r in records:
        data: TData = r.data
        name = data.GetField("name")
        input = data.GetField("input")
        mode = data.GetField("mode")
        index = data.GetField("index")


def LoadDatas():
    recordsByTables = {}
    inputFiles = []

    # 由上一步获取到的
    tables = []
    for inputFile in inputFiles:
        record = LoadTableFile("", "")

        table = tables[inputFile]
        # TODO 有需求的话，可以在这扩展多分支合并
        recordsByTables[table.name] = TableDataInfo(table, record)

    return recordsByTables


def ProcessDataTarget(recordsByTables):
    DataTargets = []
    for mission in DataTargets:
        for info in recordsByTables:
            ExportJson(info.table, info.record)
