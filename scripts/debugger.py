import time
import os

__all__ = ["Debugger"]

class Debugger:

    __slots__ = ["launchTime", "output"]

    def __init__(self) -> None:
        os.system("cls")
        self.launchTime = time.perf_counter()
        self.output = open("data/output.txt", 'w')
        self.print_out("[Launching Game...]")
        self.print_out(f"[Start Time : {time.asctime(time.localtime())}]")

    def print_out(self, string):
        print(string)
        self.output.write(string + '\n')
    
    def prints_out(self, list_str):
        for string in list_str:
            print(string)
            self.output.write(string + '\n')

    def info(self):
        return list(self.output)

    def close(self):
        totalTime = round(time.perf_counter() - self.launchTime, 1)
        self.print_out(f"[Finished in {totalTime}s...]")
        self.output.close()