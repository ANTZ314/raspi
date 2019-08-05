from PIL import Image
from resizeimage import resizeimage

fd_img = open('/home/antz/0Python/image/File.jpg', 'r')
img = Image.open(fd_img)
img = resizeimage.resize_contain(img, [200, 100])
img.save('test-image-contain.jpeg', img.format)
fd_img.close()
