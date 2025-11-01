from django.shortcuts import render
from .forms import DatasetForm
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def upload_csv(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            #csvファイルを読み込む
            df = pd.read_csv(dataset.csv_file.path)
            #データの要約を取得
            summary = df.describe().to_html(classes="table table-striped")
            #グラフを作成
            plt.figure()
            if len(df.columns) >= 2:
                df.plot(kind='scatter', x=df.columns[0], y=df.columns[1])
            else:
                df[df.columns[0]].value_counts().plot(kind='bar')
            plt.title("sample_graph")
            #バイナリ写真データ→文字列（こうすることでhtmlに入れられる）
            #BytesIOは仮想ファイルを作ってくれる
            buffer = io.BytesIO()
            #pngのバイナリデータを仮想ファイルに保存
            plt.savefig(buffer, format='png')
            #seekで読み取り位置を先頭にする
            buffer.seek(0)
            #getvalueはseekから最後までbytesとして取り出す
            image_png = buffer.getvalue()
            #image_pngに保存したのでバイナリファイルを消滅させる
            buffer.close()
            #バイナリを文字列に
            graphic = base64.b64encode(image_png).decode('utf-8')

            #return renderでテンプレート変数を定義する
            return render(request, 'result.html', {
                'summary': summary,
                'graphic': graphic
            })
    else:
        form = DatasetForm()
    return render(request, 'upload.html',{'form':form})

