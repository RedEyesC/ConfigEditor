def StandardizePath(path: str):
    return path.replace("\\", "/")


def SplitFileAndSheetName(url: str):
    sheetSepIndex = url.find("@")
    splitIndex = url.rfind("/")
    if sheetSepIndex < 0:
        return [url, None]
    else:
        return [url[0 : splitIndex + 1] + url[(sheetSepIndex + 1) :], url[splitIndex + 1 : sheetSepIndex]]

def ParseArgs(args):
    result = {}
    key = None
    for item in args:
        if item.startswith('-'):
            key = item.lstrip('-')
        else:
            if key:
                result[key] = item
                key = None
    return result