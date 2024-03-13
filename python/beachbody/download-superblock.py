from __future__ import unicode_literals
import json
import youtube_dl
import os
import requests
import re
import sys

CLOUDFRONT_URL = 'https://d197pzlrcwv1zr.cloudfront.net/'
BASE_FOLDER = './'
INPUT_FILE = './program.json'


def getVideoFileName(dl_entity):
    name = dl_entity['slug']
    # new_name = name.replace('&', 'and')
    # new_name = re.sub(r'\W', '_', new_name)

    # while os.path.exists(new_name):
    #     new_name = new_name + ""


    return name

def download(url: str, file_path: str):
    if os.path.exists(file_path) :
        print('skipping download')
        return

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

def downloadVideo(url: str, filename: str):
    if os.path.exists(filename + '.mp4'):
        print('Skipping video')
        return

    conf_filename = filename + '.%(ext)s'

    ydl_opts = {
        'outtmpl' :conf_filename,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    

def downloadResource(dl_entity, folderName):
  file = dl_entity['file']
  filename = file['originalFilename']
  url = file['url']
  file_path = os.path.join(folderName, filename)
  print('Download ', url,'to', file_path)
  download(url, file_path)

def downloadWorkout(entity):
    # base_url = 'https://d197pzlrcwv1zr.cloudfront.net/'
    video = entity['video']
    videoId = video['videoId']
    fullURL = CLOUDFRONT_URL + videoId + '/' + videoId + '_Main_B.m3u8'
    filename = entity['slug']
    print('Download video: ', filename, 'from', fullURL)
    downloadVideo(fullURL, filename)

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
        folderName = os.path.join(BASE_FOLDER, 'materials/')
        createFolder(folderName)
        downloadResource(entity, folderName)

def createFolder(dest_folder):
    print("Folder: ", dest_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

def loadJson():
    print('Using JSON: ' + INPUT_FILE, 'output folder: ', BASE_FOLDER)
    createFolder(BASE_FOLDER)
    with open(INPUT_FILE, "r") as my_file:
        jsonObj = json.load(my_file)
        startParsing(jsonObj)
    print("Finished!")


def main():
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)
    if n < 2:
        print('Need to pass <graphq> and <outputfolder>')
    
    global BASE_FOLDER
    global INPUT_FILE

    INPUT_FILE = sys.argv[1]
    BASE_FOLDER = sys.argv[2]

    loadJson()

if __name__ == "__main__":
    main()