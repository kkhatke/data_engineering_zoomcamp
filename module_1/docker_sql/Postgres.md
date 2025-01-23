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

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi \
    -v D:/data_engineering_zoomcamp/module_1/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13 

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

