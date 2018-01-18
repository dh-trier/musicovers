"""
This script uses the Clarifai API to recognize objects from images
"""


#Import Clarifai-specific packages
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
from ZZ_HelperModules import docfile

#Enter api_key between '...'
app = ClarifaiApp(api_key='')


current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "../2VV-daten", "2VV-005")
targetdatafile = join(workdir, "../4FE-daten", "4FE-006.csv")
documentationfile = join(workdir, "../4FE-daten", "4FE-006.txt")

def get_Objects ():
    #Save all files in a variable
    files = glob.glob(sourcedatafolder + "/*")
    #Amount of images in selected directory
    total_files = len(files)

    #Counts how often the while-loop is completed
    index = 0
    #Iterator
    counter = 0
    #Use a divisor that does not create a remainder to avoid IndexErrors!
    batch_size = 50

    file = codecs.open(targetdatafile, 'w', encoding='utf-8')
    file.write("Dateiname,Tag1,Tag1_P,Tag2,Tag2_P,Tag3,Tag3_P,Tag4,Tag4_P,Tag5,Tag5_P\n")
    file.close()

    while (counter < total_files):
       
        print ("Processing batch " + str(index+1))
        
        #Empty imageList after every iteration
        imageList=[]
        
        #Put images in imageList
        for x in range(counter,counter+batch_size):
            try:
                imageList.append(ClImage(filename=files[x]))
            except IndexError:
                break
        
        #Choose prediction model
        model = app.models.get('general-v1.3')
        #Use model on images
        data = model.predict(imageList)

        #Extract recognised tags and write into .csv-File
        file = codecs.open(targetdatafile, 'a', encoding='utf-8')
        split_paths = [os.path.basename(p) for p in files]
        
        for x in range(0,batch_size):  #write filename and top 5 objects into CSV file, counter bis counter+batch_size
            
            file.write(str(split_paths[index*batch_size+x])+ ";")
            
            i=0
            while i < 5:
                tags = data ['outputs'] [x] ['data'] ['concepts'][i]['name']
                value = data ['outputs'] [x] ['data'] ['concepts'] [i] ['value']
                file.write(tags + "," + str(value) + ",")
                if i == 4:
                    file.write("\n")
                i = i+1
        
        counter=counter+batch_size
        
        index=index+1
        file.close()
        
def main ():
    get_Objects()
    docfile.write(sourcedatafolder,targetdatafile, documentationfile, __doc__, tail, __file__)
    
    
main()




    

    





