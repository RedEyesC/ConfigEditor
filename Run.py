import sys
import time
import traceback

from Core.ExportPip import Run

if __name__ == "__main__":
    startTime = time.process_time()
    try:
        args = sys.argv[1:]
        Run(args[0], args[1], args[2], args[3], args[4])
    except Exception as e:
        # 打印报错堆栈
        traceback.print_exc()
    else:
        endTime = time.process_time()
        print("运行成功", flush=True)
        print("消耗时间 %.6f" % (endTime - startTime))
