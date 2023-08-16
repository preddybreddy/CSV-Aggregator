# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 
CSV_Aggregator takes input .csv or .xslx files and consolodiates them into a single excel document. Data from all distinct input files is grouped by CONTROL_PROBE_TEMP.
The goal of the project is to give an overview of data points across various sources by calculating the min, max, mean of consolodated data for each CONTROL_PROBE_TEMP.


# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1. Requirements - 
* WSL version 2
* Docker Desktop

2. Installation process
1) Start Docker Desktop on your Windows machine
2) Open the Windows Command Prompt
3) To build the docker image run the following Command 
    * ```docker build -t <image_name:image_tag> https://farrarscientific@dev.azure.com/farrarscientific/Software/_git/CSV_Aggregator```
4) To verify the successfull installtion of the image, run ```docker images``` and verify the image is present
5) To run the image
    * ```docker run -d -p <client_port>:5000 <image_name:image_tag>```

2.	Software dependencies
1) Refer to requirements.txt

# Using the app
1. Go to the port specified in <client_port>, from a browser which should give be running a UI like this - 

![Home Page](home_page.png "home page")

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)