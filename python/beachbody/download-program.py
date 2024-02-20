from __future__ import unicode_literals
import json
import youtube_dl
import os
import requests
import re

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    #filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    filename = url.split('file=', 1)[1]
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def getVideoFileName(dl_entity):
    name = dl_entity['slug']
    # new_name = name.replace('&', 'and')
    # new_name = re.sub(r'\W', '_', new_name)

    # while os.path.exists(new_name):
    #     new_name = new_name + ""


    return name

def downloadWorkout(dl_entity):
    base_url = 'https://d197pzlrcwv1zr.cloudfront.net/'
    video = dl_entity['video']
    videoId = video['videoId']
    fullURL = base_url + videoId + '/' + videoId + '_Main_B.m3u8'
    filename = getVideoFileName(dl_entity) + '.%(ext)s'

    ydl_opts = {
        'outtmpl' :filename,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([fullURL])
    

def downloadResource(dl_entity):
  file = dl_entity['file']
  url = file['url']
  download(url, './materials')



def startParsing(data):
  pageProps = data['pageProps']
  block = pageProps['block']
  entities = block['entities']
  for i in entities:
      entity = entities[i]
      entity_type = entity['_type'];
      if entity_type == 'workout':
        downloadWorkout(entity)
      elif entity_type == 'resource': 
        downloadResource(entity)

def loadJson():
    with open("./program.json", "r") as my_file:
        data = json.load(my_file)
        startParsing(data)


def main():
    loadJson()

if __name__ == "__main__":
    main()