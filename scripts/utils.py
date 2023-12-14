import datetime
import hashlib
from pathlib import Path

import yaml


def get_file_hash(file_path, hash_algorithm="sha256"):
    # 获取文件的 SHA256 值
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        # 一次读取 8Kb
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_folder_hash(folder_path, hash_algorithm="sha256"):
    file_hashes = {}

    folder = Path(folder_path)
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            file_hashes[file_path] = get_file_hash(file_path, hash_algorithm)

    combined_hash = hashlib.new(hash_algorithm)
    for file_hash in sorted(file_hashes.values()):
        combined_hash.update(file_hash.encode())

    return combined_hash.hexdigest()


def get_hash(file_path: Path, hash_algorithm="sha256"):
    if file_path.is_dir():
        return get_folder_hash(file_path, hash_algorithm)
    return get_file_hash(file_path, hash_algorithm)


def get_time():
    # 获取当前UTC时间
    current_time = datetime.datetime.utcnow()
    # 定义 UTC+8 的时差
    utc_offset = datetime.timedelta(hours=8)
    # 将当前时间加上时差得到 UTC+8 时间
    current_time_utc8 = current_time + utc_offset
    # 格式化为指定格式
    formatted_time = current_time_utc8.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def get_yaml_data(yaml_file_path: Path):
    # 打开并读取YAML文件
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


def get_yaml_data_all(yaml_file_path: Path):
    # 打开并读取YAML文件
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        yaml_data = list(yaml.safe_load_all(file))
    return yaml_data


def save_yaml(data, file_path: Path):
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(data, file, sort_keys=False, allow_unicode=True, Dumper=IndentDumper)


def save_yaml_all(data: list, file_path: Path):
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump_all(
            data, file, sort_keys=False, allow_unicode=True, Dumper=IndentDumper
        )


def calculate_sha256_hash(input_string):
    # 创建一个SHA-256哈希对象
    sha256_hash = hashlib.sha256()

    # 更新哈希对象的内容
    sha256_hash.update(input_string.encode("utf-8"))

    # 获取十六进制表示的哈希值
    result = sha256_hash.hexdigest()

    return result
