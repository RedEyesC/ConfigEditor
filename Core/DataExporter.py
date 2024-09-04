def ExportData(table, data, dataTarget):
    if dataTarget == "json":
        ExportJson(data)
    elif dataTarget == "bin":
        ExportBin(data)


def ExportJson(data):
    pass


def ExportBin(data):
    pass
