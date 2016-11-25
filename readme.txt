*使い方*

kokkailist.txtに取りたい国会図書館のURLを改行で入力

例
http://iss.ndl.go.jp/books/R100000002-I026370537-20
http://iss.ndl.go.jp/books/R100000002-I026370537-10
http://iss.ndl.go.jp/books/R100000002-I026370537-00

空白行を含むとエラーになるので注意

上記のテキストファイル記入後

コマンドプロンプトに同ファイルのkokkaiフォルダに移動(scrapy.cfgファイルが存在する階層)し
scrapy crawl kokkai -o ファイル名.拡張子

を実行
対応した拡張子のファイルが同階層に出力されます

