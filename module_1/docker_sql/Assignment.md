# Question 1
docker run -it --entrypoint=bash python:3.12.8
pip -V
pip version - 24.3.1


# Question 2
db:5432

hostname of database is db and hostname of container is 5432


# Question 3
104830	198995	109642	27686	35201

`SELECT
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
AND lpep_pickup_datetime < '2019-11-01';`

# Question 4
"2019-10-31"	515.89

`WITH daily_maximum_distance AS (
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
LIMIT 1;`