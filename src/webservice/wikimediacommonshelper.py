import os
import hashlib
import requests

# Utils to download test images from wikimedia commons

def download_tmp_file(url):
    user_agent="Ajapaik.ee OAUTH2 Uploader"
    headers={'User-Agent': user_agent}

    local_filename = "/tmp/" + hashlib.md5(url.encode('utf-8')).hexdigest() + ".jpg"
    print("Downloading " + local_filename + " " + url)
    r = requests.get(url, headers=headers)
    f = open(local_filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    return local_filename

def delete_tmp_file(url):
    local_filename = "/tmp/" + hashlib.md5(url.encode('utf-8')).hexdigest() + ".jpg"
    print("Deleting " + local_filename)
    if os.path.exists(local_filename):
        os.remove(local_filename)

def get_random_commons_image(level):
    ret={}
    url='https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=revisions%7Ccategories%7Cimageinfo&generator=random&rvprop=content&iiprop=timestamp%7Cuser%7Cmediatype%7Cmime%7Curl&grnnamespace=6&grnlimit=1'
    file=requests.get(url)
    data=file.json()
    for page_id in data["query"]["pages"]:
        page=data["query"]["pages"][page_id]
        if page["imageinfo"][0]["mime"]!="image/jpeg":
            if level<5:
                print("get_random_image() retrying")
                ret=get_random_commons_image(level+1)
                return ret
            else:
                print("get_random_image() retry failed")
                exit(1)
        ret["title"]=page["title"]
        ret["wikitext"]=page["revisions"][0]["*"]
        ret["mime"]= page["imageinfo"][0]["mime"]
        ret["image_url"]= page["imageinfo"][0]["url"]
        ret["description_url"]= page["imageinfo"][0]["descriptionurl"]

    return ret


