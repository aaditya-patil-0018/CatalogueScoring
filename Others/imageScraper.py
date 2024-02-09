# scraping the images
import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import pandas as pd
import os
import time

filename = "../Datasets/flipkart_com-ecommerce_sample.csv"
dataFile = pd.read_csv(filename)

# Function to download the image using wget command
def runcmd(cmd, verbose = False, *args, **kwargs):
    # creating the process
    process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True, shell = True)
    # starting the process
    std_out, std_err = process.communicate()
    # if verbose is true then print the output data
    if verbose:
        print(std_out.strip(), std_err)
    pass

# downloading images one by one
count = 0
# looping through the flipkart links in the database
for weburl in dataFile["product_url"]:    
    # trying to download the image
    try:
        # establishing the conenction
        response = requests.get(weburl)
        # getting the html content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # extracting image url
        try:
            image = soup.find_all("img", class_="_396cs4 _2amPTt _3qGmMb")[0]
        except:
            image = soup.find_all("img", class_="_2r_T1I _396QI4")[0]
        link = image.get("src").split("?q")[0]

        # printing the link
        print(link)
        
        # firing the wget command and downloading the image
        runcmd(f"wget --directory-prefix=flipkart_com-ecommerce_sample_images {link}")
        
        # renaming the file
        imageName = link.split("/")[-1]
        old_name = f"flipkart_com-ecommerce_sample_images/{imageName}"
        new_name = f"flipkart_com-ecommerce_sample_images/{count}.jpeg"
        os.rename(old_name, new_name)

    except:
        print("Failed")
    count += 1
