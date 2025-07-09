from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure, LTImage, LTRect, LTLine, LTPage
import os

def extract_text_and_coords(pdf_path, output_txt_path=None):
    """
    PDFからテキストとその座標情報を抽出し、表示・保存する関数。

    Args:
        pdf_path (str): 入力PDFファイルのパス。
        output_txt_path (str, optional): 抽出結果を保存するテキストファイルのパス。
                                         指定しない場合、コンソールに出力。
    """
    if not os.path.exists(pdf_path):
        print(f"エラー: '{pdf_path}' が見つかりません。")
        return

    all_extracted_data = []

    print(f"'{pdf_path}' からテキストと座標情報を抽出中...")

    # extract_pages関数を使ってページごとに処理
    # 最初の10ページまで処理する (必要に応じて調整)
    # 実際には、extract_pages(pdf_path) のようにpages引数を省略して全ページ処理できます。
    # ここでは例として、以前の要件に合わせて7ページ目（インデックス6）のみを処理します。
    # PDFページは0から始まるインデックスですが、extract_pagesのページ番号指定は1から始まることもあります。
    # 確実に7ページ目を処理するために、ページのリストをイテレートし、7ページ目を探すか、
    # ページ範囲を指定するオプションを使用します。（ここでは簡単のため、すべてのページを処理し、
    # 特定のページのみを抽出するロジックは含みません。必要であれば追加してください。）

    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        # 7ページ目（インデックス6）のみを処理する例
        # 特定のページのみを処理したい場合は、ここで条件分岐します
        # if page_num != 6: # 7ページ目以外はスキップ
        #     continue

        page_data = {
            "page_number": page_num + 1,
            "width": page_layout.width,
            "height": page_layout.height,
            "elements": []
        }

        # ページ内の各要素を処理
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # テキストコンテナの場合
                for text_line in element:
                    # LTTextLineHorizontalのような行要素
                    line_text = text_line.get_text().strip()
                    # バウンディングボックス: (x0, y0, x1, y1)
                    # x0, y0: 左下隅の座標
                    # x1, y1: 右上隅の座標
                    bbox = text_line.bbox
                    
                    # より詳細に文字ごとの座標も取得したい場合は、LTCharをイテレート
                    chars_data = []
                    for char in text_line:
                        if isinstance(char, LTChar):
                            chars_data.append({
                                "char": char.get_text(),
                                "fontname": char.fontname,
                                "size": char.size,
                                "bbox": char.bbox # 文字ごとのバウンディングボックス
                            })

                    if line_text: # 空行はスキップ
                        page_data["elements"].append({
                            "type": "text_line",
                            "text": line_text,
                            "bbox": bbox,
                            "chars": chars_data # 文字ごとの詳細情報
                        })
            elif isinstance(element, (LTRect, LTLine)):
                # 線や図形の場合
                page_data["elements"].append({
                    "type": "shape",
                    "bbox": element.bbox
                })
            # 他にもLTImage (画像), LTFigure (図) などがありますが、ここではテキストと線に焦点を当てます。

        all_extracted_data.append(page_data)

    # 結果の表示または保存
    if output_txt_path:
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            for page_data in all_extracted_data:
                f.write(f"--- Page {page_data['page_number']} (Width: {page_data['width']:.2f}, Height: {page_data['height']:.2f}) ---\n")
                for elem in page_data["elements"]:
                    if elem["type"] == "text_line":
                        f.write(f"  [Text] BBox: ({elem['bbox'][0]:.2f}, {elem['bbox'][1]:.2f}, {elem['bbox'][2]:.2f}, {elem['bbox'][3]:.2f}) Text: '{elem['text']}'\n")
                        # # 文字ごとの詳細を表示する場合 (コメントアウトを外す)
                        # for char_info in elem['chars']:
                        #     f.write(f"    Char: '{char_info['char']}' BBox: {char_info['bbox']} Font: {char_info['fontname']} Size: {char_info['size']}\n")
                    elif elem["type"] == "shape":
                        f.write(f"  [Shape] BBox: ({elem['bbox'][0]:.2f}, {elem['bbox'][1]:.2f}, {elem['bbox'][2]:.2f}, {elem['bbox'][3]:.2f})\n")
                f.write("\n")
        print(f"抽出結果を '{output_txt_path}' に保存しました。")
    else:
        for page_data in all_extracted_data:
            print(f"--- Page {page_data['page_number']} (Width: {page_data['width']:.2f}, Height: {page_data['height']:.2f}) ---")
            for elem in page_data["elements"]:
                if elem["type"] == "text_line":
                    print(f"  [Text] BBox: ({elem['bbox'][0]:.2f}, {elem['bbox'][1]:.2f}, {elem['bbox'][2]:.2f}, {elem['bbox'][3]:.2f}) Text: '{elem['text']}'")
                elif elem["type"] == "shape":
                    print(f"  [Shape] BBox: ({elem['bbox'][0]:.2f}, {elem['bbox'][1]:.2f}, {elem['bbox'][2]:.2f}, {elem['bbox'][3]:.2f})")
            print("\n")


# 実行例
pdf_file = "output_page_7.pdf" # 以前分割したPDFファイル
output_file = "extracted_coords_and_text_page7.txt"

extract_text_and_coords(pdf_file, output_file)
# またはコンソールに直接出力する場合
# extract_text_and_coords(pdf_file)
