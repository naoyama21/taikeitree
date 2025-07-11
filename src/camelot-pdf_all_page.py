import camelot
import pandas as pd
import os

# PDFファイルのパス
# ここを元のPDFファイル名に置き換えてください (例: "001178206.pdf")
pdf_path = "data/raw/R06taikeitree.pdf" # 元のPDFファイル名に修正

# ファイルが存在するか確認
if not os.path.exists(pdf_path):
    print(f"エラー: '{pdf_path}' が見つかりません。")
    print("PDFファイルのパスが正しいか確認し、実行するディレクトリにファイルがあることを確認してください。")
    exit()

print(f"'{pdf_path}' の7ページ目から94ページ目までから表データを抽出します...")

# pdfminer.sixの出力とPDFの目視確認に基づき、各列の右端のX座標を再調整します。
# これらの座標は、PDFのヘッダー行の構造に基づいています。
# レベル1の右端: 102.18
# レベル2の右端: 180.90
# レベル3の右端: 275.58
# レベル4の右端: 381.34
# レベル5の右端: 527.27
# 「積算用 単位」「工事数量 括表用単位」「モジュール コードNa」の結合部分を3分割
#   611.03 + (703.25 - 611.03) / 3 = 641.77
#   611.03 + 2 * (703.25 - 611.03) / 3 = 672.51
# 「モジュール コードNa」と「摘 要」の間: 737.98
column_coords_list = ['102.18,180.90,275.58,381.34,527.27,641.77,672.51,737.98']

# 表の全体的な領域を指定します。
# (x1, y1, x2, y2) -> 左下(x1, y1), 右上(x2, y2)
# 左端をX=50に広げ、「整地」などのテキストをカバーするようにします。
# Y座標はPDFの左下を基準にしています。
table_areas_str = ['50,50,780,538']

# 抽出されたDataFrameを格納するためのリスト
all_extracted_dfs = []

try:
    # 7ページ目から94ページ目までを抽出するようにpages引数を修正
    tables = camelot.read_pdf(
        pdf_path,
        flavor='stream',
        pages='7-94', # ここを修正: 抽出したいページ範囲を指定
        columns=column_coords_list,
        table_areas=table_areas_str,
        # row_tolはデフォルトの2で試します。必要であれば調整してください。
        # row_tol=2
    )
    print(f"指定されたページ範囲で {len(tables)} 個の表を検出しました。")

    if tables:
        # 検出された各表をDataFrameに変換し、リストに追加
        for i, table in enumerate(tables):
            df_page = table.df
            print(f"ページ {table.page} の表を抽出しました。")
            all_extracted_dfs.append(df_page)

        if all_extracted_dfs:
            # 全てのDataFrameを結合し、一つの大きなDataFrameを作成
            # ignore_index=True は、結合後に新しい連続したインデックスを割り当てます
            final_df = pd.concat(all_extracted_dfs, ignore_index=True)
            
            print("\n--- 結合されたDataFrameの最初の5行 ---")
            print(final_df.head())
            
            # 結合されたDataFrameをCSVとして保存
            #出力先のフォルダを指定
            output_folder = "data/output"
            os.makedirs(output_folder, exist_ok=True)
            output_csv_filename = os.path.join(output_folder, "all_extracted_data_pages_7_94.csv")
            try:
                final_df.to_csv(output_csv_filename, index=False, encoding='utf-8-sig')
                print(f"すべての抽出データを '{output_csv_filename}' に保存しました。")
            except PermissionError:
                print(f"エラー: '{output_csv_filename}' への書き込み権限がありません。")
                print("ファイルが他のプログラムで開かれていないか確認し、閉じてから再度実行してください。")
        else:
            print("指定されたページ範囲で有効な表が検出されませんでした。")

    else:
        print("指定された領域で表が検出されませんでした。")

except Exception as e:
    print(f"抽出中にエラーが発生しました: {e}")
    print("Ghostscriptが正しくインストールされ、パスが通っているか確認してください。")

print("\n表データの抽出が完了しました。")
