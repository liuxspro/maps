from pathlib import Path

import yaml
import yaml_include
from utils import calculate_sha256_hash, get_time, get_yaml_data, save_yaml

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


def get_info(yml_file: Path):
    info = get_yaml_data(yml_file)["info"]
    return {
        "id": info["id"],
        "name": info["name"],
        "lastUpdated": info["lastUpdated"],
    }


def pack(config):
    name = config["name"]
    if config["type"] == "folder":
        print(f"📦 Pack 📁 {name}/")
        yaml.add_constructor(
            "!include", yaml_include.Constructor(base_dir=config["path"])
        )
        # YamlIncludeConstructor.add_to_loader_class(
        #     loader_class=yaml.FullLoader, base_dir=config["path"]
        # )
        with open(config["path"].joinpath("default.yml"), "r", encoding="utf-8") as f:
            # data = yaml.load(f, Loader=yaml.FullLoader)
            data = yaml.full_load(f)
            data_hash = calculate_sha256_hash(str(data))
            save_path = DIST_DIR.joinpath(f"{name}.yml")
            current_time = get_time()
            if save_path.exists():
                old_data = get_yaml_data(save_path)
                # 移除lastUpdated值
                old_data["info"]["lastUpdated"] = None
                old_data_hash = calculate_sha256_hash(str(old_data))
                if data_hash != old_data_hash:
                    data["info"]["lastUpdated"] = current_time
                    save_yaml(data, save_path)
                    print(f"\t🔄️ Updated {old_data_hash[:5]} -> {data_hash[:5]}")
                else:
                    print("\t↪️  No Update")
            else:
                print("\t✨  Create new file")
                data["info"]["lastUpdated"] = current_time
                save_yaml(data, save_path)
        return get_info(save_path)
    # single file
    print(f"📦 Pack 📄 {name}")
    data = get_yaml_data(config["path"])
    data_hash = calculate_sha256_hash(str(data))
    save_path = DIST_DIR.joinpath(f"{name}.yml")
    current_time = get_time()
    if save_path.exists():
        old_data = get_yaml_data(save_path)
        # 移除lastUpdated值
        old_data["info"]["lastUpdated"] = None
        old_data_hash = calculate_sha256_hash(str(old_data))
        if data_hash != old_data_hash:
            data["info"]["lastUpdated"] = current_time
            save_yaml(data, save_path)
            print(f"\t🔄️ Updated {old_data_hash[:5]} -> {data_hash[:5]}")
        else:
            print("\t↪️  No Update")
    else:
        print("\t✨  Create new file")
        data["info"]["lastUpdated"] = current_time
        save_yaml(data, save_path)
    return get_info(save_path)


def main():
    if not DIST_DIR.exists():
        DIST_DIR.mkdir()
    configs = list_configs(SRC_DIR)
    all_map_info = {}
    for config in configs:
        all_map_info[config["name"]] = pack(config)
    save_yaml(all_map_info, SUM_FILE)


if __name__ == "__main__":
    main()
