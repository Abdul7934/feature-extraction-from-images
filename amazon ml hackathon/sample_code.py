import os
import pandas as pd
import random
import re
from PIL import Image
import urllib.request
from pathlib import Path
import multiprocessing
from functools import partial
import time
from tqdm import tqdm
import constants
import sanity

def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def parse_string(s):
    s_stripped = "" if s is None or str(s) == 'nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError(f"Invalid format in {s}")
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in constants.allowed_units:
        raise ValueError(f"Invalid unit [{unit}] found in {s}. Allowed units: {constants.allowed_units}")
    return number, unit

def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except Exception as e:
            print(f"Error downloading image {image_link}: {e}")
            time.sleep(delay)
    
    create_placeholder_image(image_save_path)

def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(64) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links)))
            pool.close()
            pool.join()
    else:
        for image_link in tqdm(image_links, total=len(image_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)

def predictor(image_link, category_id, entity_name):
    '''
    Call your model/approach here
    '''
    # Placeholder for model loading and prediction logic
    # Example: prediction = model.predict(image_features)
    
    # Use dummy logic for demonstration
    try:
        # Implement your model prediction here
        # For demonstration purposes
        if random.random() > 0.5:
            return f"{random.uniform(1, 100):.2f} {random.choice(list(constants.entity_unit_map.get(entity_name, [])))}"
        return ""
    except Exception as e:
        print(f"Error in prediction for image {image_link}: {e}")
        return ""

if __name__ == "__main__":
    DATASET_FOLDER = '../dataset/'
    
    # Load test dataset
    test_file = os.path.join(DATASET_FOLDER, 'test.csv')
    test = pd.read_csv(test_file)
    
    # Prepare download folder and download images
    download_folder = os.path.join(DATASET_FOLDER, 'images')
    download_images(test['image_link'].tolist(), download_folder, allow_multiprocessing=True)
    
    # Generate predictions
    test['prediction'] = test.apply(
        lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1)
    
    # Save predictions to output file
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    test[['index', 'prediction']].to_csv(output_filename, index=False)
    
    # Perform sanity check
    sanity.sanity_check(test_file, output_filename)
