def ExportData(table, records, dataTarget):
    if dataTarget == "json":
        ExportJson(table, records)
    elif dataTarget == "bin":
        ExportBin(table, records)


def ExportJson(table, records):
    pass


def ExportBin(table, records):
    pass
