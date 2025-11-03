from django.shortcuts import render, get_object_or_404, redirect
from .forms import DatasetForm
from .models import Dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os

def upload_csv(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            #csvファイルを読み込む
            try:
                df = pd.read_csv(dataset.csv_file.path, nrows=500, encoding='utf-8')
            except:
                df = pd.read_csv(dataset.csv_file.path, nrows=500, encoding='shift-jis')
            #データの要約を取得
            summary = df.describe().to_html(classes="table table-striped")
            #グラフを作成(ペアプロット)
            sns.set_theme(style='ticks')
            pairplot = sns.pairplot(df.select_dtypes(include='number'))
            #バイナリ写真データ→文字列（こうすることでhtmlに入れられる）
            #BytesIOは仮想ファイルを作ってくれる
            buffer = io.BytesIO()
            #pngのバイナリデータを仮想ファイルに保存
            pairplot.savefig(buffer, format='png')
            #seekで読み取り位置を先頭にする
            buffer.seek(0)
            #getvalueはseekから最後までbytesとして取り出す
            image_png = buffer.getvalue()
            #image_pngに保存したのでバイナリファイルを消滅させる
            buffer.close()
            plt.close()
            #バイナリを文字列に
            graphic = base64.b64encode(image_png).decode('utf-8')
            
            #グラフ作成（相関ヒートマップ）
            plt.figure(figsize=(6, 4))
            numeric_data = df.select_dtypes(include=['number'])
            sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            graphic2 = base64.b64encode(image_png).decode('utf-8')
            #return renderでテンプレート変数を定義する
            return render(request, 'result.html', {
                'summary': summary,
                'graphic': graphic,
                'graphic2': graphic2
            })
    else:
        form = DatasetForm()
    return render(request, 'upload.html',{'form':form})

def dataset_list(request):
    datasets = Dataset.objects.all().order_by('-uploaded_at')
    return render(request, 'dataset_list.html', {'datasets': datasets})

def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    try:
        df = pd.read_csv(dataset.csv_file.path, nrows=500, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(dataset.csv_file.path, nrows=500, encoding='shift_jis')
    #データの要約を取得
    summary = df.describe().to_html(classes="table table-striped")
    #グラフを作成(ペアプロット)
    sns.set_theme(style='ticks')
    pairplot = sns.pairplot(df.select_dtypes(include='number'))
    #バイナリ写真データ→文字列（こうすることでhtmlに入れられる）        #BytesIOは仮想ファイルを作ってくれる
    buffer = io.BytesIO()        
    #pngのバイナリデータを仮想ファイルに保存        
    pairplot.savefig(buffer, format='png')
    plt.close()
    #seekで読み取り位置を先頭にする
    buffer.seek(0)
    #getvalueはseekから最後までbytesとして取り出す
    image_png = buffer.getvalue()
    #image_pngに保存したのでバイナリファイルを消滅させる
    buffer.close()
    #バイナリを文字列に
    graphic = base64.b64encode(image_png).decode('utf-8')
    #グラフ作成（相関ヒートマップ）
    plt.figure(figsize=(6, 4))
    numeric_data = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graphic2 = base64.b64encode(image_png).decode('utf-8')
    #return renderでテンプレート変数を定義する
    return render(request, 'dataset_detail.html', {
        'dataset': dataset,
        'summary': summary,
        'graphic': graphic,
        'graphic2': graphic2
    })

def dataset_delete(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    #csvファイルを削除
    if dataset.csv_file:
        if os.path.isfile(dataset.csv_file.path):
            dataset.csv_file.delete(save=True)
    dataset.delete()
    return redirect('dataset_list')