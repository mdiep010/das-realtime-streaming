# das_s26_cloud_computing

DAS Spring 2026 project

https://das-realtime-streaming-zu7rpfljea-uc.a.run.app/

Set up:
- Download Docker Desktop
- Fork/clone repository
- Create .env file from example

To build environment:
- Make sure docker desktop application is running
- ```docker-compose up --build```

To start up / shut down containers:
- ```docker-compose up -d```
- ```docker-compose down -v```

To Run the pipeline:
- open another terminal
- ```cd ingestion```
- ```python main.py```
- open another terminal
-  ```cd processing```
-  ```python main.py```

To verify things are running properly:
- ```docker ps``` - check container status
- ```docker-compose exec postgres psql -U username -d project_db``` - start a psql session
    - ```\dt``` - check what tables exist
    - ```\d {table_name}``` - view schema for specific table
    - ```SELECT * FROM predictions;``` view data
    - ```SELECT COUNT(*) FROM predictions;``` count rows
- Go to ```http://localhost:8501``` to view dashboard
- Go to ```http://localhost:8080``` to view broker interface
