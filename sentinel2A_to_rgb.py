import snappy
jpy = snappy.jpy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import ProgressMonitor
import sys
from datetime import *


def write_rgb_image(bands, filename, format):
    print("Creating image info")
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    print("Creating colored band image")
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    print("Creating file")
    JAI.create("filestore", im, filename, format)


if len(sys.argv) != 3:
    print("usage: %s <file> <savefile>" % sys.argv[0])
    sys.exit(1)

ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')

file = sys.argv[1]
savefile = sys.argv[2]

print("************* Saving " + file + " to " + savefile + "******************")

startedTime = datetime.now(timezone.utc)

print("Reading Product")
p = ProductIO.readProduct(file)

print("Reading Bands")
b2 = p.getBand('B2')
b3 = p.getBand('B3')
b4 = p.getBand('B4')

bands = [b4, b3, b2]

print("Start writing...")

write_rgb_image(bands, savefile, "png")

endedTime = datetime.now(timezone.utc)

print("completed in " + str(endedTime - startedTime))
