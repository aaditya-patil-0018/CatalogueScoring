import cv2
import numpy as np
from Catalogue import Catalogue
import time
from concurrent.futures import ThreadPoolExecutor
import base64
from imquality.brisque import Brisque
from skimage import img_as_float, io
from io import BytesIO

class ImageScoring:
    def __init__(self, catalogue_data):
        self.catalogue_data = catalogue_data
        self.image_column_name = self.get_image_column()  
        if self.image_column_name:
            self.clear = 0  
            self.blur = 0   
            self.no_image = 0  
        else:
            print("No Image Column in the Catalogue!")  

    def get_image_column(self):
        for column in self.catalogue_data.columns:
            if "image" in column.lower():
                return column
        return None

    def check_clarity(self):
        def process_image(image_data):
            try:
                if image_data:
                    # Decode base64 image data and convert to numpy array
                    # image_data = base64.b64decode(image_data)
                    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
                    if laplacian_var > 50:
                        return "blur"
                    else:
                        return "clear"
                else:
                    return "no_image"
            except Exception as e:
                print(f"Error processing image: {e}")
                return "error"

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_image, self.catalogue_data[self.image_column_name]))

        self.clear = results.count("clear")
        self.blur = results.count("blur")
        self.no_image = results.count("no_image")
        
        return {"clear": self.clear, "blur": self.blur, "no_image": self.no_image}

if __name__ == "__main__":
    filename = "catalogue3.json"
    catalogue = Catalogue()
    catalogue_data = catalogue.open(filename)
    
    start_time = time.time()
    img_scoring = ImageScoring(catalogue_data)
    clarity_results = img_scoring.check_clarity()
    
    total_images = len(catalogue_data)
    clear_percentage = (clarity_results["clear"] / total_images) * 100
    blur_percentage = (clarity_results["blur"] / total_images) * 100
    no_image_percentage = (clarity_results["no_image"] / total_images) * 100
    
    print(f"Clear Image: {round(clear_percentage, 2)}%")
    print(f"Blur Image: {round(blur_percentage, 2)}%")
    print(f"No Image Percentage: {round(no_image_percentage, 2)}%")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
