'''This script will determine the difference between two dates and then
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


def is_file_type_pic(filename):
    '''Returns True is the given filename of type string ends in
    .png .jpg .jpeg .tiff .bmp or .gif.
    '''
    if (filename.lower().endswith((
            '.png', '.jpg',
            '.jpeg', '.tiff',
            '.bmp', '.gif'))):
        return True
    return False

def print_num_of_pics(given_directory):
    '''Prints the number of picture files in a given directory.'''
    pic_count = 0
    for file in given_directory:
        if is_file_type_pic(file):
            pic_count += 1
    print(f"{pic_count} picture files were found.")    

def write_metadata(image, exif_field, metadata):
    metadata = metadata.strftime(DATETIME_STR_FORMAT)
    setattr(image, exif_field, metadata)
    print(f"SET {image.name} DATETIME: {metadata}")

def change_image_datetime(
    image_filename,
    date_delta):

    # Create a datetime object to store the current datetime data
    # so we can simply subtract the delta from the datetime object
    # to get our final fixed_date. datetime.datetime handles the math
    image = Image(image_filename)
    fixed_date = datetime.datetime(
        year = int(image.get("datetime")[0:4]),
        month = int(image.get("datetime")[5:7]),
        day = int(image.get("datetime")[8:10]),
        hour = int(image.get("datetime")[11:13]),
        minute = int(image.get("datetime")[14:16]),
        second = int(image.get("datetime")[17:]),
    )
    fixed_date -= date_delta
    
    if (image.get("datetime") == "None" or
        image.get("datetime") == "" or
        image.get("datetime") == None):
        # Since there is no datetime data in field to work with
        # we throw a message telling the user and then stop working
        # with this image.
        print(f"!!! NO EXIF DATA IN {image_filename}\n"
              + "!!! CANNOT DETERMINE ORIGINAL DATETIME\n"
              + "!!! IMAGE SKIPPED")
        return

    write_metadata(image, "datetime", fixed_date)
    if OVERWRITE_DATEDIGITIZED:
        write_metadata(image, "datetime_digitized", fixed_date)  
    if OVERWRITE_DATEORIGINAL:
        write_metadata(image, "datetime_original", fixed_date)
    with open(image_filename, 'wb') as new_image_file:
        new_image_file.write(image.get_file())

def main():
    print_num_of_pics(os.listdir(os.getcwd()))
    print("Continue? (y/n)")
    # TODO: Clean this up. (Break into functions?)
    while True:
        user_input = input()
        if user_input == "y":
            for file in os.listdir(os.getcwd()):
                if is_file_type_pic(file):
                    change_image_datetime(
                        file,
                        (CURRENT_DATE - DESIRED_DATE))
                else:
                    continue
        elif user_input == "n":
            print("Program will now exit.")
            break
        else:
            print("invalid input, please try again.")

if __name__ == "__main__":
    main()
