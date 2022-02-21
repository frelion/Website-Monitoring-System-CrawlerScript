import flash.database as db

def write():
    with open("urls.txt","w") as f:
        for id, url in db.db_url():
            if id==-1:continue
            f.write(url)
            f.write('\n')