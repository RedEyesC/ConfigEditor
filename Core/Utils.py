def StandardizePath(path: str):
    return path.replace("\\", "/")


def SplitFileAndSheetName(url: str):
    sheetSepIndex = url.find("@")
    splitIndex = url.rfind("/")
    if sheetSepIndex < 0:
        return [url, None]
    else:
        return [url[0 : splitIndex + 1] + url[(sheetSepIndex + 1) :], url[splitIndex + 1 : sheetSepIndex]]
