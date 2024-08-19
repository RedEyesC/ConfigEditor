import math
import openpyxl


class Cell:
    row: int
    column: int
    value: any

    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value


class Title:
    name: str
    index: int
    root: bool
    subTitle: dict[str, str]

    def __init__(self, name: str, index: int, root: bool = False):
        self.name = name
        self.index = index
        self.root = root
        self.AddSubTitle("value", name)

    def AddSubTitle(self, tag, value):
        self.subTitle[tag] = value


class TitleRow:
    title: Title
    row: list[Cell]

    def __init__(self, title: str, row: list[Cell]):
        self.title = title
        self.row = row


class RowColumnSheet:
    rawUrl: str
    name: str

    titles: dict[int, Title]
    sheetName: str
    cells: list[list[Cell]]

    rows: list[any]

    def __init__(
        self, rawUrl: str, name: str, sheetName: str, titles: dict[int, Title], cells: list[list[Cell]]
    ):
        self.rawUrl = rawUrl
        self.name = name

        self.titles = titles
        self.sheetName = sheetName
        self.cells = cells
        self.rows = []

    def Load(self):
        for row in self.cells:
            if self.IsBlankRow(row):
                continue

            self.rows.append([self.GetRowTag(row), self.ParseOneLineTitleRow(row)])

    def IsBlankRow(self, row):
        for title in self.title:
            v = row[title.index].value
            if v != None:
                return False

        return True

    def GetRowTag(self, row):
        if len(row) > 0:
            return row[0].value
        else:
            return ""

    def ParseOneLineTitleRow(self, row):
        fields = {}

        for title in self.title:
            fields[title.name] = TitleRow(title, row)

        return fields


class TData:
    fields: dict

    def __init__(self, sheet, row, recordType):
        pass

    def GetField(self, fieldName: str):
        if fieldName in self.fields:
            return self.fields[fieldName]
        else:
            return None


class Record:
    data: any
    source: str
    tags: str

    def __init__(self, data: any, source: str, tags: str):
        self.data = data
        self.source = source
        self.tags = tags


# 之后整理的时候移除DataLoader，现在暂时放这里
def LoadTableFile(recordType, actualFile, sheetName):
    datas: list[Record] = []

    sheets: list[RowColumnSheet] = LoadRawSheets(actualFile, sheetName)
    for sheet in sheets:
        for r in sheet.rows:
            row: dict[str, TitleRow] = r[0]
            tagStr: str = r[1]

            if IsIgnoreTag(tagStr):
                continue

            # 确认数据类型
            data = TData(sheet, row, recordType)
            datas.append(Record(data, sheet.rawUrl, tagStr))

    return datas


def LoadRawSheets(rawUrl, sheetName):
    sheets: list[RowColumnSheet] = []

    workbook = openpyxl.load_workbook(rawUrl, read_only=True)  # 打开文件

    for name in workbook.sheetnames:
        if sheetName == name or sheetName == None:
            worksheet = workbook[name]
            print(f"正在处理子表: {name}")
            sheet = ParseRawSheet(rawUrl, sheetName, worksheet, name)
            sheets.append(sheet)

    workbook.close()
    return sheets


def ParseRawSheet(rawUrl: str, sheetName: str, reader, name: str):
    metaStr = reader["A1"]
    state = TryParseMeta(metaStr)
    if state < 0:
        print("非法配置格式错误")
        exit(-1)

    if state > 0:
        orientRow = True
    else:
        orientRow = False

    cells = ParseRawSheetContent(reader, orientRow)
    titles = ParseTitle(cells)
    RemoveNotDataRow(cells)
    sheet = RowColumnSheet(rawUrl, sheetName, name, titles, cells)
    sheet.Load()
    return sheet


def TryParseMeta(metaStr: str):
    if metaStr == "" | metaStr.startswith("##"):
        return -1

    orientRow = 1

    attrs = metaStr[2:].split("#")
    for attr in attrs:
        if attr == "var":
            continue

        if attr == "row":
            orientRow = 1
            continue

        if attr == "column":
            orientRow = 0

    return orientRow


def ParseRawSheetContent(reader, orientRow: bool):
    originRows: list[list[Cell]] = []
    rowIndex: int = 0

    for rowData in reader.rows:
        row: list[Cell] = []
        for i in range(len(rowData)):
            row.append(Cell(rowIndex, i, row[i]))

        originRows.append(row)

        rowIndex == rowIndex + 1

    finalRows: list[list[Cell]] = []

    if orientRow:
        finalRows = orientRow
    else:
        maxColumn: int = 0

        for row in originRows:
            rowLen = len(row)
            maxColumn = math.max(rowLen, maxColumn)

        finalRows: list[list[Cell]] = []

        for i in range(len(maxColumn)):
            row: list[Cell] = []

            for j in range(len(originRows)):
                if i < len(originRows):
                    row.append(originRows[j][i])
                else:
                    row.append(Cell(j + 1, i, None))

    return finalRows


def ParseTitle(cells: list[list[Cell]]):
    titles = []

    topTitleRowIndex = TryFindTopTitle(cells)
    if topTitleRowIndex < 0:
        print("没有定义任何有效 标题行")
        exit(-1)

    ParseSubTitles(titles, cells, topTitleRowIndex + 1)

    if len(titles) < 0:
        print("没有定义任何有效 标题行")
        exit(-1)

    return titles


def TryFindTopTitle(cells: list[list[Cell]]):
    rowIndex = -1

    for i in range(len(cells)):
        row = cells[i]
        rowLen = len(row)
        if rowLen == 0 or (not row[0].startswith("##")):
            break

        rowTag: str = row[0]
        attrs = rowTag[2:].split("#")
        if "var" in attrs:
            rowIndex = i
            break

    return rowIndex


def ParseSubTitles(titles: dict[int, Title], cells: list[list[Cell]], excelRowIndex: int):
    row = cells[excelRowIndex]

    rowLen = len(row)

    for i in range(rowLen):
        cell = row[i]
        name: str = cell.Value
        if IsIgnoreTitle(name):
            continue

        titles[i] = Title(name, i)

    for i in range(excelRowIndex, len(cells)):
        row = cells[i]
        rowLen = len(row)
        if rowLen == 0 or (not row[0].startswith("##")):
            break

        tag: str = row[0][2:]

        for j in range(rowLen):
            cell = row[j]
            value: str = cell.Value
            titles[i].AddSubTitle(tag, value)


def TryFindNextSubFieldRowIndex(cells, excelRowIndex):
    if excelRowIndex < len(cells):
        return -1


def IsIgnoreTitle(title: str):
    return title.startswith("#")


def IsIgnoreTag(tagStr: str):
    return tagStr == "##"


def RemoveNotDataRow(cells: list[list[Cell]]):
    for row in cells[::-1]:
        rowLen = len(row)

        if rowLen == 0 or row[0].startswith("##"):
            cells.remove(row)
