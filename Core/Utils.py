def StandardizePath(path: str):
    return path.replace("\\", "/")


def SplitFileAndSheetName(url: str):
    sheetSepIndex = url.find("@")
    if sheetSepIndex < 0:
        return [url, None]
    else:
        return [url[(sheetSepIndex + 1) :], url[0:sheetSepIndex]]
