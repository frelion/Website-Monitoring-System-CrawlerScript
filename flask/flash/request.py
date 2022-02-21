import grequests
import requests
import time

def readUrl(batch,patch = -1):
    pos = 0
    urllist = []
    if patch == -1:
        while True:
            urllist.clear()
            with open("urls.txt","r") as f:
                f.seek(pos)
                count = batch
                line = f.readline()
                while line and count > 0:
                    pos = f.tell()
                    urllist.append(line[:-1])
                    line = f.readline()
                    count -=1
            yield urllist
            if len(urllist) != batch:break
    
    else:
        for i in range(patch):
            urllist.clear()
            with open("urls.txt","r") as f:
                f.seek(pos)
                count = batch
                line = f.readline()
                while line and count > 0:
                    pos = f.tell()
                    urllist.append(line[:-1])
                    line = f.readline()
                    count -=1
            yield urllist
            if len(urllist) != batch:break

def request(batch, patch=-1):
    for urllist in readUrl(batch, patch):
        reqs = [grequests.get(url, timeout=60) for url in urllist]
        reqs = grequests.map(reqs)
        for i in range(len(reqs)):
            if type(reqs[i]) == type(None):reqs[i]=404
            else:reqs[i]=reqs[i].status_code
        yield dict(zip(urllist,reqs))