# Introduction 
CSV_Aggregator takes input .csv and/or .xslx files and consolodiates them into a single excel document. Data from all distinct input files is grouped by CONTROL_PROBE_TEMP
The goal of the project is to give an overview of data points across various sources by calculating the min,max and mean of consolidated data for each CONTROL_PROBE_TEMP


# Getting Started
1. Requirements - 
* WSL version 2
* Docker Desktop

2. Installation process
1) Docker Instructions
    1) Start Docker Desktop
    2) Open the terminal
    3) To build the docker image run the following command 
        * ```docker build -t <image_name:image_tag> https://farrarscientific@dev.azure.com/farrarscientific/Software/_git/CSV_Aggregator```
    4) To verify the successfull installation of the image, run ```docker images``` and verify the image is present
    5) To run the image
        * ```docker run -d -p <client_port>:5000 <image_name:image_tag>```

2) Local Instructions
    1) Clone the git repository
    2) Open Anaconda Prompt
        - Recreate environment ```conda create --name <name> --file spec-list.txt```
    3) Activate the conda environment
        - ```conda activate <name>```
    4) ```cd``` into the folder where you cloned the repo
    5) Create python venv
        - ```py -m venv env```
    6) Activate the venv
        - ```.\env\Scripts\activate```
    7) Install dependencies
        - ```pip install -r requirements.txt```
    8) Start the server
        - ```py app.py```
2. Software dependencies
1) Refer to requirements.txt

# Using the app
1. Go to the port specified in <client_port>, from a browser which should give be running a UI like this - 

![Home Page](home_page.png "home page")

2. The app does not support window switching when uploading files. To get around this - 
    1. Store all the files to be uploaded in a folder beforehand 
    2. Once "Choose Files" is clicked, navigate to the folder created beforehand and select all the input files

3. Afer you hit "Submit" then an Excel file by the name of ```Aggregated Data``` should be downloaded onto the disk in the location indicated by the browser

# Contribute
1. Add functionality to add files after choosing input for the first time
    - At present, once files are uploaded, additional files cannot be uploaded without clearing out the existing files

2. Show the file names of the uploaded files to the user

3. Allow for user to pick the download location as well as the name of the downloaded file