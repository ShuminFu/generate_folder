import os
import random
import string


def generate_test_files():
    test_dir = "test_files"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # 定义文件类型配置
    file_configs = {
        "doc": [".doc", ".docx", ".pdf", ".txt"],
        "img": [".jpg", ".png", ".gif", ".webp"],
        "video": [".mp4", ".avi", ".mkv", ".mov"],
        "audio": [".mp3", ".wav", ".flac", ".m4a"],
        "code": [".py", ".js", ".cpp", ".java"],
        "data": [".csv", ".json", ".xml", ".xlsx"]
    }

    # 定义一些可能的中间标记
    middle_marks = ["draft", "final", "rev", "ver", "edit"]
    date_patterns = ["2024", "202403", "20240315"]

    def generate_base_name(prefix):
        # 生成2-3个随机中间部分
        num_parts = random.randint(2, 3)
        parts = []

        for _ in range(num_parts):
            part_type = random.choice(['mark', 'date', 'random'])
            if part_type == 'mark':
                parts.append(random.choice(middle_marks))
            elif part_type == 'date':
                parts.append(random.choice(date_patterns))
            else:
                parts.append(''.join(random.choices(string.ascii_lowercase, k=4)))

        # 将所有部分用下划线连接
        return f"{prefix}_{'_'.join(parts)}"

    # 为每个前缀生成一组文件
    for prefix, extensions in file_configs.items():
        # 为这个前缀生成一个基础名称
        base_name = generate_base_name(prefix)

        # 使用这个基础名称生成4-8个文件
        num_files = random.randint(4, 8)
        for i in range(num_files):
            # 添加序号作为最后一个部分
            full_name = f"{base_name}_{str(i + 1).zfill(3)}"
            # 随机选择一个文件扩展名
            ext = random.choice(extensions)
            # 生成完整文件名
            filename = f"{full_name}{ext}"
            filepath = os.path.join(test_dir, filename)

            # 创建空文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Test file: {filename}")

            print(f"已创建文件: {filename}")

    # 生成一些随机命名的文件组
    for i in range(3):
        random_prefix = ''.join(random.choices(string.ascii_lowercase, k=4))
        base_name = generate_base_name(random_prefix)

        # 为每个随机前缀生成2-4个文件
        num_files = random.randint(2, 4)
        for j in range(num_files):
            full_name = f"{base_name}_{str(j + 1).zfill(3)}"
            random_ext = random.choice([ext for exts in file_configs.values() for ext in exts])
            filename = f"{full_name}{random_ext}"
            filepath = os.path.join(test_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Random test file: {filename}")

            print(f"已创建随机文件: {filename}")

    print(f"\n测试文件已生成在 {os.path.abspath(test_dir)} 目录下")

    # 统计生成的文件信息
    files = os.listdir(test_dir)
    print(f"\n总共生成了 {len(files)} 个文件")

    # 按前缀统计
    prefix_count = {}
    for file in files:
        prefix = '_'.join(file.split('_')[:-1])  # 获取最后一个下划线之前的所有内容
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

    print("\n各前缀文件数量：")
    for prefix, count in prefix_count.items():
        print(f"{prefix}: {count}个文件")


if __name__ == "__main__":
    generate_test_files()