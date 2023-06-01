#!/bin/bash          
path="/Users/ioanna/Downloads/FoodSeg103/Images/img_dir/train/00000000.jpg"
output="output"
python3 scripts/amg.py --checkpoint sam_vit_h_4b8939.pth --model-type vit_h --input $path --output $output --device cpu 