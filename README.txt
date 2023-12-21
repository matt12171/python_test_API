Very basic example for running FastAPI with MongoDB

To run on local machine 

    - pip install -r requirements.txt
    This will install several python packages listed in that file

    - Create a file called sensitive.py 
    This is where we will put the MongoDB connection string

    - In sensitive.py create the variable shown below
    mongo_connection_string = "PUT THE MONGODB CONNECTION STRING HERE"

    - uvicorn app:app --reload
    This starts the local server and you can now check everything is working


So far I have only added error handling for get users/{id}. This example could be recreated for all of them. 

