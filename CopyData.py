from random import random
from os import listdir
from shutil import copyfile


val_ratio = 0.25

src_directory = 'PetImages/'
for file in listdir(f"{src_directory}/Dog/"):
    dst_dir = 'train/dogs/'
    src = src_directory + '/Dog/' + file
    if random() < val_ratio:
        dst_dir = "test/dogs/"
    dst = 'dataset/' + dst_dir + file
    copyfile(src, dst)

for file in listdir(f"{src_directory}/Cat/"):
    dst_dir = 'train/cats/'
    src = src_directory + '/Cat/' + file
    if random() < val_ratio:
        dst_dir = "test/cats/"
    dst = 'dataset/' + dst_dir + file
    copyfile(src, dst)