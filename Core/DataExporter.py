def ExportData(table, records, dataTarget):
    if dataTarget == "json":
        ExportJson(records)
    elif dataTarget == "bin":
        ExportBin(records)


def ExportJson(records):
    x = ""
    for record in records:
        pass


def ExportBin(records):
    pass
