# Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice
Docker and SQL

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework. 

When your solution has SQL or shell commands and not code
(e.g. python files) file format, include them directly in
the README file of your repository.


## Question 1. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1

#### Solution :
<details open>
<summary> Expand</summary>

- First run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

- Then run `pip -V` in the container to check the version of `pip`.

```cmd
docker run -it --entrypoint=bash python:3.12.8
pip -V
```
```Output
pip version - 24.3.1
```
</details>


## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

If there are more than one answers, select only one of them

#### Solution :
<details open>
<summary> Expand</summary>

In given Docker Compose, services communicate with each other using the service names defined in the docker-compose.yaml file as hostnames, and the internal ports as defined in the service's Docker image. The ports published to the host are not used for inter-service communication within the Docker network created by Docker Compose.

The PostgreSQL database service is named `db`. The internal port for PostgreSQL, which is `5432`, is used within the Docker network. Although you have mapped 5433 on the host to 5432 in the container, this mapping is relevant only for accessing the service from outside the Docker network, not from services within the same Docker network, like pgadmin.

Therefore, the correct hostname and port that pgadmin should use to connect to the PostgreSQL database is:

- Hostname: `db`  Port: `5432`

```
db:5432
```
</details>

##  Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from October 2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether
you want to use Jupyter or a python script.

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles 

Answers:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202

#### Solution :
<details open>
<summary> Expand</summary>

- Query

```SQL
SELECT
  SUM(
  	CASE 
	  WHEN trip_distance <= 1 THEN 1 
	  ELSE 0 
	END) AS up_to_1_mile,
  SUM(
  	CASE 
	  WHEN trip_distance > 1 
	  	AND trip_distance <= 3 THEN 1 
	  ELSE 0 
	END) AS between_1_and_3_miles,
  SUM(
  	CASE 
	  WHEN trip_distance > 3 
	  	AND trip_distance <= 7 THEN 1 
	  ELSE 0 
	END) AS between_3_and_7_miles,
  SUM(
  	CASE 
	  WHEN trip_distance > 7 
	  	AND trip_distance <= 10 THEN 1 
	  ELSE 0 
	END) AS between_7_and_10_miles,
  SUM(
  	CASE 
	  WHEN trip_distance > 10 THEN 1 
	  ELSE 0 
	END) AS over_10_miles
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2019-10-01' 
AND lpep_pickup_datetime < '2019-11-01';
```
- Output

| up_to_1_mile | between_1_and_3_miles | between_3_and_7_miles | between_7_and_10_miles | over_10_miles |
|--------------|-----------------------|-----------------------|------------------------|---------------|
| 104830       | 198995                | 109642                | 27686                  | 35201         |

</details>

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31

#### Solution :
<details open>
<summary> Expand</summary>

- Query

```SQL
WITH daily_maximum_distance AS (
	    SELECT
	        DATE(lpep_pickup_datetime) AS pickup_day,
	        MAX(trip_distance) AS max_distance
	    FROM green_taxi_data
	    GROUP BY DATE(lpep_pickup_datetime)
	)

SELECT 
    pickup_day,
    max_distance
FROM daily_maximum_distance
ORDER BY max_distance DESC
LIMIT 1;
```
- Output

| pickup_day  | max_distance |
|-------------|--------------|
| 2019-10-31  | 515.89       |

</details>

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

#### Solution :
<details open>
<summary> Expand</summary>

- Query

```SQL
SELECT
	DATE(td.lpep_pickup_datetime) AS pickup_day,
	td."PULocationID" AS pickup_location,
	CONCAT(zn."Borough",'-',zn."Zone") AS pickup_zone,
	SUM(td.total_amount) AS total_amt
FROM green_taxi_data td
	LEFT JOIN zones zn
		ON td."PULocationID" = zn."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
GROUP BY pickup_day, pickup_location, pickup_zone
ORDER BY total_amt DESC
LIMIT 2;
```
- Output

| pickup_day  | pickup_location | pickup_zone       | total_amt             |
|-------------|-----------------|-------------------|-----------------------|
| 2019-10-18  | 74              | East Harlem North | 18686.67999999973     |
| 2019-10-18  | 75              | East Harlem South | 16797.259999999787    |

</details>

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone
named "East Harlem North" which was the drop off zone that had
the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

#### Solution :
<details open>
<summary> Expand</summary>

- Query

```SQL
WITH pickup_trip AS (
		SELECT 
			DATE(td.lpep_pickup_datetime) AS pickup_day,
			td."PULocationID" AS pickup_id,
			td."DOLocationID" AS dropoff_id,
			zn."Zone" AS pickup_zone,
			td.tip_amount AS tip
		FROM green_taxi_data td
			LEFT JOIN zones zn
				ON td."PULocationID" = zn."LocationID"
		WHERE DATE(td.lpep_pickup_datetime) >= '2019-10-01'
		AND DATE(td.lpep_pickup_datetime) <= '2019-10-31'
		),
	dropoff_trip AS (
		SELECT
			pt.pickup_day,
			pt.pickup_zone,
			pt.tip,
			zn."Zone" AS dropoff_zone
		FROM pickup_trip pt
			LEFT JOIN zones zn
				ON pt.dropoff_id = zn."LocationID"
	)
SELECT 
	pickup_day,
	pickup_zone,
	dropoff_zone,
	tip 
FROM dropoff_trip
WHERE pickup_zone = 'East Harlem North'
ORDER BY tip DESC
LIMIT 1;
```
- Output

| pickup_day  | pickup_zone      | dropoff_zone | tip  |
|-------------|------------------|--------------|------|
| 2019-10-25  | East Harlem North | JFK Airport  | 87.3 |

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](../../../01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

#### Solution :
<details open>
<summary> Expand</summary>

**Downloading the provider plugins and setting up backend** - This is handled by the `terraform init` command, which initializes a Terraform working directory, sets up the backend, and downloads necessary provider plugins.

**Generating proposed changes and auto-executing the plan** - This is done with the `terraform apply -auto-approve` command, which applies the changes as per the Terraform configuration files without requiring interactive approval.

**Remove all resources managed by Terraform** - The `terraform destroy` command is used to remove all resources managed by Terraform according to the configuration files.

```
terraform init, terraform apply -auto-approve, terraform destroy
```
</details>

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1
