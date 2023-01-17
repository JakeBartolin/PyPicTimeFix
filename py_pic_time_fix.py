'''This script will determine the difference between two dates and then
shift the EXIF metadata of all picture files in the same directory by
the date difference.
'''


from exif import Image, DATETIME_STR_FORMAT
import os
import datetime

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

def get_num_of_pics_in(given_directory):
    '''Prints the number of picture files in a given directory.'''
    pic_count = 0
    for file in given_directory:
        if is_file_type_pic(file):
            pic_count += 1
    return pic_count 

def print_welcome_message():
    print("""\n
    **************************************************************************************
    *                                     MIT License                                    *
    **************************************************************************************
    
    Copyright (c) 2023 Jacob Bartolin
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
    
    
    
    **************************************************************************************
    *                             Welcome to Py Pic Time Fix                             *
    **************************************************************************************
    
    This script works by finding the difference between the known (wrong) date
    of one of your photos and the desired (correct) date of the same photo. Then
    it will re-date all photos in the same folder as the script by that difference.
    
    Before beginning, make sure all the photos you want to change the date on are in
    the same folder as this script file. Make sure you also have a BACKUP of all the
    photos in case something goes wrong.
    
    """)

def write_metadata(image, exif_field, metadata):
    """Writes the given metadata to the given EXIF field of the
    given image object.
    """
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

def input_datetime_dialog():
    """Returns a datetime object after prompting the user to enter
    the year, month, day, hour, minute and second.
    """
    year = input("Please enter the year: ")
    month = input("Please enter the month: ")
    day = input("Please enter the day: ")
    hour = input("Please enter the hour: ")
    minute = input("Please enter the minute: ")
    second = input("Please enter the second: ")
    return datetime.datetime(year, month, day, hour, minute, second)

def main():
    print_welcome_message()
    print("First, let's get the current (wrong) date of one of the pictures.")
    current_date = input_datetime_dialog()
    print("Next, let's get the desired (correct) date of THE SAME PICTURE.")
    desired_date = input_datetime_dialog()

    print(f"I see {get_num_of_pics_in(os.listdir(os.getcwd()))} picture files in this folder.\nContinue? (y/n)")
    if input() == "y":
        for file in os.listdir(os.getcwd()):
            if is_file_type_pic(file):
                change_image_datetime(
                    file,
                    (current_date - desired_date))
            else:
                continue
        print("\n\nScript Complete.\n\n")
    else:
        print("Script Stopped")

if __name__ == "__main__":
    main()
