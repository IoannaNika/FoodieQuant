def get_classes():
    return ['cauliflower','lemon','biscuit','french_fries','lettuce','bread','cheese','rice','potato','celery_stick',
            'green_beans','blueberry','spring_onion','carrot','grape','corn','fish','juice','cilantro_mint','sausage',
            'other_ingredients','strawberry','cucumber','fried_meat','egg','asparagus','tomato','pork','coffee','french_beans',
            'pepper','pasta','poultry','steak','onion','broccoli','pie','noodles','ice_cream','apple','cake','orange','tomato_sauce']

def show_annotations(masks):
    import matplotlib.pyplot as plt
    import numpy as np
    
    if len(masks) == 0:
        return
    sorted_masks = sorted(masks, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_masks[0]['segmentation'].shape[0], sorted_masks[0]['segmentation'].shape[1], 4))
    img[..., 3] = 0
    for ann in sorted_masks:
        mask = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[mask] = color_mask
    ax.imshow(img)
    
def get_api_key(filename="secret.txt"):
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)