from PyPDF2 import PdfReader, PdfWriter

# 分割したいPDFファイルを読み込む
# 必ず '001178206.pdf' を実際のPDFファイルのパスに置き換えてください
try:
    reader = PdfReader("R06taikeitree.pdf")
except FileNotFoundError:
    print("エラー: 'R06taikeitree.pdf' が見つかりません。")
    print("PDFファイルのパスが正しいか確認し、実行するディレクトリにファイルがあることを確認してください。")
    exit() # ファイルが見つからない場合は処理を終了

# 抽出したいページの範囲を定義
# 7ページ目から10ページ目までを抽出します。
# Pythonのリストは0-indexedなので、7ページ目はインデックス6、10ページ目はインデックス9です。
start_page_number = 7  # 抽出開始ページ (1から数える)
end_page_number = 17   # 抽出終了ページ (1から数える)

# 0-indexedのページインデックスに変換
start_index = start_page_number - 1
end_index = end_page_number - 1 # スライスではこの値まで含まれないため、+1は不要

print(f"PDFのページ {start_page_number} から {end_page_number} までを分割します。")

# 指定されたページ範囲を個別のファイルに分割
# range(start_index, end_index + 1) とすることで、start_index から end_index までのインデックスを処理します。
for i in range(start_index, end_index + 1):
    # PDFにそのページが存在するか確認
    if i < len(reader.pages):
        page = reader.pages[i]
        writer = PdfWriter()
        writer.add_page(page)
        
        # 出力ファイル名に元のページ番号を含める (iは0-indexedなので+1する)
        output_filename = f"output_page_{i+1}.pdf"
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
        print(f"{output_filename} を作成しました。")
    else:
        print(f"警告: PDFにはページ {i+1} が存在しません。指定された範囲がPDFの総ページ数を超えています。")

print(f"PDFのページ {start_page_number} から {end_page_number} までの分割が完了しました。")
