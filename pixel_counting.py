import sys
import os
import argparse
import pandas as pd
import json
import cv2


def main():
    parser = argparse.ArgumentParser(description="Plot abundances from file.")
    parser.add_argument('--input_folder', dest='inp_f', type=str, help="path to input folder", required=False, default="output/ice_cream")  
    args = parser.parse_args()


    # Get metadata
    metadata = pd.read_csv(os.path.join(args.inp_f, "metadata.csv"))

    ids= metadata["id"].tolist()[1:]
    areas = metadata["area"].tolist()[1:]


    id_to_pixel_count = {}
    for i,id in enumerate(ids): 
        # load image corresponding to id
        img = cv2.imread(os.path.join(args.inp_f, str(id) + ".png"), cv2.IMREAD_GRAYSCALE)
        # the masks are black and white so calculate the number of white pixels
        pixel_count = cv2.countNonZero(img)
        assert pixel_count == areas[i]
        id_to_pixel_count[id] = {}
        id_to_pixel_count[id]["area/pixel_count"]  = areas[i]

    # find masks that include other masks and remove them, using bounding box information
    ids_removed = set()
    for id in ids:
        bbox_x0_id = metadata[metadata["id"] == id]["bbox_x0"].tolist()[0]
        bbox_y0_id = metadata[metadata["id"] == id]["bbox_y0"].tolist()[0]
        bbox_w_id = metadata[metadata["id"] == id]["bbox_w"].tolist()[0]
        bbox_h_id = metadata[metadata["id"] == id]["bbox_h"].tolist()[0]
        for id2 in ids:
            if id == id2:
                continue

            bbox_x0_id2 = metadata[metadata["id"] == id2]["bbox_x0"].tolist()[0]
            bbox_y0_id2 = metadata[metadata["id"] == id2]["bbox_y0"].tolist()[0]
            bbox_w_id2 = metadata[metadata["id"] == id2]["bbox_w"].tolist()[0]
            bbox_h_id2 = metadata[metadata["id"] == id2]["bbox_h"].tolist()[0]

            # if id2 is inside id
            if bbox_x0_id2 >= bbox_x0_id and bbox_y0_id2 >= bbox_y0_id and bbox_x0_id2 + bbox_w_id2 <= bbox_x0_id + bbox_w_id and bbox_y0_id2 + bbox_h_id2 <= bbox_y0_id + bbox_h_id:
                # remove id2
                ids_removed.add(id2)
                print ("id2", id2, "is inside id", id)
    
    print("ids_removed", ids_removed)
    for id in ids_removed:
        del id_to_pixel_count[id]

    # calculate total pixel count
    total_pixel_count = 0
    for id in id_to_pixel_count:
        total_pixel_count += int(id_to_pixel_count[id]["area/pixel_count"])
    
    print("total_pixel_count", total_pixel_count)
    # Calculate percentage of each mask
    for id in id_to_pixel_count:
        id_to_pixel_count[id]['area_percentage'] =  id_to_pixel_count[id]["area/pixel_count"] / total_pixel_count

     
    # save to json
    with open(os.path.join(args.inp_f, "pixel_count.json"), 'w') as fp:
        json.dump(id_to_pixel_count, fp)
 
    return



if __name__ == "__main__":
    sys.exit(main())