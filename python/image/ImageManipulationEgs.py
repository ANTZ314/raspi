#/home/antz/0Python/image/File.jpg

##########################################################
# Open and resize image
##########################################################
from PIL import Image
from resizeimage import resizeimage


with open('test-image.jpeg', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [200, 100])
        cover.save('test-image-cover0.jpeg', image.format)
        
##########################################################
# 2 stage Validation & resize -> ERROR?
##########################################################
from PIL import Image

from resizeimage import resizeimage

with open('/home/antz/0Python/image/File.jpg', 'r+b')
    with Image.open() as image:
        is_valid = resizeimage.resize_cover.validate(image, [200, 100])

# do something else...

if is_valid:
    with Image.open('/home/antz/0Python/image/File.jpg') as image:
        resizeimage.resize_cover.validate(image, [200, 100], validate=False)
        cover = resizeimage.resize_cover(image, [200, 100])
        cover.save('test-image-cover1.jpeg', image.format)

##########################################################
# Crop an image with a 200x200 cented square:
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_crop(img, [200, 200])
img.save('test-image-crop2.jpeg', img.format)
fd_img.close()

##########################################################
# Resize and crop (from center) the image so that it covers 
# a 200x100 rectangle
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_cover(img, [200, 100])
img.save('test-image-cover3.jpeg', img.format)
fd_img.close()

##########################################################
# Resize the image to minimum so that it is contained in a 
# 200x100 rectangle is the ratio between source and destination image
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_contain(img, [200, 100])
img.save('test-image-contain.jpeg', img.format)
fd_img.close()

##########################################################
# Resize the image to be 200px width:
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_width(img, 200)
img.save('test-image-width.jpeg', img.format)
fd_img.close()

##########################################################
# Resize the image to be 200px height:
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_height(img, 200)
img.save('test-image-height.jpeg', img.format)
fd_img.close()

##########################################################
# Resize the image to be contained in a 200px square:
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_thumbnail(img, [200, 200])
img.save('test-image-thumbnail.jpeg', img.format)
fd_img.close()

##########################################################
# Resize Image with the specified method : 
# ‘crop’, ‘cover’, ‘contain’, ‘width’, ‘height’ or ‘thumbnail’.
##########################################################
from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize('thumbnail', img, [200, 200])
img.save('test-image-thumbnail.jpeg', img.format)
fd_img.close()

########
# Tests:
########
pip install -r requirements.dev.txt
pip install -e .
python setup.py test











