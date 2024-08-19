import time
import traceback

from Core.ExportPip import RunPip
from Core.Utils import LoadRawSheets


if __name__ == "__main__":
    startTime = time.process_time()
    try:
        pass
        # LoadRawSheets("G:/Project/BlackRail/Assets/RawData/Config/生成配置.xlsx",'Sheet1')
    except Exception as e:
        # 打印报错堆栈
        traceback.print_exc()
    else:
        endTime = time.process_time()
        print("运行成功", flush=True)
        print("消耗时间 %.6f" % (endTime - startTime))
