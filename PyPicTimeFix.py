'''
This script will determine the difference between two dates and then
shift the EXIF metadata of all picture files in the same directory by
the date difference.
'''


from exif import Image, DATETIME_STR_FORMAT
import os
import datetime

# The currently set date and time of one of the pictures.
CURRENT_DATE = datetime.datetime(
    year = 2022,
    month = 1,
    day = 22,
    hour = 22,
    minute = 43,
    second = 26)

# The date you want to be set to the same picture.
DESIRED_DATE = datetime.datetime(
    year = 2022,
    month = 2,
    day = 1,
    hour = 0,
    minute = 0,
    second = 0)

# Whether to overwrite the "datedigitized"
# and "dateoriginal" EXIF fields.
OVERWRITE_DATEDIGITIZED = True
OVERWRITE_DATEORIGINAL = True


def change_image_datetime(
    image_filename,
    date_delta,
    overwrite_datedigitized,
    overwrite_dateoriginal):
    
    image = Image(image_filename)
    
    # Create a datetime object to store the current datetime data
    # so we can simply add the delta to the datetime object below.
    fixed_date = datetime.datetime(
        year = int(image.get("datetime")[0:4]),
        month = int(image.get("datetime")[5:7]),
        day = int(image.get("datetime")[8:10]),
        hour = int(image.get("datetime")[11:13]),
        minute = int(image.get("datetime")[14:16]),
        second = int(image.get("datetime")[17:]),
    )
    fixed_date -= date_delta
    
    if image.get("datetime") == "None" or image.get("datetime") == "":
        print(f"!!! NO EXIF DATA IN {image_filename}\n"
              + "!!! CANNOT DETERMINE ORIGINAL DATETIME\n"
              + "!!! IMAGE SKIPPED")
        return
    else:
        image.datetime = fixed_date.strftime(DATETIME_STR_FORMAT)
        print(f"SET {image_filename} DATETIME: {fixed_date}")
        
    if overwrite_datedigitized:
        image.datetime_digitized = fixed_date.strftime(DATETIME_STR_FORMAT)
        print(f"SET {image_filename} DATETIME_DIGITIZED: {fixed_date}")
        
    if overwrite_dateoriginal:
        image.datetime_original = fixed_date.strftime(DATETIME_STR_FORMAT)
        print(f"SET {image_filename} DATETIME_ORIGINAL: {fixed_date}")
    
    with open(image_filename, 'wb') as new_image_file:
        new_image_file.write(image.get_file())


file_count = 0
for file in os.listdir(os.getcwd()):
    if (file.lower().endswith((
            '.png', '.jpg',
            '.jpeg', '.tiff',
            '.bmp', '.gif'))):
        file_count += 1
    
print(f"{file_count} picture files were found\nContinue?")
if input() == "yes":
    for file in os.listdir(os.getcwd()):
        if (file.lower().endswith((
            '.png', '.jpg',
            '.jpeg', '.tiff',
            '.bmp', '.gif'))):
            change_image_datetime(
                file,
                (CURRENT_DATE - DESIRED_DATE),
                OVERWRITE_DATEDIGITIZED,
                OVERWRITE_DATEORIGINAL)
        else:
            continue
else:
    print("Press any key to exit.")
    input()
