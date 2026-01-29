import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


PIL_TAGS = [0x0132, 0x010E, 0x9286, 0x02, 0x04]

#  Defines the path objects
infoPath = "media/SXzdl11MMOUHptovcu3lrZdtMGf2-s-elve3ZUjanPiQ04t87k/"
mediaPath = infoPath + "Photos/"
rP = Path(infoPath)
mP = Path(mediaPath)

#  Fills each array with filenames from respective dirs
infoArr = list(rP.glob("*.json"))
imgArr = list(mP.glob("post/*.WEBP"))
vidArr = list(mP.glob("post/*.MP4"))

#  Loads the json objs for the relevant fields
memoryInfo = json.loads(infoArr[4].read_text(encoding="utf-8"))
postInfo = json.loads(infoArr[5].read_text(encoding="utf-8"))
realmojiInfo = json.loads(infoArr[8].read_text(encoding="utf-8"))

#  Makes both arrays the same so they can be iterated over
equalizer = len(postInfo) - len(memoryInfo)
for x in range(equalizer):
    memoryInfo.append({})

#  Formats all photo paths so the are all uniform
def addFSlash(path):
    if (path.startswith("P")):
        path = "/" + path
    return path


#  Formats the date for use as the file name
def dateFormat(dateTime):
    dateTime = dateTime.replace("T", "_")
    dateTime = dateTime.replace(":", "-")
    dateTime = dateTime.split(".")[0]
    return dateTime

#  Adding relevant image data as metadata
for img in imgArr:
    imgData = Image.open(img.as_posix())
    ogImgPath = Path(imgData.filename)
    memoryMeta = []

    #  Retrieving and updating from/to the relevant json files
    for x in range(len(postInfo)):
        frontPath = addFSlash(postInfo[x]["primary"]["path"])
        backPath = addFSlash(postInfo[x]["secondary"]["path"])
        
        try:
            music = memoryInfo[x]["music"]
        except:
            music = {"track": None, "artist": None, "openUrl": None, "artwork": None, "provider": None}

        try:
            location = memoryInfo[x]["location"]
        except:
            location = {"latitude": 0, "longitude": 0}

        try:
            caption = memoryInfo[x]["caption"]
        except:
            caption = "No caption provided"

        try:
            isLate = memoryInfo[x][isLate]
        except:
            isLate = None

        try:
            beRealMoment = datetime.strptime(memoryInfo[x]["berealMoment"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            beRealMoment = None

        try:
            date = datetime.strptime(postInfo[x]["takenAt"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y:%m:%d %H:%M:%S")
        except:
            date = None

        extraInfo = f"Taken Late: {isLate} \nRetake Counter: {postInfo[x]["retakeCounter"]} \nBeReal Time: {beRealMoment} \nMusic track: {music["track"]} \nMusic Artist: {music["artist"]} \nMusic URL: {music["openUrl"]} \nMusic Artwork: {music["artwork"]} \nMusic Provider: {music["provider"]}"
        memoryMeta = [dateFormat(postInfo[x]["takenAt"]), date, caption, extraInfo,
                      location["latitude"], location["longitude"]]

        if str(ogImgPath.name) in str(frontPath):
            memoryMeta[0] += "_Front"
            memoryInfo[x].update({"frontImage":{"path": frontPath.replace(ogImgPath.name, (memoryMeta[0] + ".webp"))}})
            break
        elif str(ogImgPath.name) in str(backPath):
            memoryMeta[0] += "_Back"
            memoryInfo[x].update({"backImage":{"path": backPath.replace(ogImgPath.name, (memoryMeta[0] + ".webp"))}})
            break

    imgExif = imgData.getexif()
    for j in range(len(PIL_TAGS)):
        imgExif[PIL_TAGS[j]] = memoryMeta[j + 1]
    print(imgExif)

    imgData.save(mediaPath + "post/" + memoryMeta[0] + ".webp", exif=imgExif) #  Creates a new image, not save the edit to old image

    ogImgPath.unlink() #  Deletes original image