from exif import Image, DATETIME_STR_FORMAT
import os
import datetime
import piexif

# Define FIRST picture's current date, then enter it's desired date
CURRENT_DATE = datetime.datetime(1970, 1, 1)
DESIRED_DATE = datetime.datetime(2000, 1, 1)

timeDifference = CURRENT_DATE - DESIRED_DATE

def changeImageDateTime(imageFilename, offset):
    
    image = Image(imageFilename)
    
    if (image.get("datetime")) == "None":
        print(f"!!! {imageFilename} did not have EXIF -datetime- data so it wasn't changed and the image was skipped.")
        return
    else:
        newDateTime = image.datetime # + offset
        image.set("datetime", newDateTime)
        print(f"{imageFilename} + 's -datetime- field was set to {newDateTime}")
        
    if (image.get("datetime_digitized")) == "None":
        print(f"!!! {imageFilename} did not have EXIF -datetime_digitized- data so -datetime- will be written instead")
        image.set("datetime_digitized", image.datetime)
    else:
        newDateTime = image.datetime_digitized#  + offset
        image.set("datetime_digitized", newDateTime)
        print(f"{imageFilename}'s -datetime_digitized- field was set to {newDateTime}")
        
    if (image.get("datetime_original")) == "None":
        print(f"!!!{imageFilename} did not have EXIF -datetime_original- data so -datetime- will be written instead")
        image.set("datetime_original", image.datetime)
    else:
        newDateTime = image.datetime_original# + offset
        image.set("datetime_original", newDateTime)
        print(f"{imageFilename}'s -datetime_original- field was set to {newDateTime}")
    
    


# Get current directory
Directory = os.getcwd()

# Loop through images in that directory, check if file is a valid image, and change it's EXIF data
for file in os.listdir(Directory):
    if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
        changeImageDateTime(file, timeDifference)
    else:
        continue
