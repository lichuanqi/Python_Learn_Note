# 相对于传统的os及os.path，pathlib具体如下优势：

# pathlib实现统一管理，解决了传统操作导入模块不统一问题；
# pathlib使得在不同操作系统之间切换非常简单；
# pathlib是面向对象的，路径处理更灵活方便，解决了传统路径和字符串并不等价的问题；
# pathlib简化了很多操作，简单易用。

from pathlib import Path

# 文件绝对路径
current_file = Path(__file__)
print(current_file)
current_path = current_file.parent
print(current_path)

config_path = current_path / "AppData"
if not config_path.exists():
    config_path.mkdir(exist_ok=True)
    print("config_path no exists, mkdir over")
print(config_path)

config_file = config_path / "config.json"
print(config_file)
if config_file.exists():
    print('config_file exists')
else:
    print('config_file no exists')

Path(current_file).name       # 文件名+文件后缀
Path(current_file).stem       # 文件名
Path(current_file).suffix     # 文件后缀
Path(current_file).suffixes   # 文件后缀列表
Path(current_file).root       # 根目录
Path(current_file).parts      # 文件
Path(current_file).anchor     # 根目录
Path(current_file).parent     # 父级目录
Path(current_file).parents    # 上级目录的列表

# 当前所在目录
current_path = Path.cwd()

# 电脑用户的目录
home_path = Path.home()