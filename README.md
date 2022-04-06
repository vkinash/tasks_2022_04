<h2>Requirements:</h2>

1. python3.8 
2. docker (https://docs.docker.com/engine/install/)
3. docker compose (https://docs.docker.com/compose/install/)

<h2>Task 1</h2>

How to run the solution of Task 1 (task_1.py):

1. Create virtual environment.
2. Install requirements. In directory ```/tasks``` run ```pip install -r requirements.txt```
3. Run docker-compose. In directory ```/tasks``` run ```docker-compose up -d```
4. Run the application. in ```tasks/task_1``` directory run ```python3 task_1.py```

After the run will be created two files in directory ```task/output```. 
 ```file_a.csv``` contains generated 1024 rows and 8 columns with generated random data according point "A" of the test task.
 ```file_b.csv``` contains data from ```file_a.csv``` filtrated according point "B" of the test.

Data in MySQL can be seen in ```mysql_container``` in ```db.t_upload_data``` table.
```commandline
SELECT * FROM db.t_upload_data;
```
Data in MongoDB can be seen in ```mongo_container```  in ```mydb``` database, ```my_collection``` collection.
```commandline
use mydb
db.getCollection('my_collection').find()
```

<h2>Task 2</h2>

How to set up the application:
1. Create virtual environment.
2. Install requirements. In directory ```/tasks``` run ```pip install -r requirements.txt```
3. Run the application. In ```/tasks/scraping_task``` directory run ```scrapy crawl pc```

Scraped data will be written in  ```tasks/scraping_task/scraping_task/output```.
Example of scraped data could be found in GoogleDisk https://drive.google.com/drive/folders/1UkBkAh6xL4TC_ldsdOCJ601Xpi-gB7FZ?usp=sharing

