import os

path = os.path.dirname(__file__)
home_path = os.path.dirname(path)
# 目录信息
dirs = ["tools","knowledge","questions","hardware"]


def snake_to_camel(snake_str):
    # 将字符串按下划线分割
    components = snake_str.split('_')
    # 第一个单词保持小写，其余单词首字母大写
    return ''.join(x.capitalize() for x in components)

res = ""
for item in dirs:
    abs_path1 = os.path.join(home_path, item) # 一级目录
    con_path1 = "/" + item + "/"
    res += f"- {snake_to_camel(item)}\n"
    for path2 in os.listdir(abs_path1):
        abs_path2 = os.path.join(abs_path1,path2) #二级目录
        con_path2 = con_path1 + path2
        file_path2 = snake_to_camel(os.path.splitext(path2)[0])
        if file_path2 != "Readme":
            if os.path.isdir(abs_path2):
                con_path2 += "/"
                res += f'  - {file_path2}\n'
                for path3 in os.listdir(abs_path2):
                    abs_path3 = os.path.join(abs_path2,path3) #三级目录
                    con_path3 = con_path2 + path3
                    file_path3 = snake_to_camel(os.path.splitext(path3)[0])
                    if file_path3 != "Readme":
                        res += f'    - [{file_path3}]({con_path3} "{file_path3}记录")\n'
            else:
                res += f'  - [{file_path2}]({con_path2} "{file_path2}记录")\n'


with open("test.md","w",encoding="utf-8") as f:
    f.write(res)

print(res)