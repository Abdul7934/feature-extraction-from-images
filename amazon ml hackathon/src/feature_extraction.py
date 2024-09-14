import os
import torch
import numpy as np
from PIL import Image
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

# Define a PyTorch dataset for image loading
class ImageDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, image_path

# Batch feature extraction function
def feature_extraction(image_paths, model, feature_folder, batch_size=32, device='cpu'):
    # Define the transform (resize, normalize)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Create the dataset and DataLoader
    dataset = ImageDataset(image_paths, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    # Move model to device (GPU or CPU)
    model = model.to(device)

    # Ensure feature folder exists
    if not os.path.exists(feature_folder):
        os.makedirs(feature_folder)

    # Set the model to evaluation mode
    model.eval()

    with torch.no_grad():
        for images, image_paths in tqdm(dataloader, desc="Extracting features"):
            # Move images to device
            images = images.to(device)

            # Extract features
            features = model(images)

            # Move features back to CPU for saving
            features = features.cpu().numpy()

            # Save each feature as a separate .npy file
            for i, feature in enumerate(features):
                image_name = os.path.basename(image_paths[i])
                feature_path = os.path.join(feature_folder, f'{image_name}.npy')
                np.save(feature_path, feature)

# Use the function to extract features
if __name__ == "__main__":
    # Load pre-trained ResNet50 model
    model = models.resnet50(pretrained=True)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove the final classification layer

    # Move to GPU if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Define paths
    IMAGE_FOLDER = '../images/'
    FEATURE_FOLDER = '../features/'

    # Get image paths
    image_paths = [os.path.join(IMAGE_FOLDER, img) for img in os.listdir(IMAGE_FOLDER)]

    # Run feature extraction with batch processing
    feature_extraction(image_paths, model, FEATURE_FOLDER, batch_size=64, device=device)
