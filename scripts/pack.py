from pathlib import Path

from utils import (
    get_hash,
    get_time,
    get_yaml_data,
    get_yaml_data_all,
    save_yaml,
    save_yaml_all,
)

SRC_DIR = Path(__file__).parent.parent.joinpath("src")
DIST_DIR = Path(__file__).parent.parent.joinpath("dist")
SUM_FILE = DIST_DIR.joinpath("summary.yml")


def list_configs(config_dir):
    # 目录配置
    configs = []
    for folder in config_dir.glob("*"):
        files_in_folder = [f.name for f in folder.glob("*") if f.is_file()]
        if folder.is_dir() and "default.yml" in files_in_folder:
            configs.append({"name": folder.name, "path": folder, "type": "folder"})
    # 单文件配置
    configs.extend(
        [{"name": x.stem, "path": x, "type": "file"} for x in config_dir.glob("*.yml")]
    )
    return configs


def get_config_data(file_path: Path):
    # 读取文件夹配置
    if file_path.is_dir():
        default = get_yaml_data(file_path.joinpath("default.yml"))
        import_files = default.get("import")
        map_data = {}
        for import_file in import_files:
            data = get_yaml_data(file_path.joinpath(f"{import_file}.yml"))
            map_data[import_file] = data
        del default["import"]
        return default, map_data
    info, data = get_yaml_data_all(file_path)
    return info, data


def init_summary():
    print("Generate New Summary File...")
    configs = list_configs(SRC_DIR)
    all_map_info = {}
    for config in configs:
        config_path = config["path"]
        dist_file = DIST_DIR.joinpath(f"{config['name']}.yml")

        info, data = get_config_data(config_path)
        info["hash"] = get_hash(config_path)
        info["lastUpdated"] = get_time()
        all_map_info[info["id"]] = info
        # 保存地图配置
        save_yaml_all([info, data], dist_file)
    # 保存summary
    save_yaml(all_map_info, SUM_FILE)


def pack(config):
    name = config["name"]
    current_hash = get_hash(config["path"])
    current_time = get_time()
    dist_file = DIST_DIR.joinpath(f"{config['name']}.yml")

    if config["type"] == "folder":
        print(f"📦 Pack 📁 {name}/")
    else:
        print(f"📦 Pack 📄 {name}")

    summary = get_yaml_data(SUM_FILE)
    current_map_sum = summary[name]
    if current_hash == current_map_sum["hash"]:
        print("\t↪️  No Update")
    else:
        # 更新地图配置文件
        info, data = get_config_data(config["path"])
        info["lastUpdated"] = current_time
        print(f"\t🔄️ Updated {current_hash[:5]} > {current_map_sum['hash'][:5]}")
        save_yaml_all([info, data], dist_file)
        # 更新 summary
        current_map_sum["hash"] = current_hash
        current_map_sum["lastUpdated"] = current_time
        save_yaml(summary, SUM_FILE)


def main():
    if not DIST_DIR.exists():
        DIST_DIR.mkdir()
    if not SUM_FILE.exists():
        init_summary()
        return
    summary_data = get_yaml_data(SUM_FILE)
    configs = list_configs(SRC_DIR)
    # 检查是否有文件增加
    for config in configs:
        if config["name"] in summary_data.keys():
            pack(config)
        else:
            name = config["name"]
            print(f"✨ New File {name}")
            info, data = get_config_data(config["path"])
            info["hash"] = get_hash(config["path"])
            info["lastUpdated"] = get_time()
            summary_data[config["name"]] = info
            # 更新 summary
            save_yaml(summary_data, SUM_FILE)
            # 更新地图配置文件
            save_yaml_all([info, data], DIST_DIR.joinpath(f"{name}.yml"))
            print("\t🔄️  Added")
    # 检查文件是否减少
    del_key = []
    for key in summary_data.keys():
        if key not in [x["name"] for x in configs]:
            del_key.append(key)

    for key in del_key:
        print(f"❎  Remove {key}")
        del summary_data[key]
        DIST_DIR.joinpath(f"{key}.yml").unlink()  # 只是文件的删除
    save_yaml(summary_data, SUM_FILE)


if __name__ == "__main__":
    main()
