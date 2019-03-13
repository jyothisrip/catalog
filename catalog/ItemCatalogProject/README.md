### It is an item catalog project about furnitures 

# By Jyothi Sri

This web application is a project for the Udacity [Full Stack Nano Degree Course](https://www.udacity.com/course/full-stack
-web-developer-nanodegree--nd004).

### Initial steps to be taken

	*First we have to decide about which item we are going to develop a project
	*Next we have to gather information about our item project
	*And we must specify view of the item catalog 
	*The information like gathering furniture company names
		and furnitures in that company.
	*The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of
     the application.

		
### Needs for developing a furniture project 
	
	*Vagrant and Virtual box we need to install
	*And we also need flask module
	*And finally README file for describing about our project in brief to understand our project
	
	
### Required Skills for developing an item catalog
	
	1)Python

	2)HTML

	3)CSS

	4)OAuth

	5)Flask Framework

	6)DataBaseModels
		
### Commands for running project 
	
	*We have to open our project folder
	*Open command prompt in your project folder
	*We should create vagrant file using command `vagrant init ubuntu/xenial64`
	
	*To connect virtual machine by using command `vagrant up`
	
	*To login virtual machine by using command 	`vagrnat ssh`
	
	*Exit directories by using command `cd ..` and again exit `cd ..`
	
	*To move vagrant path by using command `cd /vagrant`
	
	*List out files by using command `ls`
	
	*Create virtual environment by using `sudo apt-get install python-virtualenv`.It allows you to 
	 manage separate package installations for different projects. It essentially allows you to 
	 create a “virtual” isolated Python installation and install packages into that virtual installation.
	 
	*Then we should move to virtual environment
		`. venv\scripts\activate`
		
	*We need to install some module like Flask by using command `pip install flask` and it is used 
	 in some light weight stuff like APIs for example.
	 
    *Install sqlalchemy by using command `pip install sqlalchemy`.SQLAlchemy is a library that 
	 facilitates the communication between Python programs and databases.
	 
	*Install requests by using `pip install requests` command for accessing the incoming data in flask.
	
	*Install psycopg2 by using `pip install psycopg2`.It is designed for multi-threaded applications
   	 and manages its own connection pool. Other interesting features of the adapter are that if you 
	 are using the PostgreSQL array data type, Psycopg will automatically convert a result using 
	 that data type to a Python list.
	 
	*Install oauth2client by running command `pip install oauth2client`.oauth2client makes it easy to interact with 
	 OAuth2-protected resources, especially those related to Google APIs.
	 
    *For creating database we should run `python FurnitureData_Setup.py` file, after running we get 
	 a message "Successfully created furniture database"
	 
	*Run `python furdatabase_init.py` file for inserting furniture details in database named 
	 `furniture.db` and it prints :
									>>Successfully created furniture database
									>>Successfully Added First Furniture User
									>>Your furniture details has been inserted in your database!
									
	*Run `python furniture.py` and access the application using `localhost:8000` 
	
	
### For logging to our project

	a. We need to create API key for that we have to open [https://console.developers.google.com]
	
	b. We have to select Credentials and select API key to create API key 
	
	c. After that select OAuth consent screen and fill details required
	
	d. Click Create credentials and select OAuth client ID and select Application type as Web application
	 and give https://localhost:8000 in Authorized JavaScript origins
	 
	e. Authorized redirect URIs for loging and connecting to our gmail account = https://localhost:8000/login and https://localhost:8000/gconnect 
	
	f. Download the OAuth 2.0 client IDs which is named as client_secret_1008368134895-6ki5png57441msndkss9sr31q227eikf.apps.googleusercontent.com.json
	
	g. We have to copy the data in that file and paste in client_secrets.json
	
	h. And copy client_id and replace it in `login.html` and `mainpage.html`
	
	i. Run the application using `python furniture.py`
	
	
### Results of JSON

	Furniture Catalog JSON: `localhost:8000/FurnitureStore/JSON`
		- Displays the whole furnitures along with categories and it's models. 

	Furniture Categories JSON: `localhost:8000/furnitureStore/furnitureCategories/JSON`
		- Displays all Furniture categories
	
    Furniture Editions: `localhost:8000/furnitureStore/editions/JSON`
		- Displays all Furniture Models

	Furniture Edition JSON: `localhost:8000/furnitureStore/<path:furniture_name>/editions/JSON`
		- Displays Furniture models for a specific Furniture category

	Furniture Category Edition JSON: `localhost:8000/furnitureStore/<path:furniture_name>/<path:edition_name>/JSON`
		- Displays a specific Furniture category Model.
