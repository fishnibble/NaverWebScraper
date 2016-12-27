import requests
import urllib.request
from bs4 import BeautifulSoup
import os, os.path

class naverscrape(object):
    def __init__(self, urlpayload, path):
        self.urlpayload = urlpayload
        self.path = path
        url = requests.get(urlpayload)
        self.soup = BeautifulSoup(url, "html.parser")

    def payloadprep(self):
        url = []
        for text in self.soup.find_all_next('div', class_='levels clearfix'):
            for links in text.find_all('a'):
                url.append("http://www.memrise.com" + links.get('href'))
        return url
    # Goes to main list of chapters and grabs all the urls for each chapter

    def getvocab(self):
        url = self.payloadprep()
        souparray = []
        helper = []
        vocab = ''
        for link in url:
            goto = requests.get(url).content
            soup = BeautifulSoup(goto, "html.parser")
            helper.append(vocab)
            souparray.append(helper)
            test = ''
            helper = []
            for vocab in soup.find_all('div', attrs={"class": "col_a col text"}):
                test += vocab.text + '\n'
                if '갑자기' in test:
                    souparray.append([test])
                #need to fix this loop so it can be used for any course
        return souparray
        #Goes to everything in the payload and grabs all the vocab in every URL
        #col_a col text is every all the korean text is at

    def makefolders(self):
        counter = 0
        vocab = self.getvocab()
        if not os.path.isdir(self.path + "{0}".format(counter)):
            os.mkdir(self.path + "{}".format(counter))

    def getmp3(self):
        for root, dirnames, filenames in os.walk(self.path):
            for files in filenames:
                if files.endswith('.txt'):
                    f = open(os.path.join(root, files) ,'r', encoding='UTF-8')
                    for stuff in f:
                        vocab = stuff.replace('.', '')
                        rawurl = requests.get('http://m.krdic.naver.com/search/all/0/{0}?format=HTML&isMobile=true'.format(vocab)).content
                        soup = BeautifulSoup(rawurl, "html.parser")
                        mp3url = []
                        for text in soup.find_all('div', class_='dt'):
                            for links in text.find_all('a'):
                                mp3url.append(links.get('href'))
                            try:
                                urllib.request.urlretrieve(mp3url[1], root + '/{}.mp3'.format(stuff).replace('\n', ''))
                                print("Downloaded {0}".format(stuff) + 'in {0}'.format(root))
                            except:
                                pass

