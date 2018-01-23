
from PIL import Image, ImageEnhance
import io
from google.cloud import vision
from google.cloud import language
from oauth2client.client import GoogleCredentials
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("image_directory", help="Location of images to be clipped- it feels sad if there are other files in this directory")
parser.add_argument("output_directory", help="Location where images will be stored")
args = parser.parse_args()

image_folder = args.image_directory
out_folder   = args.output_directory


credentials = GoogleCredentials.get_application_default()

vision_client = vision.Client.from_service_account_json('new_key.json')

language_client = language.Client()

PROCESS = False
#This section uses a bash files called textcleaner to create high contrast b/w images of each document file. http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
if PROCESS:
    for image_name in os.listdir(image_folder):
        with io.open(image_folder+image_name, 'rb') as image_file:
           
            os.system('textcleaner /Users/ajanco/projects/GAM/images/{} /Users/ajanco/projects/dylan/output/{}'.format(image_name, image_name))  
            print('saving {}'.format(file_name))

for image_name in os.listdir('/Users/ajanco/projects/dylan/output/hand/'):
    with io.open(image_folder+image_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)
        
        document = image.detect_full_text()
        boxes = []

        for page in document.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    boxes.append(paragraph.bounding_box)
                
           
        count = 0 
        SAVE = True
        SHOW = True

        
        im = Image.open(image_folder+image_name)

        if SHOW:
            im.show()
        for box in boxes:
            left  = min([box.vertices[i].x for i in range(4)]) - 10
            upper = min([box.vertices[i].y for i in range(4)]) - 10
            right = max([box.vertices[i].x for i in range(4)]) + 10 
            lower = max([box.vertices[i].y for i in range(4)]) + 10
            box = (left, upper, right, lower)
            region = im.crop(box)
            
            if SHOW:
                region.show()
                raw_input("Enter to open another image, Ctrl+C to kill")
            if SAVE:
                img_name = image_name.split('.')[0]
                extension = image_name.split('.')[1]
                region.save(out_folder+"/"+img_name+str(count)+'.'+extension)
                count += 1

