PDF表抽出スクリプト
このプロジェクトは、PythonのCamelotライブラリを使用して、PDFファイルから表形式のデータを抽出し、構造化されたCSVファイルとして保存するためのスクリプトです。特に、罫線が明確でないPDF（streamフレーバー）からの抽出に最適化されており、pdfminer.sixで特定した正確な座標情報に基づいて列と表の領域を定義しています。

機能
指定されたPDFファイルから、特定のページ範囲（例: 7ページから94ページ）の表データを抽出します。

Camelotのstreamフレーバーを使用し、テキストの配置に基づいて列を識別します。

columns引数にX座標を明示的に指定することで、列の分割精度を向上させます。

table_areas引数で表の抽出領域を限定し、不要なテキストの混入を防ぎます。

抽出されたすべてのページの表データを一つのPandas DataFrameに結合します。

結合されたDataFrameをCSVファイルとして、指定された出力ディレクトリに保存します。

出力ディレクトリが存在しない場合、自動的に作成します。

セットアップ
このスクリプトを実行するには、以下の要件を満たす必要があります。

1. Pythonのインストール
Python 3.7以降が必要です。Pythonの公式サイトからダウンロードしてインストールしてください。

2. Ghostscriptのインストール
CamelotはPDFを処理するためにGhostscriptを必要とします。お使いのOSに応じて、以下の手順でインストールし、システムパスを通してください。

Windows: Ghostscriptの公式サイトからインストーラーをダウンロードし、インストールします。インストール後、C:\Program Files\gs\gsX.XX\binのようなbinフォルダのパスをシステム環境変数Pathに追加します（X.XXはバージョン番号）。

macOS (Homebrew): ターミナルでbrew install ghostscriptを実行します。

Linux (Debian/Ubuntu): ターミナルでsudo apt-get install ghostscriptを実行します。

インストール後、新しいターミナル/コマンドプロンプトを開き、gswin64c -v (Windows) または gs -v (macOS/Linux) を実行して、Ghostscriptが正しくインストールされ、パスが通っていることを確認してください。

3. Pythonライブラリのインストール
以下のコマンドを実行して、必要なPythonライブラリをインストールします。

pip install pandas "camelot-py[cv]" openpyxl pdfminer.six

使用方法
PDFファイルの配置:
抽出したいPDFファイル（例: R06taikeitree.pdf）を、スクリプトの実行ディレクトリから見てdata/raw/フォルダに配置してください。

スクリプトの実行:
ターミナルまたはコマンドプロンプトで、スクリプトが保存されているディレクトリに移動し、以下のコマンドを実行します。

python camelot-pdf.py

重要な注意事項
PDFパスの確認: スクリプト内のpdf_path変数が、抽出したいPDFファイルへの正しい相対パスまたは絶対パスを指していることを確認してください。

列の座標 (column_coords_list): このスクリプトは、pdfminer.sixで事前に特定された列のX座標に強く依存しています。異なるレイアウトのPDFを処理する場合、これらの座標を再調整する必要があります。pdfminer.sixを使用して、新しいPDFの各列の右端のX座標を特定してください。

表の領域 (table_areas_str): 表がページ内の特定の領域に限定されている場合、table_areas_strを調整することで抽出精度が向上します。PDFビューアで座標を確認し、必要に応じて調整してください。
