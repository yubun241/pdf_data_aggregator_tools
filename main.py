'''
data　←ここに表（前半：先にスキャンを行う面）裏（後半：後にスキャンを行う面）とディレクトリを作成し元ファイルを入れる
temp　←ここに表（前半）裏（後半）とディレクトリを作成し　処理中のファイルが入る
result　←ここに最終的に結合するデータを順番通りに入れる
src ←ここにプログラム
'''

from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
import os
import re
import shutil

# フォルダの中身を空にする
def clear_folder(folder_path):
    for filename in tqdm(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    folders_to_clear = ["../result", "../temp/前半", "../temp/後半"]
    for folder in folders_to_clear:
        clear_folder(folder)

#---------------------------------------------------------------------------

# 分割するコード
def split_pdf(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True) 

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    for i in tqdm(range(total_pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        output_filename = f"page_{i + 1}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        #print(f"Saved {output_path}")

if __name__ == "__main__":
    input_pdf = "../data/前半/前半.pdf"
    output_folder = "../temp/前半"
    split_pdf(input_pdf, output_folder)


def split_pdf(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # 出力フォルダ作成

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    for i in tqdm(range(total_pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        output_filename = f"page_{i + 1}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        #print(f"Saved {output_path}")

if __name__ == "__main__":
    input_pdf = "../data/後半/後半.pdf"
    output_folder = "../temp/後半"
    split_pdf(input_pdf, output_folder)



# 後半の順番を入れ替える
def reverse_rename_files(folder_path):
    # folder_path内のpage_x.pdfを全部取得
    files = [f for f in os.listdir(folder_path) if re.match(r'page_\d+\.pdf$', f)]

    # ファイル名から数字部分を取得しsort
    def extract_number(filename):
        match = re.search(r'page_(\d+)\.pdf', filename)
        return int(match.group(1)) if match else -1

    files_sorted = sorted(files, key=extract_number)
    files_reversed = list(reversed(files_sorted))

    # 一時的に別名でリネーム（名前重複回避のため）
    tmp_renames = []
    for i, filename in enumerate(files_reversed, start=1):
        old_path = os.path.join(folder_path, filename)
        tmp_name = f"tmp_{i}.pdf"
        tmp_path = os.path.join(folder_path, tmp_name)
        os.rename(old_path, tmp_path)
        tmp_renames.append((tmp_path, i))

    # 一時ファイルを連番のpage_x.pdfにリネーム
    for tmp_path, new_num in tmp_renames:
        new_name = f"page_{new_num}.pdf"
        new_path = os.path.join(folder_path, new_name)
        os.rename(tmp_path, new_path)
        #print(f"Renamed {tmp_path} -> {new_path}")

if __name__ == "__main__":
    folder = "../temp/後半"
    reverse_rename_files(folder)
    print('入れ替え完了')

# 後半を偶数ページにリネームする
dir_path = "../temp/後半"
pattern = re.compile(r"page_(\d+)\.pdf")

# 1回目：全ファイルを偶数連番 + _F付きにリネーム
files = os.listdir(dir_path)
files = [f for f in files if pattern.match(f)]
files.sort(key=lambda x: int(pattern.match(x).group(1)))

for index, filename in enumerate(files, start=1):
    old_path = os.path.join(dir_path, filename)
    new_number = index * 2   # 偶数連番（2,4,6...）
    new_filename = f"page_{new_number}_F.pdf"
    new_path = os.path.join(dir_path, new_filename)

    #print(f"Renaming {filename} -> {new_filename}")
    os.rename(old_path, new_path)

# 2回目：_Fを除去して最終的な名前に戻す
pattern_f = re.compile(r"(page_\d+)_F\.pdf")
files = os.listdir(dir_path)

for filename in files:
    match = pattern_f.match(filename)
    if match:
        old_path = os.path.join(dir_path, filename)
        new_filename = f"{match.group(1)}.pdf"
        new_path = os.path.join(dir_path, new_filename)
        #print(f"Final rename {filename} -> {new_filename}")
        os.rename(old_path, new_path)


# 前半を奇数ページにリネームする

dir_path = "../temp/前半"
pattern = re.compile(r"page_(\d+)\.pdf")

# 1回目：奇数連番 + _F付きリネーム
files = os.listdir(dir_path)
files = [f for f in files if pattern.match(f)]
files.sort(key=lambda x: int(pattern.match(x).group(1)))

for index, filename in enumerate(files, start=1):
    old_path = os.path.join(dir_path, filename)
    new_number = index * 2 - 1  # 奇数連番 (1, 3, 5, ...)
    new_filename = f"page_{new_number}_F.pdf"
    new_path = os.path.join(dir_path, new_filename)

    #print(f"Renaming {filename} -> {new_filename}")
    os.rename(old_path, new_path)

# 2回目：_F除去して最終ファイル名に
pattern_f = re.compile(r"(page_\d+)_F\.pdf")
files = os.listdir(dir_path)

for filename in files:
    match = pattern_f.match(filename)
    if match:
        old_path = os.path.join(dir_path, filename)
        new_filename = f"{match.group(1)}.pdf"
        new_path = os.path.join(dir_path, new_filename)

        #print(f"Final rename {filename} -> {new_filename}")
        os.rename(old_path, new_path)


# ファイルを移動させる
source_dirs = ["../temp/前半", "../temp/後半"]
destination_dir = "../result"

# もしdestination_dirがない場合は作成
os.makedirs(destination_dir, exist_ok=True)

for src_dir in source_dirs:
    for filename in tqdm(os.listdir(src_dir)):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(destination_dir, filename)
        #print(f"Moving {src_path} -> {dst_path}")
        shutil.move(src_path, dst_path)

# 結合したPDFを作成
def extract_page_number(filename):
    # 大文字小文字を区別せずにPage_数字_ 形式から数字を抽出
    match = re.search(r'page_(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else -1

def merge_pdfs(input_folder, output_path):
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    pdf_files.sort(key=extract_page_number)

    writer = PdfWriter()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
        #print(f"Added {pdf_file}")

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
    print(f"Merged PDF saved as {output_path}")

if __name__ == "__main__":
    input_folder = "../result"
    output_pdf_path = "../merged_result.pdf"
    merge_pdfs(input_folder, output_pdf_path)
    print('結合完了')




