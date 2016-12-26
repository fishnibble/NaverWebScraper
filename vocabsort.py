import requests
import urllib.request
from bs4 import BeautifulSoup
import os, os.path


x = requests.get('http://www.memrise.com/course/283033/korean-made-simple-go-billy-korean/')

url = x.content

soup = BeautifulSoup(url, "html.parser")

url = []
path = 'C:/Users/fish/Desktop/untitled/naverscraper/'
souparray = []
test = ""
helper = []
me = 0
sublink = []
subcount = 0

for text in soup.find_all('div', class_='levels clearfix'):
    for links in text.find_all('a'):
        url.append("http://www.memrise.com" + links.get('href'))

for link in url:
    sublink.append(link[72:-1])
    os.mkdir(path, sublink[subcount])
    subcount += 1

    for link in url:
        goto = requests.get(link).content
        soup = BeautifulSoup(goto, "html.parser")
        helper.append(test)
        souparray.append(helper)
        test = ''
        helper = []

        for vocab in soup.find_all('div', attrs={"class": "col_a col text"}):
            test += vocab.text + '\n'
            if '갑자기' in test:
                souparray.append([test])

                for words in souparray:
                    if not os.path.isdir(path + "{}".format(me)):
                        os.mkdir(path + "{}".format(me))
                    with open(path + "{}".format(me) + '/{}'.format(me) + '.txt', 'w', encoding='utf-8') as txtf:

                        str1 = ''.join(words)
                        txtf.write(str1)
                        str1 = ""
                        txtf.close()
                    me += 1
rootdir = 'C:/Users/fish/Desktop/untitled/naverscraper/'
for root, dirnames, filenames in os.walk(rootdir):
        for files in filenames:
            if files.endswith('.txt'):
                f = open(os.path.join(root, files) ,'r', encoding='UTF-8')
                for stuff in f:
                    vocab = stuff.replace('.', '')
                    rawurl = requests.get('http://m.krdic.naver.com/search/all/0/{0}?format=HTML&isMobile=true'.format(vocab)).content
                    soup = BeautifulSoup(rawurl, "html.parser")
                    mp3Url = []
                    for text in soup.find_all('div', class_='dt'):
                        for links in text.find_all('a'):
                            mp3Url.append(links.get('href'))
                        try:
                            urllib.request.urlretrieve(mp3Url[1], root + '/{}.mp3'.format(stuff).replace('\n', ''))
                            print("Downloaded {0}".format(stuff) + 'in {0}'.format(root))
                        except:
                            pass









