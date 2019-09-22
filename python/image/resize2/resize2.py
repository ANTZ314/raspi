from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_crop(img, [200, 200])
img.save('test-image-crop2.jpeg', img.format)
fd_img.close()