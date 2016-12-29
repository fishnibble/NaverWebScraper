import requests
import urllib.request
from bs4 import BeautifulSoup
import os, os.path


class naverscrape(object):
    def __init__(self, urlpayload, path):
        self.urlpayload = urlpayload
        self.path = path

    def payloadprep(self):
        urlarray = []
        url = requests.get(self.urlpayload).content
        soup = BeautifulSoup(url, "html.parser")

        for text in soup.find_all('div', class_='levels clearfix'):
            for links in text.find_all('a'):
                urlarray.append("http://www.memrise.com" + links.get('href'))
        return urlarray

    # Goes to main list of chapters and grabs all the urls for each chapter


    def getvocab(self):
        url = self.payloadprep()
        souparray = []
        helper = []
        test = ''

        for link in url:
            goto = requests.get(link).content
            soup = BeautifulSoup(goto, "html.parser")
            helper.append(test)
            souparray.append(helper)
            test = ''
            helper = []
            for vocab in soup.find_all('div', attrs={"class": "col_a col text"}):
                test += vocab.text + '\n'
                # if '갑자기' in test:
                # souparray.append([test.replace('.', " ")])
                    # need to fix this loop so it can be used for any course
        return souparray
        # Goes to everything in the payload and grabs all the vocab in every URL
        # col_a col text is every all the korean text is at

    def makefolders(self):
        counter = 1
        urls = self.payloadprep()
        for links in urls:
            if not os.path.isdir(self.path + "{0}".format(counter)):
                os.mkdir(self.path + "{}".format(counter))
                counter += 1

    def getenglish(self):
        url = self.payloadprep()
        souparray = []
        helper = []
        test = ''

        for link in url:
            goto = requests.get(link).content
            soup = BeautifulSoup(goto, "html.parser")
            helper.append(test)
            souparray.append(helper)
            test = ''
            helper = []
            for vocab in soup.find_all('div', attrs={"class": "col_b col text"}):
                test += vocab.text + ' '
                # if '갑자기' in test:
                # souparray.append([test.replace('.', " ")])
                # need to fix this loop so it can be used for any course
        return souparray

    def getmp3(self):
        for root, dirnames, filenames in os.walk(self.path):
            for files in filenames:
                if files.endswith('.txt'):
                    f = open(os.path.join(root, files), 'r', encoding='UTF-8')
                    for stuff in f:
                        vocab = stuff.replace('.', '')
                        rawurl = requests.get(
                            'http://m.krdic.naver.com/search/all/0/{0}?format=HTML&isMobile=true'.format(vocab)).content
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

    def writevocab(self, korea, english = None):

        count = 1
        if english == None:
            for words in korea:
                with open(self.path + "{}".format(count) + '/{}'.format(count) + '.txt', 'w', encoding='utf-8') as txtf:
                    str1 = ''.join(words)
                    txtf.write(str1)
                    str1 = ''
                count +=1
        else:
            pass
