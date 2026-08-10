import sys
import time

# # 最简单的百分比进度条
# total = 100
# for i in range(total):
#     time.sleep(0.05)  # 模拟任务
    
#     progress = (i + 1) / total * 100
#     sys.stdout.write(f"\r进度: {progress:.1f}% ({i+1}/{total})")
#     sys.stdout.flush()

# print("\n完成！")
# print("="*72)

# 图形化进度条
def progress_bar(current, total, bar_length=50):
    """
    自定义进度条函数
    """
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '█' + '▶'
    padding = int(bar_length - len(arrow)) * '░'
    percent = fraction * 100
    
    sys.stdout.write(f'\r|{arrow}{padding}| {percent:.1f}% ({current}/{total})')
    sys.stdout.flush()
total_items = 200
for i in range(total_items):
    time.sleep(0.02)  # 模拟任务
    progress_bar(i + 1, total_items)

print("\n任务完成！")


# 彩色进度条
class ColorfulProgressBar:
    """彩色进度条类"""
    
    # 颜色代码
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    def __init__(self, total, description="进度", color='green', bar_length=40):
        self.total = total
        self.description = description
        self.color = self.COLORS.get(color, self.COLORS['green'])
        self.bar_length = bar_length
        self.reset = self.COLORS['reset']
    
    def update(self, current):
        percent = current / self.total
        filled_length = int(self.bar_length * percent)
        bar = '█' * filled_length + '░' * (self.bar_length - filled_length)
        
        # 动态颜色（根据进度变化）
        if percent < 0.3:
            color = self.COLORS['red']
        elif percent < 0.7:
            color = self.COLORS['yellow']
        else:
            color = self.COLORS['green']
        
        message = f"\r{self.description}: {color}[{bar}]{self.reset} {percent:.1%} ({current}/{self.total})"
        sys.stdout.write(message)
        sys.stdout.flush()
    
    def finish(self):
        print(f"\n{self.COLORS['green']} 已完成{self.reset}")

total = 150
bar = ColorfulProgressBar(total, "下载小说", 'cyan', 30)

for i in range(total):
    time.sleep(0.03)  # 模拟下载
    bar.update(i + 1)

bar.finish()




import sys
import time
import itertools

def spinning_cursor():
    """旋转光标生成器"""
    while True:
        for cursor in '|/-\\':
            yield cursor

def spinner_progress(total, message="处理中"):
    """旋转进度指示器"""
    spinner = spinning_cursor()
    
    for i in range(total):
        time.sleep(0.1)  # 模拟任务
        
        # 显示旋转光标和进度
        percent = (i + 1) / total * 100
        sys.stdout.write(f'\r{message} {next(spinner)} {percent:.1f}% ({i+1}/{total})')
        sys.stdout.flush()
    
    print(f"\r{message}100.0% ({total}/{total})   ")

spinner_progress(100, "正在下载")



# import time
# for i in range(5):
#     print(f"当前数字: {i}", end="\r")  # 不换行，回到行首
#     time.sleep(1)
# for i in range(5):
#     print(f"\r当前数字: {i}", end='') # 不换行，回到行首 注意 end = '' 默认为换行
#     time.sleep(1)


# import sys
# # print() 会自动添加换行符，不适合进度条
# print()
# print("进度: 50%")  # 自动换行

# # sys.stdout.write() 更底层，可控制
# sys.stdout.write("进度: 50%\r")  # 不换行，回到行首
# sys.stdout.flush()  # 强制立即输出


# # 没有flush()，输出可能被缓冲，不立即显示
# for i in range(101):
#     sys.stdout.write(f"\r进度: {i}%")
#     # 没有flush()，可能累积到缓冲区满才显示
#     time.sleep(0.1)

# # 有flush()，立即显示
# for i in range(101):
#     sys.stdout.write(f"\r进度: {i}%")
#     sys.stdout.flush()  # 强制立即输出到屏幕
#     time.sleep(0.1)