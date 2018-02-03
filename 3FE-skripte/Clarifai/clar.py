"""
This script uses the Clarifai API to recognize objects from images.
"""

# import Clarifai-specific packages
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
#Import other needed packages
import json
import codecs
import glob
import os
from os.path import join
import os.path
import re
import docfile
from collections import Counter

# enter api_key between '...'
app = ClarifaiApp(api_key='...')

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "../2VV-daten", "2VV-009")
targetdatafile = join(workdir, "../4FE-daten/recognized_objects", "all_files.csv")
targetdatafile_2 = join(workdir, "../4FE-daten/recognized_objects", "all_objects.csv")
documentationfile = join(workdir, "../4FE-daten", "4FE-006.txt")


# ===============
# Functions
# ===============

object_list = []

def count_objects(list_of_objects):
    #counts how often objects were found
    data = Counter(list_of_objects)
    return data

def write_objects_to_csv ():
    data = count_objects(object_list)
    file = codecs.open(targetdatafile_2, 'w' , encoding='utf-8')
    file.write("Unique Tags" + "\t"  + "Frequency" + "\n")
    for object, amount in data.items():
        file.write(object + "\t" + str(amount) + "\n")
    file.close()
    
def get_objects ():
    # save all files in a variable
    files = glob.glob(sourcedatafolder + "/*")
    # amount of images in selected directory
    total_files = len(files)
    # counts how often the while-loop is completed
    index = 0
    # iterator
    counter = 0
    # use a divisor that does not create a remainder to avoid IndexErrors!
    batch_size = 32

    # create CSV header
    file = codecs.open(targetdatafile, 'w', encoding='utf-8')
    file.write("filename,hash,tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8,tag9,tag10,tag11,tag12,tag13,tag14,tag15,tag16,tag17,tag18,tag19,tag20\n")
    file.close()

    # iterate over all files
    while counter < total_files:
        print("Processing batch " + str(index + 1))
        
        # empty imageList after every iteration
        imageList = []
        
        # put images in imageList
        for x in range(counter, counter + batch_size):
            try:
                imageList.append(ClImage(filename=files[x]))
            except (IndexError) as e:
                print("Error: " + e)
        
        # choose prediction model
        try:
            model = app.models.get('general-v1.3')
        # use model on images
            data = model.predict(imageList)
        #handle unknown ApiError
        except:
                print("Error!")
        
        
        # extract recognized tags and write into .csv-File
        file = codecs.open(targetdatafile, 'a', encoding='utf-8')
        split_paths = [os.path.basename(p) for p in files]
            
        for x in range(0, batch_size):  # write filename and top 5 objects into CSV file; from counter to counter + batch_size
            filename = split_paths[index * batch_size + x]  # get full file name
            image_hash = re.search('[^_]*_([^_]*)', filename)  # get hash
            image_hash = image_hash.group(1)
            file.write(filename + "," + image_hash)  # write filename and hash to CSV file
                
            i = 0
            while i < 20:
                tags = data ['outputs'][x]['data']['concepts'][i]['name']
                object_list.append(tags)
                file.write("," + tags)
                if i == 19:
                    file.write("\n")
                i = i + 1
            
        counter = counter + batch_size
            
        index = index + 1
        file.close()
       

def main():
    get_objects()
    write_objects_to_csv()
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, __doc__, tail, __file__)


main()
