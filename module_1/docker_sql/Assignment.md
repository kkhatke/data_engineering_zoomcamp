# Question 1
docker run -it --entrypoint=bash python:3.12.8
pip -V
pip version - 24.3.1


# Question 2
db:5432

hostname of database is db and hostname of container is 5432


# Question 3
| up_to_1_mile | between_1_and_3_miles | between_3_and_7_miles | between_7_and_10_miles | over_10_miles |
|--------------|-----------------------|-----------------------|------------------------|---------------|
| 104830       | 198995                | 109642                | 27686                  | 35201         |

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

# Question 4
| pickup_day  | max_distance |
|-------------|--------------|
| 2019-10-31  | 515.89       |

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

# Question 5
| pickup_day  | pickup_location | pickup_zone       | total_amt             |
|-------------|-----------------|-------------------|-----------------------|
| 2019-10-18  | 74              | East Harlem North | 18686.67999999973     |
| 2019-10-18  | 75              | East Harlem South | 16797.259999999787    |


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

# Question 6
| pickup_day  | pickup_zone      | dropoff_zone | tip  |
|-------------|------------------|--------------|------|
| 2019-10-25  | East Harlem North | JFK Airport  | 87.3 |


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

# Question 7
terraform init, terraform apply -auto-approve, terraform destroy

**Downloading the provider plugins and setting up backend** - This is handled by the `terraform init` command, which initializes a Terraform working directory, sets up the backend, and downloads necessary provider plugins.

**Generating proposed changes and auto-executing the plan** - This is done with the `terraform apply -auto-approve` command, which applies the changes as per the Terraform configuration files without requiring interactive approval.

**Remove all resources managed by Terraform** - The `terraform destroy` command is used to remove all resources managed by Terraform according to the configuration files.