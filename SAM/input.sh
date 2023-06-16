#!/bin/bash          
path="ice_cream.jpeg"
output="output"
python3 SAM/scripts/amg.py --checkpoint sam_vit_h_4b8939.pth --model-type vit_h --input $path --output $output --device cpu 