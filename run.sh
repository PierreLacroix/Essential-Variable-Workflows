unzip data/s2.zip -d /tmp/unzipped

python sentinel2A_to_rgb.py /tmp/unzipped/*/MTD_MSIL1C.xml data/s2.png