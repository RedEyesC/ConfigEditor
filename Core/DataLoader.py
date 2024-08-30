import math
import openpyxl

from Core.DataType import TryParseValue


class Cell:
    row: int
    column: int
    value: str

    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value


class Title:
    name: str
    index: int

    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.subTitle: dict[str, str] = {}

        self.AddSubTitle("value", name)

    def AddSubTitle(self, tag, value):
        self.subTitle[tag] = value

    def GetSubTitle(self, tag):
        return self.subTitle[tag]


class TitleRow:
    titles: dict[int, Title]
    row: list[Cell]
    tag: str

    def __init__(self, titles: dict[int, Title], row: list[Cell]):
        self.titles = titles
        self.row = row
        self.tag = self.GetRowTag()

    def GetRowTag(self):
        if len(self.row) > 0:
            return self.row[0].value
        else:
            return ""


class RowColumnSheet:
    rawUrl: str

    titles: dict[int, Title]
    sheetName: str
    cells: list[list[Cell]]

    rows: list[TitleRow]

    def __init__(self, rawUrl: str, sheetName: str, titles: dict[int, Title], cells: list[list[Cell]]):
        self.rawUrl = rawUrl

        self.titles = titles
        self.sheetName = sheetName
        self.cells = cells
        self.rows = []

        for row in self.cells:
            if self.IsBlankRow(row):
                continue
            self.rows.append(TitleRow(self.titles, row))

    def IsBlankRow(self, row: list[Cell]):
        for index in self.titles:
            title = self.titles[index]
            v = row[title.index].value
            if v != None:
                return False

        return True


class Record:
    fields: dict
    data: dict

    def __init__(self, titleRow: TitleRow, recordType):
        titles = titleRow.titles
        row = titleRow.row

        self.fields = {}
        self.data = {}

        for index in titles:
            title = titleRow.titles[index]
            key = title.name
            type = title.GetSubTitle("type")

            self.SetField(key, TryParseValue(row[index], type))

        model = recordType["mode"]

        if model == "map":
            for key in self.fields:
                self.data[key] = self.GetField(key)
        elif model == "list":
            keys = recordType["index"]

            tempData = self.data
            for key in keys:
                value = self.GetField(key)
                tempData[value] = {}
                tempData = tempData[value]

            for key in self.fields:
                tempData[key] = self.GetField(key)

    def GetField(self, fieldName: str):
        if fieldName in self.fields:
            return self.fields[fieldName]
        else:
            return None

    def SetField(self, fieldName: str, value):
        self.fields[fieldName] = value


def LoadTableFile(recordType, actualFile, sheetName):
    datas: list[Record] = []

    sheets: list[RowColumnSheet] = LoadRawSheets(actualFile, sheetName)
    for sheet in sheets:
        for TitleRow in sheet.rows:
            if IsIgnoreTag(TitleRow.tag):
                continue

            # 确认数据类型
            data = Record(TitleRow, recordType)
            datas.append(data)

    return datas


def LoadRawSheets(rawUrl, sheetName):
    sheets: list[RowColumnSheet] = []

    workbook = openpyxl.load_workbook(rawUrl, read_only=True)  # 打开文件

    for name in workbook.sheetnames:
        if sheetName == name or sheetName == None:
            worksheet = workbook[name]
            print(f"正在处理子表: {name}")
            sheet = ParseRawSheet(
                rawUrl,
                name,
                worksheet,
            )
            sheets.append(sheet)

    workbook.close()
    return sheets


def ParseRawSheet(rawUrl: str, sheetName: str, reader):
    metaStr = reader["A1"].value
    state = TryParseMeta(metaStr)
    if state < 0:
        print("A1单元格非法配置格式")
        exit(-1)

    if state > 0:
        orientRow = True
    else:
        orientRow = False

    cells = ParseRawSheetContent(reader, orientRow)
    titles = ParseTitle(cells)
    RemoveNotDataRow(cells)
    sheet = RowColumnSheet(rawUrl, sheetName, titles, cells)
    return sheet


def TryParseMeta(metaStr: str):
    if (metaStr == "") or (not metaStr.startswith("##")):
        return -1

    orientRow = 1

    attrs = metaStr[2:].split("##")
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
            row.append(Cell(rowIndex, i, rowData[i].value))

        originRows.append(row)

        rowIndex == rowIndex + 1

    finalRows: list[list[Cell]] = []

    if orientRow:
        finalRows = originRows
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
    topTitleRowIndex = TryFindTopTitle(cells)
    if topTitleRowIndex < 0:
        print("没有定义任何有效 标题行")
        exit(-1)

    titles = {}
    ParseSubTitles(titles, cells, topTitleRowIndex)

    if len(titles) < 0:
        print("没有定义任何有效 标题行")
        exit(-1)

    return titles


def TryFindTopTitle(cells: list[list[Cell]]):
    rowIndex = -1

    for i in range(len(cells)):
        row = cells[i]
        rowLen = len(row)

        if rowLen == 0:
            break

        rowTag: str = row[0].value

        if rowTag == None:
            break

        if not rowTag.startswith("##"):
            break

        attrs = rowTag[2:].split("##")
        if "var" in attrs:
            rowIndex = i
            break

    return rowIndex


def ParseSubTitles(titles: dict[int, Title], cells: list[list[Cell]], excelRowIndex: int):
    row = cells[excelRowIndex]

    rowLen = len(row)

    for i in range(rowLen):
        cell = row[i]
        name: str = cell.value
        if (name == None) or IsIgnoreTitle(name):
            continue

        titles[i] = Title(name, i)

    for i in range(excelRowIndex + 1, len(cells)):
        row = cells[i]
        rowLen = len(row)
        if rowLen == 0:
            break

        rowtag = row[0].value

        if (rowtag == None) or (not rowtag.startswith("##")):
            break

        tag: str = row[0].value[2:]

        for j in range(rowLen):
            cell = row[j]
            value: str = cell.value

            if j in titles:
                titles[j].AddSubTitle(tag, value)


def TryFindNextSubFieldRowIndex(cells, excelRowIndex):
    if excelRowIndex < len(cells):
        return -1


def IsIgnoreTitle(title: str):
    return title.startswith("##")


def IsIgnoreTag(tagStr: str):
    return tagStr == "##"


def RemoveNotDataRow(cells: list[list[Cell]]):
    for row in cells[::-1]:
        rowLen = len(row)
        rowtag = row[0].value
        if rowLen == 0 or (rowtag != None and rowtag.startswith("##")):
            cells.remove(row)
