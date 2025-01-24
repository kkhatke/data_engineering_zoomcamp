services:
    postgres:
        image: postgres:13
        environment:
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=postgres
            - POSTGRES_DB=postgres
        volumes:
            - postgres-db-volume:/var/lib/postgresql/data (local:container)
        ports:
            - 5432:5432 (Host:Container)    
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U postgres"]
            interval: 5s
            retries: 5
        restart: always

# Running Postgres Container through Docker CLI

```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi \
    -v D:/data_engineering_zoomcamp/module_1/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

# pgcli connect to Postgres database

`pgcli -h localhost -p 5432 -U postgres -d postgres -c 'SELECT * FROM green_taxi_data LIMIT 10;'`

-h localhost
-p port default 5432
-U username
-d database
-c command

# Run jupyter notebook

`python -m notebook`

# Dataset 
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz


# PGAdmin Docker 

`docker run -it -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=root -p 5050:80 dpage/pgadmin4`

-p 5050:80 = port mapping host:container

Unable to connect to server: because container of postgres is on another container
So we need network mode bridge

# Docker Network

`docker network ls` - list all the networks
`docker network create pg-network` - create a network
`docker network rm pg-network` - remove a network

`docker run -it -d -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -p 5432:5432  --network pg-network --name pg-database -v D:/data_engineering_zoomcamp/module_1/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data postgres:13`

Be insure that the network is created before running the container and check the data is available in the network

`docker run -it -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=root -p 5050:80 --network pg-network --name pg-admin dpage/pgadmin4`

Then in the browser, go to http://localhost:5050 and login with admin@admin.com and root, 

-create a new server and connect to the database and check the data.
-for creeating the server, click on 'Servers' then 'Add' 
then Name = should be any name 
then in 'Connection' => 'Host' = name of the postgres container, 
'Port' = 5432, 
'Database' = postgres, 
'Username' = root, 
'Password' = root

# Data Ingest pipeline 

--Run through script and passing parameters

Run through CMD prompt
`python ingest_data.py --user root --password root --host localhost --port 5432 --db ny_taxi --table_name green_taxi_data --url https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet` 

--Through Docker CLI

`docker build -t ingest_data:1.0 .` -- build the image
`docker run -it ingest_data:1.0 --user root --password root --host localhost --port 5432 --db ny_taxi --table_name green_taxi_data --url https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet` -- run the container

--run in network mode

`docker run -it --network pg-network ingest_data:1.0 --user root --password root --host localhost --port 5432 --db ny_taxi --table_name green_taxi_data --url https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet` -- Pass the network name

# Python Function for see and download the data from localhost

`python -m http.server 8000`
it will open the browser and show the data in the browser at localhost:8000 
