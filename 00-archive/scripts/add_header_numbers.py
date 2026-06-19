import os
import re
import sys

# 默认使用命令行执行脚本时的当前工作目录
repo_dir = os.getcwd()

# 如果传入了命令行参数，则使用参数指定的目录
if len(sys.argv) > 1:
    target_dir = sys.argv[1]
    if os.path.isdir(target_dir):
        repo_dir = os.path.abspath(target_dir)
    else:
        print(f"错误: 路径 '{target_dir}' 不是一个有效的目录。")
        sys.exit(1)

print(f"开始处理目录: {repo_dir}")

def add_header_numbers(content):
    lines = content.splitlines()
    new_lines = []
    
    in_yaml = False
    in_code_block = False
    
    # 对应 2-6 级标题的计数器，最多支持 5 层标题嵌套 (## 到 ######)
    counters = [0] * 5
    
    for line_idx, line in enumerate(lines):
        # 1. 识别并跳过 YAML frontmatter
        if line_idx == 0 and line == '---':
            in_yaml = True
            new_lines.append(line)
            continue
        elif in_yaml and line == '---':
            in_yaml = False
            new_lines.append(line)
            continue
            
        if in_yaml:
            new_lines.append(line)
            continue
            
        # 2. 识别并跳过代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        # 3. 匹配标题行 (仅匹配 2 级到 6 级标题)
        title_match = re.match(r'^(#{2,6})\s+(.*)', line)
        if title_match:
            hashes = title_match.group(1)
            title_text = title_match.group(2)
            
            level = len(hashes)
            idx = level - 2  # idx=0 表示二级标题，idx=1 表示三级标题
            
            # 更新当前层级计数器
            counters[idx] += 1
            # 重置所有子层级的计数器
            for i in range(idx + 1, len(counters)):
                counters[i] = 0
                
            # 组装层级序号字符串，例如 [1, 2] -> "1.2."
            num_parts = counters[:idx + 1]
            num_str = ".".join(map(str, num_parts)) + "."
            
            # 剥离已存在的标题序号，防止重复添加。匹配如 "1. ", "1.1 ", "1.1.2. " 等格式
            clean_text = re.sub(r'^(?:\d+(?:\.\d+)*\.\s*|\d+(?:\.\d+)*\s+)', '', title_text)
            
            # 组合成规范化的新标题行
            new_line = f"{hashes} {num_str} {clean_text}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    return "\n".join(new_lines) + ("\n" if content.endswith('\n') else "")

# 扫描指定目录执行更新
processed_files = 0
modified_files = 0

for dirpath, dirnames, filenames in os.walk(repo_dir):
    parts = dirpath.split(os.sep)
    if any(part.startswith('.') for part in parts):
        continue
        
    for filename in filenames:
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(dirpath, filename)
        processed_files += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            updated_content = add_header_numbers(original_content)
            
            if original_content != updated_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                modified_files += 1
                rel_path = os.path.relpath(filepath, repo_dir)
                print(f"已修改: {rel_path}")
        except Exception as e:
            print(f"处理 {filename} 失败: {e}")

print(f"执行完毕: 检查了 {processed_files} 个文件, 实际更新了 {modified_files} 个文件。")
