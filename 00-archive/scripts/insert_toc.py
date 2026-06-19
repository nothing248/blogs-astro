import os
import sys

# 默认使用终端当前工作目录
repo_dir = os.getcwd()

# 若第一个参数不是命令选项（不以 -- 开头），则视作指定的路径
if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
    target_dir = sys.argv[1]
    if os.path.isdir(target_dir):
        repo_dir = os.path.abspath(target_dir)
    else:
        print(f"错误: 路径 '{target_dir}' 不是一个有效的目录。")
        sys.exit(1)

print(f"开始处理目录: {repo_dir}")

def insert_toc_placeholder(content):
    # 去重检查
    if '<!-- toc -->' in content or '<!-- toc' in content:
        return content
        
    lines = content.splitlines()
    if not lines:
        return '<!-- toc -->\n'
        
    # 1. 识别并跨过 YAML 头部
    if lines[0] == '---':
        yaml_end_idx = -1
        for i in range(1, len(lines)):
            if lines[i] == '---':
                yaml_end_idx = i
                break
        if yaml_end_idx != -1:
            # 找到正文的第一个非空行索引
            content_start_idx = yaml_end_idx + 1
            while content_start_idx < len(lines) and lines[content_start_idx].strip() == '':
                content_start_idx += 1
            
            new_lines = lines[:yaml_end_idx + 1]
            new_lines.append('')
            new_lines.append('<!-- toc -->')
            new_lines.append('')
            new_lines.extend(lines[content_start_idx:])
            return '\n'.join(new_lines) + ('\n' if content.endswith('\n') else '')
            
    # 2. 无 YAML 头部直接在首行插入
    content_start_idx = 0
    while content_start_idx < len(lines) and lines[content_start_idx].strip() == '':
        content_start_idx += 1
        
    new_lines = ['<!-- toc -->', '']
    new_lines.extend(lines[content_start_idx:])
    return '\n'.join(new_lines) + ('\n' if content.endswith('\n') else '')

# 判断是否是批量运行模式
is_batch = '--batch' in sys.argv

processed_count = 0
modified_count = 0

for dirpath, dirnames, filenames in os.walk(repo_dir):
    parts = dirpath.split(os.sep)
    if any(part.startswith('.') for part in parts):
        continue
        
    for filename in filenames:
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(dirpath, filename)
        processed_count += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            updated_content = insert_toc_placeholder(original_content)
            
            if original_content != updated_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                modified_count += 1
                
                rel_path = os.path.relpath(filepath, repo_dir)
                print(f"修改成功: {rel_path}")
                
                # 如果不是批量模式，修改完第一个后退出
                if not is_batch:
                    print("\n[提示] 默认测试模式已完成。您可以使用 'git diff' 查看此修改效果。")
                    print("若一切正常，请通过运行以下指令进行全量批量处理：")
                    print(f"python3 {sys.argv[0]} --batch\n")
                    sys.exit(0)
                    
        except Exception as e:
            print(f"处理 {filename} 出错: {e}")

if is_batch:
    print(f"\n[批量执行完毕] 检查了 {processed_count} 个文件，成功插入了 {modified_count} 个文件。")
else:
    print("\n没有找到需要插入 <!-- toc --> 的文件。")
