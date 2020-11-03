from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from .models import News
import urllib.request
import requests as rq
from newsapp.modules import modules
# csvdownload用
from django.http import HttpResponse
import csv
import io

# Create your views here.

class Create(CreateView):
   template_name = 'home.html'
   model = News
   fields = ('url',)
   success_url = reverse_lazy('list')


# https://news.yahoo.co.jp/
def listfunc(request):
   for post in News.objects.all():
       url = post.url
   list = []
   response = rq.get(url)
   bs = BeautifulSoup(response.text, "html.parser")
   ul_tag = bs.find_all(class_="topicsList_main")
   for tag in ul_tag[0]:
      title = tag.a.getText()
      url2 = tag.a.get("href")
      list.append([title, url2])
   # context = {'list': list,}
   context = {'list': modules.data_get(),}
   return render(request, 'list.html', context)


def csvdownload(request):
   response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
   filename = urllib.parse.quote(('データ.csv'))
   response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
   writer = csv.writer(response)
   writer.writerow(['タイトル', 'URL'])
   writer.writerows(modules.data_get())
   return response

'''
import re
import lxml.html as lx
def seofunc(request):
    search_query = post.value
    #requestsのget関数を使用して、Googleの検索結果画面(10位まで)の情報を抜き出す
    r = rq.get('http://www.google.co.jp/search?hl=jp&gl=JP&num=10&q='+search_query)
    html = r.text.encode()		#コンテンツをエンコードする
    root = lx.fromstring(html)	#パース（lxmlでスクレイピングする準備をする）

    #F6セルから下方向に記事URLを抜き出す
    i=6
    for a in root.cssselect('div#search h3.r a'):
        worksheet.update_cell(i,6, re.sub(r'/url\?q=|&sa.*', '',a.get('href'))) #update_cell(行,列,上書きする値)
        i = i+1

    #F列に入力されているURLをクロールして、タイトル、要約、キーワードを抜き出す
    #10位のサイトまで繰り替えす
    for i in range(6,16):
        try: # 古いサイトが読み込めないので無視する
            search = rq.get(worksheet.acell('F'+str(i)).value)	#acell('F6'.value) F6〜15セルの値をクロールする
            search_html = search.text.encode(search.encoding)	#encode(XXXX.encoding)：読み込む前に文字化けするものに対応

            #文字コードがUTFｰ8ならUTF-8でデコードしてパース
            if(search.encoding=='utf-8' or search.encoding=='UTF-8'):
                search_root = lx.fromstring(search_html.decode('utf-8'))

            #文字コードがそれ以外は普通にパース
            else:
                search_root = lx.fromstring(search_html)

            #タイトルの設定
            list_title = []
            for a in search_root.cssselect('title'):
                list_title.append(a.text)
            title=''
            for index,item in enumerate(list_title):
                if index==0:
                    title = item
                else:
                    title = title + ', ' +item
            worksheet.update_cell(i,3, title)

            #ディスクリプションの設定
            list_description = []
            for a in search_root.cssselect('meta[name="description"]'):
                list_description.append(a.get('content'))
            description=''
            for index,item in enumerate(list_description):
                if index==0:
                    description = item
                else:
                    description = description + ', ' +item
            worksheet.update_cell(i,4, description)

            #キーワードの設定
            list_keywords = []
            for a in search_root.cssselect('meta[name="keywords"]'):
                list_keywords.append(a.get('content'))
            keywords=''
            for index,item in enumerate(list_keywords):
                if index==0:
                    keywords = item
                else:
                    keywords = keywords + ', ' +item
            worksheet.update_cell(i,5, keywords)

        except: #例外処理：古いサイトを読み込めなかったときにする処理
            worksheet.update_cell(i,3, 'エラーのため測定不能')
            worksheet.update_cell(i,4, 'エラーのため測定不能')
            worksheet.update_cell(i,5, 'エラーのため測定不能')
'''
