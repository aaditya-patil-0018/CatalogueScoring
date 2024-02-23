# Import necessary libraries
import cv2
import numpy as np
import os
from Catalogue import Catalogue
import base64
from concurrent.futures import ThreadPoolExecutor
import time

# Class for scoring image clarity
class ImageScoring:
    def __init__(self, catalogue_data):
        self.catalogue_data = catalogue_data
        self.image_column_name = self.get_image_column()  # Get the column name containing image data
        if self.image_column_name:
            # self.start_time = time.time()  # Start time measurement
            self.clear = 0  # Counter for clear images
            self.blur = 0   # Counter for blurred images
            self.no_image = 0  # Counter for rows with no image data
            # self.check_clarity()  # Method to check clarity of images
        #     self.total_images = len(self.catalogue_data[self.image_column_name])  # Total number of images
        #     # Calculate percentages
        #     self.clear_percentage = (self.clear / self.total_images) * 100
        #     self.blur_percentage = (self.blur / self.total_images) * 100
        #     self.no_image_percentage = (self.no_image / self.total_images) * 100
        #     # Print results
        #     print(f"Clear Image: {round(self.clear_percentage, 2)}%")
        #     print(f"Blur Image: {round(self.blur_percentage, 2)}%")
        #     print(f"No Image Percentage: {round(self.no_image_percentage, 2)}%")
        #     end_time = time.time()  # End time measurement
        #     print(f"Time taken: {end_time - start_time} seconds")
        else:
            print("No Image Column in the Catalogue!")  # Inform if no image column is found

    # Method to get the column containing image data
    def get_image_column(self):
        image_column = None
        for column in self.catalogue_data.columns:
            if "image" in column.lower():
                image_column = column
                break
        return image_column

    # Method to check clarity of images
    def check_clarity(self):
        # Function to process images in batches
        def process_image_batch(batch):
            for image_data in batch:
                try:
                    if image_data and image_data.replace(" ","")!="":
                        # Decode base64 image data and convert to numpy array
                        image_bytes = base64.b64decode(image_data)
                        nparr = np.frombuffer(image_bytes, np.uint8)
                        # Decode image and convert to grayscale
                        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                        # Calculate Laplacian variance to determine clarity
                        laplacian_var = int(cv2.Laplacian(image, cv2.CV_64F).var())
                        if laplacian_var < 40:
                            self.blur += 1  # Increment blur count
                        else:
                            self.clear += 1  # Increment clear count
                    else:
                        self.no_image += 1  # Increment count for rows with no image data
                except Exception as e:
                    self.no_image += 1
                    print(f"Error processing image: {e}")  # Print error if image processing fails

        with ThreadPoolExecutor() as executor:
            batch_size = 100  # Adjust batch size as needed
            for i in range(0, len(self.catalogue_data), batch_size):
                batch = self.catalogue_data[self.image_column_name][i:i+batch_size]
                executor.submit(process_image_batch, batch)

        self.total_images = len(self.catalogue_data[self.image_column_name])  # Total number of images
        # Calculate percentages
        self.clear_percentage = (self.clear / self.total_images) * 100
        self.blur_percentage = (self.blur / self.total_images) * 100
        self.no_image_percentage = (self.no_image / self.total_images) * 100
        # Print results
        print(f"Clear Image: {round(self.clear_percentage, 2)}%")
        print(f"Blur Image: {round(self.blur_percentage, 2)}%")
        print(f"No Image Percentage: {round(self.no_image_percentage, 2)}%")
        # end_time = time.time()  # End time measurement
        # print(f"Time taken: {end_time - self.start_time} seconds")
        return {"clear": self.clear, "clear percentage": round(self.clear_percentage, 2),
                "blur": self.blur, "blur percentage": round(self.blur_percentage, 2),
                "no image": self.no_image, "no image percentage": round(self.no_image_percentage, 2)}
        

if __name__ == "__main__":
    filename = "catalogue3.json"  # Replace with your filename
    catalogue = Catalogue()  # Instantiate Catalogue class
    catalogue_data = catalogue.open(filename)  # Open catalogue data
    img_scoring = ImageScoring(catalogue_data)  # Initialize ImageScoring class with catalogue data
    img_scoring.check_clarity()
