from __future__ import unicode_literals
import json
import os
import requests
import youtube_dl
import sys

CLOUDFRONT_URL = 'https://d197pzlrcwv1zr.cloudfront.net/'
BASE_FOLDER = './'
INPUT_FILE = './program.json'

def startParsing(jsonObj):
    data = jsonObj['data']
    getProgramDetailsBySlug = data['getProgramDetailsBySlug']
    for item in getProgramDetailsBySlug:
        meta_box = item['meta_box']
        subNav = meta_box['subNav']
        for item2 in subNav:
            # print(item2['id'], ' - ', item2['title'])
            if item2['title'] == 'Workouts':
                videoGroups = item2['videoGroups']
                parseVideoGroups(videoGroups)
        components = meta_box['components']
        parseComponents(components)

def parseComponents(components):
    componentProgramMaterialsResources = components['componentProgramMaterialsResources']
    resources = componentProgramMaterialsResources ['resources']
    folderName = BASE_FOLDER + 'materials/'
    createFolder (folderName)
    for resource in resources:
        category = resource['category']
        catName = category['slug']
        folderName = folderName + catName
        createFolder (folderName)
        parseResources(folderName, resource['resources'])

def parseResources(folderName, resources):
    for resource in resources:
        meta_box = resource['meta_box']
        attachment = meta_box['attachment']
        if attachment:
            print(attachment['url'], folderName)
            # download(attachment['url'], folderName)


def parseVideoGroups(videoGroups):
    for item in videoGroups:
        folderName = BASE_FOLDER + item['slug'] + "/"
        createFolder(folderName)
        meta_box = item['meta_box']
        videos = meta_box['videos']
        parseVideos(folderName, videos)

def parseVideos(folderName, videos) :
    for item in videos: 
        outputFile = folderName + item['slug']
        # print('-- Video output: ', outputFile)
        meta_box = item['meta_box']
        mpxVideo = meta_box['mpxVideo']

        parseMPXVideo(outputFile, mpxVideo)


def parseMPXVideo(outputFile, mpxVideo):
    meta_box = mpxVideo['meta_box']
    guid = meta_box['guid']
    stream_url = CLOUDFRONT_URL + guid + '/' + guid + "_Main_B.m3u8"
    print(stream_url, outputFile)
    # downloadWorkout(stream_url, outputFile)

def createFolder(dest_folder):
    print("Folder: ", dest_folder)
    # if not os.path.exists(dest_folder):
    #     os.makedirs(dest_folder)  # create folder if it does not exist


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

def downloadWorkout(filename, url):
    # base_url = 'https://d197pzlrcwv1zr.cloudfront.net/'
    # video = dl_entity['video']
    # videoId = video['videoId']
    # fullURL = base_url + videoId + '/' + videoId + '_Main_B.m3u8'
    outFile = filename + '.%(ext)s'

    ydl_opts = {
        'outtmpl' :outFile,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def loadJson():
    print('Using JSON: ' + INPUT_FILE, 'output folder: ', BASE_FOLDER)
    createFolder(BASE_FOLDER)
    with open(INPUT_FILE, "r") as my_file:
        jsonObj = json.load(my_file)
        startParsing(jsonObj)


def main():
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)
    if n < 2:
        print('Need to pass <graphq> and <outputfolder>')
    
    global BASE_FOLDER
    global INPUT_FILE

    INPUT_FILE = sys.argv[1]
    BASE_FOLDER = sys.argv[2] + '/'

    loadJson()

if __name__ == "__main__":
    main()