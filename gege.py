import os
import random
import hashlib
import json
from datetime import datetime

URL_DIR = "urls"
PROGRESS_FILE = "progress.json"
OUTPUT_DIR = "output"

LINKS_PER_MD = 300
BATCH_MD_COUNT = 1

DIR_POOL = ["post", "article", "news", "view", "page", "info"]
EXT_POOL = ["sHtMl", "ShTmL", "sHtML", "sHTML"]


# ======================
def random_chinese(length):
    return "".join(chr(random.randint(0x4e00, 0x9fa5)) for _ in range(length))


def short_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:6]


def gen_link(base):
    return f"{base}/{random.choice(DIR_POOL)}/{random.randint(100000,999999)}.{random.choice(EXT_POOL)}"


# ======================
# 读取 urls 文件夹
# ======================
def load_url_groups():
    groups = {}

    for file in os.listdir(URL_DIR):
        if file.endswith(".txt"):
            path = os.path.join(URL_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                urls = [i.strip().rstrip("/") for i in f if i.strip()]

            if urls:
                groups[file] = urls

    return groups


# ======================
# 进度
# ======================
def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ======================
def build_md(urls):
    header = random_chinese(random.randint(50, 80))
    content = header

    for _ in range(LINKS_PER_MD):
        base = random.choice(urls)
        content += "<br>" + gen_link(base)

    return content


# ======================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    groups = load_url_groups()
    progress = load_progress()

    for file_name, urls in groups.items():

        if file_name not in progress:
            progress[file_name] = 0

        for i in range(BATCH_MD_COUNT):

            md_index = progress[file_name] + i + 1

            md_content = build_md(urls)

            date = datetime.now().strftime("%Y%m%d")
            h = short_hash(md_content + str(random.random()))

            safe_name = file_name.replace(".txt", "")

            out_name = f"{date}_{safe_name}_{md_index}_{h}.md"
            out_path = os.path.join(OUTPUT_DIR, out_name)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"[OK] {file_name} -> {out_name}")

        progress[file_name] += BATCH_MD_COUNT

    save_progress(progress)


if __name__ == "__main__":
    main()