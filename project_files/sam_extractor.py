def extract_images(mask_path, image_path, processed_path):
    import os
    import skimage
    import numpy as np
    
    # Load image
    image = skimage.io.imread(image_path)
    extracted_masks = []
    
    # Access all masks
    for file in os.listdir(mask_path):
        if file.endswith(".png"):
            # Load mask
            mask = skimage.io.imread(f"{mask_path}/{file}")
            # Binarize the mask
            mask[mask > 0] = 1
            result = np.zeros_like(image)

            # Update every channel
            for i in range(image.shape[-1]):
                result[..., i] = np.multiply(image[..., i], mask)

            # Find the bounding box
            bbox = np.argwhere(mask)
            (y_start, x_start), (y_stop, x_stop) = bbox.min(0), bbox.max(0) + 1 
            result = result[y_start:y_stop, x_start:x_stop]

            # Pad image
            result = np.pad(result, ((10, 10), (10, 10), (0, 0)))

            # Save output
            if not os.path.exists(processed_path):
                os.makedirs(processed_path)
            result = skimage.transform.resize(result, (300, 300), anti_aliasing=True)
            
            extracted_masks.append(result)
            skimage.io.imsave(f"{processed_path}/{file}", result)
            
    return extracted_masks