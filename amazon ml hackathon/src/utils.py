import os
import re
import requests
from pathlib import Path
from PIL import Image
import multiprocessing
from functools import partial
from tqdm import tqdm
import urllib.request
import time
import constants
from src import constants


# Utility function to correct common mistakes in unit names
def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    corrections = {
        'ter': 'tre',
        'feet': 'foot'
    }
    for wrong, correct in corrections.items():
        if wrong in unit:
            return unit.replace(wrong, correct)
    return unit

# Parses a string to extract the number and unit
def parse_string(s):
    s_stripped = "" if s is None or str(s).strip().lower() == 'nan' else s.strip()
    if not s_stripped:
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

# Creates a placeholder image if image download fails
def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

# Downloads a single image with retry logic
def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for attempt in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except Exception as e:
            print(f"Download failed for {image_link}: {e}")
            time.sleep(delay)

    # If all retries fail, create a placeholder image
    create_placeholder_image(image_save_path)

# Downloads multiple images using multiprocessing
def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        # Use a reasonable number of processes for efficiency
        num_processes = min(multiprocessing.cpu_count(), 64)
        with multiprocessing.Pool(num_processes) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links), desc="Downloading Images"))
    else:
        for image_link in tqdm(image_links, total=len(image_links), desc="Downloading Images"):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)
