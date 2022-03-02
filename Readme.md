
Streamlit_application
├── app.py
├── Feature selection.ipynb.ipynb
├── Dockerfile
├── Credit Risk Analysi ML bootcamp.csv
├── model.pkl
├── Readme.md
├── requirments.txt
└── rf_model.pkl


app.py --> contain all the code of the streamlit application
Feature selection.ipynb --> contain the eda and model training code 
Credit risk analysis ml bootcamp.csv --> dataset 
preprocess.py --> contain helper function 
requirements.txt --> all the necessary packages used to build the application
rf_model --> trained random forest model pickle file 


-----------------------------------------------------------------------
To run the application type the following command 

On Linux :

	Step1: Create a virtual environment 
		python3 -m venv dir_name 
	
	Step2: Activate the virtual environment
		source bin/activate
	
	Step3: Install the required dependencies and packages from the requirments.txt
		pip3 install -r requirments.txt
	
	Step4: Run the application
		python3 app.py


On Windows :
	
	Step1 : Create a virtual environment 
			 python -m venv dir_name
	
	Step2 : Activate the virtual environment
			 Scripts\activate 
	
	Step3 : Install the required dependencies and packages from the requirment.txt file
			 pip install -r requirments.txt
	
	Step4 : Now run the application by typing the command 
			streamlit run app.py 

			By default will run on port no 8501 , but we can change it by typing
			streamlit run app.py --server.port 9000
	

To make the application a docker container:
	First make sure docker is installed on your system

	Step1 : Build the images from the dockerfile 
	
		docker build --tag image_name:tag .

	Step3 : See the images we just built 
		
		docker images
	
	Step3 : Create a docker container from the docker image just created (our application is configured to be run on port 8000) 
		
		docker run --name container_name -p 9000:9000 images_name:tag
	
	Step4 : You can see the conatiner running 
		
		docker ps -a
	
	Step5 : To stop a running container 
		
		docker stop conatiner_id 
		
	Step6 : To start a stopped a container 
		
		docker start container_id
	
	
		
