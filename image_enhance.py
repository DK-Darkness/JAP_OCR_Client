
# coding: utf-8

import struct
import numpy as np
import os
import sys
import glob
from PIL import Image, ImageEnhance

RECORD_SIZE = 8199
i = 0

files = glob.glob("ETL8G/*")
for filename in files:
    print("Reading {}".format(filename))
    _,file_pre = filename.split('/')
    with open(filename, 'rb') as f:
        while True:
            s = f.read(RECORD_SIZE)
            if s is None or len(s) < RECORD_SIZE:
                break
            r = struct.unpack(">HH8sIBBBBHHHHBB30x8128s11x", s)
            img = Image.frombytes('F', (128, 127), r[14], 'bit', (4, 0))
            img = img.convert('L')
            i = i + 1
            dirname = b'\x1b$B' + r[1].to_bytes(2, 'big') + b'\x1b(B'
            dirname = dirname.decode("iso-2022-jp")
            try:
                os.makedirs(f"extract/{dirname}")
            except:
                pass
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(16)

            
            imagefile = f"extract/{dirname}/{file_pre}_{i:0>6}.png"
            print(imagefile)
            img.save(imagefile)

