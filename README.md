# py_pic_time_fix
 A small python 3 script to adjust the EXIF metadata time of a set of photos by a given offset.

 # Usage
 0. **Make a backup of all the photos you want to change the date on.** The error checking of `PyPicTimeFix` is pretty scarce and if something goes wrong you want to be able to revert back to your original files.
 1. Move the `PyPicTimeFix.py` file into the same folder as your photos you want to adjust.
 2. Open `PyPicTimeFix.py` in any text editor of your choice.
 3. Go to the `CURRENT_DATE` section and enter the date that is **currently** set for one of your pictures.
 4. Go right below it to the `DESIRED_DATE` section and enter the date that you want that same picture to have.
 5. Check the `OVERWRITE_DATEDIGITIZED` and `OVERWRITE_DATEORIGINAL` variables. Setting these to `True` will make the script overwrite the `datedigitized` and `dateoriginal` metadata fields with the new date.
    - Many apps and programs will look at the `dateoriginal` field to get the date of the photo. This is why I reccommend you keep these set where they are, but if you're using scanned images or need to keep the dates untouched there is a way to turn this off.
6. Save and close `PyPicTimeFix.py`.
7. Run the script. The easiest way to do this is from your terminal of choice by navigating to the directory the script is in and entering something like `python3 PyPicTimeFix.py`
    - (TODO: Make the usage guide a bit more noob friendly.)
