from exif import Image, DATETIME_STR_FORMAT
import os
import datetime

# Define FIRST picture's current date, then enter it's desired date
CURRENT_DATE = datetime.datetime(year = 2022, month = 1, day = 22, hour = 22, minute = 43, second = 26)
DESIRED_DATE = datetime.datetime(year = 2022, month = 2, day = 1, hour = 0, minute = 0, second = 0)

# Change these variables to 'True' to overwrite the "date digitized" and/or "date created" EXIF fields
OVERWRITE_DATEDIGITIZED = True
OVERWRITE_DATEORIGINAL = True

TimeDelta = CURRENT_DATE - DESIRED_DATE

def changeImageDateTime(imageFilename, timeDelta, OVERWRITE_DATEDIGITIZED, OVERWRITE_DATEORIGINAL):
    
    image = Image(imageFilename)
    fileTrueDate = datetime.datetime(
        year = int(image.get("datetime")[0:4]),
        month = int(image.get("datetime")[5:7]),
        day = int(image.get("datetime")[8:10]),
        hour = int(image.get("datetime")[11:13]),
        minute = int(image.get("datetime")[14:16]),
        second = int(image.get("datetime")[17:]),
    )
    fileTrueDate -= timeDelta # 
    
    if image.get("datetime") == "None" or image.get("datetime") == "":
        print(f"!!! NO EXIF DATA IN {imageFilename}\n!!! CANNOT DETERMINE ORIGINAL DATETIME\n!!! IMAGE SKIPPED")
        return
    else:
        image.datetime = fileTrueDate.strftime(DATETIME_STR_FORMAT)
        print(f"SET {imageFilename} DATETIME: {fileTrueDate}")
        
    if OVERWRITE_DATEDIGITIZED:
        image.datetime_digitized = fileTrueDate.strftime(DATETIME_STR_FORMAT)
        print(f"SET {imageFilename} DATETIME_DIGITIZED: {fileTrueDate}")
        
    if OVERWRITE_DATEORIGINAL:
        image.datetime_original = fileTrueDate.strftime(DATETIME_STR_FORMAT)
        print(f"SET {imageFilename} DATETIME_ORIGINAL: {fileTrueDate}")
    
    with open(imageFilename, 'wb') as new_image_file:
        new_image_file.write(image.get_file())

# Get current directory
Directory = os.getcwd()

# Loop through images in that directory, check if file is a valid image, and change it's EXIF data based on timeDifference
for file in os.listdir(Directory):
    if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
        changeImageDateTime(file, TimeDelta, OVERWRITE_DATEDIGITIZED, OVERWRITE_DATEORIGINAL)
    else:
        continue
