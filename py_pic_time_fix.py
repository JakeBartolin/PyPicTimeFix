'''This script will determine the difference between two dates and then
shift the EXIF metadata of all picture files in the same directory by
the date difference.
'''

from exif import Image, DATETIME_STR_FORMAT
import os
import datetime


def set_file_modification_time(filename, mtime):
    """
    Set the modification time of a given filename to the given mtime.
    mtime must be a datetime object.
    """
    stat = os.stat(filename)
    atime = stat.st_atime
    os.utime(filename, times=(atime, mtime.timestamp()))

def prompt_to_overwrite(field_to_overwrite):
    user_input = input("Do you want to overwrite the " +
            field_to_overwrite +
            "metadata field in these photos? (y/n) ")
    while user_input not in ['y', 'n']:
        user_input = input("Invalid input. Please enter 'y' or 'n': ")
        
    if user_input == "y":
        return True

    return False

def prompt_for_date(input_prompt):
    '''Prompts the user to input a date and time.
    then returns a datetime.datetime object based
    on the input.'''
    
    print(input_prompt)
    
    while True:
        try:
            year = int(input("Year (e.g. 2021): "))
            month = int(input("Month (1-12): "))
            day = int(input("Day (1-31): "))
            hour = int(input("Hour (0-23): "))
            minute = int(input("Minute (0-59): "))
            second = int(input("Second (0-59): "))
            
            datetime_obj = datetime.datetime(year, month, day, hour, minute, second)
            return datetime_obj
        except ValueError:
            print("Invalid input. Please try again.\n")

def print_num_of_pics(given_directory):
    '''Prints the number of picture files in a given directory.'''
    pic_count = 0
    for file in given_directory:
        if (file.lower().endswith((
            '.jpg',
            '.jpeg', '.tiff',
            '.bmp', '.gif'))):
            pic_count += 1
    print(str(pic_count) + " picture files were found in " + str(given_directory))

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

def print_goodbye_message(images_modified):
    print(f"{str(images_modified)} images were modified.")
    print(
        '''
        **************************************************************************************
        *                                  Script Complete                                   *
        **************************************************************************************'''
    )

def write_metadata(image, field_name, field_value, file_name):
    '''Attempts to write metadata to the given image metadata field.
    Prints a message on success or failure.'''
    try:
        metadata = field_value.strftime(DATETIME_STR_FORMAT)
        setattr(image, field_name, metadata)
        print("{} '{}' has been set to {}".format(file_name, field_name, field_value))
    except Exception as e:
        print("\033[0;31;40mCould not write '{}' for {}: {}\033[0;0m".format(field_name, file_name, e))

def change_file_data(
    file_name,
    date_delta,
    overwrite_datedigitized,
    overwrite_dateoriginal):

    # Create a datetime object to store the current datetime data
    # so we can simply subtract the delta from the datetime object
    # to get our final fixed_date. datetime.datetime handles the math
    image = Image(file_name)
    try:
        fixed_date = datetime.datetime(
            year = int(image.get("datetime")[0:4]),
            month = int(image.get("datetime")[5:7]),
            day = int(image.get("datetime")[8:10]),
            hour = int(image.get("datetime")[11:13]),
            minute = int(image.get("datetime")[14:16]),
            second = int(image.get("datetime")[17:]),
        )
    except:
        print("\033[0;31;40mCould not get 'datetime' data from " + file_name + " metadata\033[0;0m")
        try:
            print("\033[0;33;40mTrying to get datetime from 'datemodified'...\033[0;0m")
            fixed_date = os.path.getmtime(file_name)
            fixed_date = datetime.datetime.fromtimestamp(fixed_date)
            print("\033[0;32;40mGetting 'datetime' from 'datemodified' was successful!\033[0;0m")
        except:
            print("\033[0;31;40mUnable to get datetime from 'datemodified'.\033[0;0m")
            print("\033[0;30;41m" + file_name + " was skipped.\033[0;0m")
            return
    
    fixed_date -= date_delta

    write_metadata(image, "datetime", fixed_date)
    if overwrite_datedigitized:
        write_metadata(image, "datetime_digitized", fixed_date, file_name)
    if overwrite_dateoriginal:
        write_metadata(image, "datetime_original", fixed_date, file_name)
    
    try:
        set_file_modification_time(file_name, fixed_date)
        print("'file_modiication_time' set for " + file_name)
    except:
        print("\033[0;31;40mCould not set 'file_modification_datetime' for " + file_name + "\033[0;0m")

def main():
    print_num_of_pics(os.listdir(os.getcwd()))
    print("Continue? (y/n)")
    
    user_input = input("Continue? (y/n) ")
    while user_input not in ['y', 'n']:
        user_input = input("Invalid input. Please enter 'y' or 'n': ")
        
    if user_input == "y":
            # Ask the user input what date is there, what date needs
            # to be there, and what metadata fields to overwrite.
            current_date = prompt_for_date("Please enter the current (wrong) date for a photo.")
            desired_date = prompt_for_date("Please enter the desired (correct) date for the same photo.")
            overwrite_datedigitized = prompt_to_overwrite("datedigitized")
            overwrite_dateoriginal = prompt_to_overwrite("dateoriginal")
            
            # Try to open each file in the directory and write the date
            # offset in the appropriate field(s).
            images_modified = 0
            
            for file in os.listdir(os.getcwd()):
                try:
                    change_file_data(
                        file,
                        (current_date - desired_date),
                        overwrite_datedigitized,
                        overwrite_dateoriginal)
                    images_modified += 1
                except:
                    print("\033[0;31;40m" + file + " had a problem and was not modified.\033[0;0m")
                    
    print_goodbye_message(images_modified)

if __name__ == "__main__":
    main()
