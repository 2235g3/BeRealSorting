from pathlib import Path
from PIL import Image

infoPath = "media/SXzdl11MMOUHptovcu3lrZdtMGf2-s-elve3ZUjanPiQ04t87k/"
mediaPath = infoPath + "Photos/"
rP = Path(infoPath)
mP = Path(mediaPath)
infoArr = list(rP.glob("*.json"))
imgArr = list(mP.glob("post/*.WEBP"))
vidArr = list(mP.glob("post/*.MP4"))

imgData = Image.open(imgArr[0].as_posix())
imgData.save(mediaPath + "post/filename.webp") #  Creates a new image, not save the edit to old image

#for img in imgArr:
#    imgName = img.name
#    imgData = Image.open(img.as_posix())
#    print(imgData.info)
