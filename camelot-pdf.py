import camelot
import pandas as pd
import os

# PDFファイルのパス
pdf_path = "output_page_8.pdf"

# ファイルが存在するか確認
if not os.path.exists(pdf_path):
    print(f"エラー: '{pdf_path}' が見つかりません。")
    print("PDFファイルのパスが正しいか確認し、実行するディレクトリにファイルがあることを確認してください。")
    exit()

print(f"'{pdf_path}' から表データを抽出します（columnsとtable_areasを精密化）...")

# pdfminer.sixの出力とPDFの目視確認に基づき、各列の右端のX座標を再調整します。
# 9つの論理的な列（レベル1から摘要まで）があるため、8つの垂直線が必要です。
# 各ヘッダーの右端のX座標を基点とし、結合されている部分（積算用～コードNa）は均等に分割を試みます。
# レベル1の右端: 102.18
# レベル2の右端: 180.90
# レベル3の右端: 275.58
# レベル4の右端: 381.34
# レベル5の右端: 527.27
# 「積算用 単位」「工事数量 括表用単位」「モジュール コードNa」の結合部分 (611.03 から 703.25) を3分割
#   611.03 + (703.25 - 611.03) / 3 = 611.03 + 30.74 = 641.77
#   611.03 + 2 * (703.25 - 611.03) / 3 = 611.03 + 61.48 = 672.51
# 「モジュール コードNa」と「摘 要」の間: 737.98 (「摘 要」の左端)

# column_coords_str を単一の文字列を含むリストとして定義
column_coords_list = ['102.18,180.90,275.58,381.34,527.27,641.77,672.51,737.98']

# 表の全体的な領域を指定します。
# (x1, y1, x2, y2) -> 左下(x1, y1), 右上(x2, y2)
# ヘッダーの最上部が約Y=538、ページの左端が約X=50（整地のx0=54.91をカバーするため）、右端が約X=780、ページ下部が約Y=50と仮定
table_areas_str = ['50,50,780,538'] # ここを修正しました

try:
    tables = camelot.read_pdf(
        pdf_path,
        flavor='stream',
        pages='all',
        columns=column_coords_list, # ここを修正: リストとして渡す
        table_areas=table_areas_str,
        # row_tolはデフォルトの2で試します。必要であれば調整してください。
        # row_tol=2
    )
    print(f"columnsとtable_areas指定で {len(tables)} 個の表を検出しました。")

    if tables:
        df = tables[0].df
        print("\n--- 精密化したcolumnsとtable_areasで抽出された表の最初の5行 ---")
        print(df.head())
        
        # 抽出されたDataFrameをCSVとして保存
        df.to_csv("extracted_table_refined_columns_area.csv", index=False, encoding='utf-8-sig')
        print("抽出された表を 'extracted_table_refined_v2_columns_area.csv' に保存しました。")

        # 'Table' object has no attribute 'to_pdf' エラーを避けるため、一時的にコメントアウト
        # tables[0].to_pdf('table_debug_refined.pdf')
        # print("'table_debug_refined.pdf' を生成しました。これを開いて列の区切りが正しいか確認してください。")

    else:
        print("指定された領域で表が検出されませんでした。")

except Exception as e:
    print(f"抽出中にエラーが発生しました: {e}")
    print("Ghostscriptが正しくインストールされ、パスが通っているか確認してください。")

print("\n表データの抽出が完了しました。")
