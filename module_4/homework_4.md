# Kayla Tinker HW #4 Answers

For this homework, you will need the following datasets:
* [Green Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)
* [Yellow Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)
* [For Hire Vehicle dataset (2019)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv)

:bulb: I used url2bucket.py to grab data and placed into GCP buckets. Then used sql from module 3 video 1 to add external
tables into BigQuery and recopied those over.

### Question 1: Understanding dbt model resolution

Provided you've got the following sources.yaml
```yaml
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema:   "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi
```

with the following env variables setup where `dbt` runs:
```shell
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
```

What does this .sql model compile to?
```sql
select * 
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}
```

- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.my_nyc_tripdata.ext_green_taxi`
- `select * from myproject.raw_nyc_tripdata.ext_green_taxi`
- `select * from myproject.my_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.green_taxi`

As In BigQuery, the terms project and database are interchangeable. So
your database name would be `dtc_zoomcamp_2025`, but the export takes priority, thus it
will be `myproject`. Which in our examples we work under the same project, so I am unsure why
we would want to change it, but according to the links below that is what export does. Then the model output, wouldn't
live where your raw data does, so that would be what you call `my_nyc_tripdata`.
And with the information given, the only table name is `ext_green_taxi`.
Ok, so we are setting our env_var using `export` here according to
https://stackoverflow.com/questions/72956095/dbt-environment-variables-and-running-dbt
https://docs.getdbt.com/docs/build/environment-variables

#### ANSWER 
**`select * from myproject.my_nyc_tripdata.ext_green_taxi`**


### Question 2: dbt Variables & Dynamic Models

Say you have to modify the following dbt_model (`fct_recent_taxi_trips.sql`) to enable Analytics Engineers to dynamically control the date range. 

- In development, you want to process only **the last 7 days of trips**
- In production, you need to process **the last 30 days** for analytics

```sql
select *
from {{ ref('fact_taxi_trips') }}
where pickup_datetime >= CURRENT_DATE - INTERVAL '30' DAY
```

What would you change to accomplish that in a such way that command line arguments takes precedence over ENV_VARs, which takes precedence over DEFAULT value?

- Add `ORDER BY pickup_datetime DESC` and `LIMIT {{ var("days_back", 30) }}`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", 30) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", "30") }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", var("days_back", "30")) }}' DAY`

To set variables we use `var`, and we can set a default if the variable isn't
provided, so that default here could be `30`. BUT we want the env_var
to take precedence over the Default value, thus we use env_var for it. 
From CLI, we need --var, thus we need to use var to 'override' the above options. This is 
somewhat shown in video 4.3.1 min 38, but env_var is not discussed and needs to be found in dtb
documentation - https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
and https://docs.getdbt.com/docs/build/environment-variables

#### ANSWER 
**Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY**


### Question 3: dbt Data Lineage and Execution

Considering the data lineage below **and** that 
taxi_zone_lookup is the **only** materialization build (from a .csv seed file):

Select the option that does **NOT** apply for 
materializing `fct_taxi_monthly_zone_revenue`:

- `dbt run`
- `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`
- `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`
- `dbt run --select +models/core/`
- `dbt run --select models/staging/+`

key work 'materialized'. So I am thinking it would be the /staging/+

#### ANSWER 
**`dbt run --select models/staging/+`*


### Question 4: dbt Macros and Jinja

Consider you're dealing with sensitive data (e.g.: [PII](https://en.wikipedia.org/wiki/Personal_data)), 
that is **only available to your team and very selected few individuals**, 
in the `raw layer` of your DWH (e.g: a specific BigQuery dataset or PostgreSQL schema), 

 - Among other things, you decide to obfuscate/masquerade that data through your staging models, 
and make it available in a different schema (a `staging layer`) for other Data/Analytics Engineers to explore

- And **optionally**, yet  another layer (`service layer`), where you'll build your 
dimension (`dim_`) and fact (`fct_`) tables (assuming the [Star Schema dimensional modeling](https://www.databricks.com/glossary/star-schema)) for Dashboarding and for Tech Product Owners/Managers

You decide to make a macro to wrap a logic around it:

```sql
{% macro resolve_schema_for(model_type) -%}

    {%- set target_env_var = 'DBT_BIGQUERY_TARGET_DATASET'  -%}
    {%- set stging_env_var = 'DBT_BIGQUERY_STAGING_DATASET' -%}

    {%- if model_type == 'core' -%} {{- env_var(target_env_var) -}}
    {%- else -%}                    {{- env_var(stging_env_var, env_var(target_env_var)) -}}
    {%- endif -%}

{%- endmacro %}
```

And use on your staging, dim_ and fact_ models as:
```sql
{{ config(
    schema=resolve_schema_for('core'), 
) }}
```

That all being said, regarding macro above, 
**select all statements that are true to the models using it**:

- Setting a value for  `DBT_BIGQUERY_TARGET_DATASET` env var is mandatory, or it'll fail to compile
- Setting a value for `DBT_BIGQUERY_STAGING_DATASET` env var is mandatory, or it'll fail to compile
- When using `core`, it materializes in the dataset defined in `DBT_BIGQUERY_TARGET_DATASET`
- When using `stg`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`
- When using `staging`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`

#### ANSWER 
**ALL except Setting a value for `DBT_BIGQUERY_STAGING_DATASET**


### Question 5: Taxi Quarterly Revenue Growth

1. Create a new model `fct_taxi_trips_quarterly_revenue.sql`
2. Compute the Quarterly Revenues for each year for based on `total_amount`
3. Compute the Quarterly YoY (Year-over-Year) revenue growth 
  * e.g.: In 2020/Q1, Green Taxi had -12.34% revenue growth compared to 2019/Q1
  * e.g.: In 2020/Q4, Yellow Taxi had +34.56% revenue growth compared to 2019/Q4

Considering the YoY Growth in 2020, which were the yearly quarters with the best (or less worse) 
and worst results for green, and yellow

- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q3, worst: 2020/Q4}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q3, worst: 2020/Q4}

#### ANSWER
 **green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}**





### Question 6: P97/P95/P90 Taxi Monthly Fare

1. Create a new model `fct_taxi_trips_monthly_fare_p95.sql`
2. Filter out invalid entries (`fare_amount > 0`, `trip_distance > 0`, and `payment_type_description in ('Cash', 'Credit Card')`)
3. Compute the **continuous percentile** of `fare_amount` partitioning 
by service_type, year and month

Now, what are the values of `p97`, `p95`, `p90` for Green Taxi and Yellow Taxi, in April 2020?

- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 25.5, p90: 19.0}

#### ANSWER 
**green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}**

```sql
-- in Cloud IDE DBT (AI support)
WITH clean_fact_trips AS (
    SELECT
        service_type,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(MONTH FROM pickup_datetime) AS month,
        fare_amount,
        trip_distance,
        payment_type_description
    FROM {{ ref('fact_trips') }}
    WHERE
        fare_amount > 0
        AND trip_distance > 0
        AND lower(payment_type_description) in ('cash', 'credit card')
),

fare_amt_perc AS(
    SELECT
        service_type,
        year,
        month,
        PERCENTILE_CONT(fare_amount, 0.97) OVER (PARTITION BY service_type, year, month) AS p97,
        PERCENTILE_CONT(fare_amount, 0.95) OVER (PARTITION BY service_type, year, month) AS p95,
        PERCENTILE_CONT(fare_amount, 0.90) OVER (PARTITION BY service_type, year, month) AS p90
    FROM clean_fact_trips
)

SELECT * FROM fare_amt_perc

-- In BigQuery
SELECT service_type, year, month, p97, p95, p90
FROM `taxi-rides-ny-448101.module_4_dbt_model.fact_taxi_trips_monthly_p95`
WHERE year = 2020 and month = 4
GROUP BY service_type, year, month, p97, p95, p90
```


### Question 7: Top #Nth longest P90 travel time Location for FHV

Prerequisites:
* Create a staging model for FHV Data (2019), and **DO NOT** add a deduplication step, 
just filter out the entries where `where dispatching_base_num is not null`
* Create a core model for FHV Data (`dim_fhv_trips.sql`) joining with `dim_zones`. 
Similar to what has been done [here](../../../04-analytics-engineering/taxi_rides_ny/models/core/fact_trips.sql)
* Add some new dimensions `year` (e.g.: 2019) and `month` (e.g.: 1, 2, ..., 12), 
based on `pickup_datetime`, to the core model to facilitate filtering for your queries

Now...
1. Create a new model `fct_fhv_monthly_zone_traveltime_p90.sql`
2. For each record in `dim_fhv_trips.sql`, compute 
the [timestamp_diff](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_diff) in seconds between dropoff_datetime and pickup_datetime - we'll call it `trip_duration` for this exercise
3. Compute the **continous** `p90` of `trip_duration` partitioning by 
year, month, pickup_location_id, and dropoff_location_id

For the Trips that **respectively** started from `Newark Airport`, `SoHo`, 
and `Yorkville East`, in November 2019, what are **dropoff_zones** with the 
2nd longest p90 trip_duration ?

- LaGuardia Airport, Chinatown, Garment District
- LaGuardia Airport, Park Slope, Clinton East
- LaGuardia Airport, Saint Albans, Howard Beach
- LaGuardia Airport, Rosedale, Bath Beach
- LaGuardia Airport, Yorkville East, Greenpoint

#### ANSWER 
**LaGuardia Airport, Chinatown, Garment District**

```sql
-- Staging Schema add
version: 2

sources:
  - name: staging
    database: "{{ env_var('DBT_DATABASE', 'taxi-rides-ny-448101') }}"
    schema: "{{ env_var('DBT_SCHEMA', 'module_4_dbt') }}"
      # loaded_at_field: record_loaded_at
      # Change DB to now 'module_4_dbt' from trips_data_all
    tables:
      - name: green_tripdata
      - name: fhv_tripdata
      # for homework p#7
      - name: yellow_tripdata
         # freshness:
           # error_after: {count: 6, period: hour}


models:
    - name: stg_fhv_tripdata
      description: >
        Trip made by fhv, also known as for-hire vehicles.
        The records were collected and provided to the NYC Taxi and Limousine Commission (TLC) by
        technology service providers.
      columns:
          - name: dispatching_base_num
            description: dispatching_base_num
          - name: pickup_datetime
            description: The date and time when the meter was engaged.
          - name: dropOff_datetime
            description: The date and time when the meter was disengaged.
          - name: Affiliated_base_numbe
            description: Affiliated_base_numbe
          - name: PUlocationID
            description: locationid where the meter was engaged.
            tests:
              - relationships:
                  to: ref('taxi_zone_lookup')
                  field: locationid
                  severity: warn
          - name: DOlocationID
            description: locationid where the meter was engaged.
            tests:
              - relationships:
                  to: ref('taxi_zone_lookup')
                  field: locationid
          - name: SR_Flag
            description: >
              This flag indicates ?
                Y =
                N =

-- Create stg_fhv_tripdata.sql
{{
    config(
        materialized='view'
    )
}}

with tripdata as
(
  select *,
  from {{ source('staging','fhv_tripdata') }}
  where dispatching_base_num is not null
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    {{ dbt.safe_cast("dispatching_base_num", api.Column.translate_type("integer")) }} as dispatchid,
    {{ dbt.safe_cast("Affiliated_base_number", api.Column.translate_type("integer")) }} as affilid,
    {{ dbt.safe_cast("PUlocationID", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }} as dropoff_locationid,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    SR_Flag,

from tripdata

-- Create dim_fhv_trips.sql in core
{{
    config(
        materialized='table'
    )
}}

-- join dim_zones and Add some new dimensions `year` (e.g.: 2019) and `month` (e.g.: 1, 2, ..., 12),
-- based on `pickup_datetime`

with fhv_tripdata as (
    select *
    from {{ ref('stg_fhv_tripdata') }}
),
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select
    EXTRACT(YEAR FROM fhv_tripdata.pickup_datetime) AS year,
    EXTRACT(MONTH FROM fhv_tripdata.pickup_datetime) AS month,
    fhv_tripdata.pickup_datetime,
    fhv_tripdata.dropoff_datetime,
    fhv_tripdata.tripid,
    fhv_tripdata.dispatchid,
    fhv_tripdata.affilid,
    fhv_tripdata.pickup_locationid,
    fhv_tripdata.dropoff_locationid,
    fhv_tripdata.SR_Flag,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone
from fhv_tripdata
inner join dim_zones as pickup_zone
on fhv_tripdata.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_tripdata.dropoff_locationid = dropoff_zone.locationid


-- Create fct_fhv_monthly_zone_traveltime_p90.sql
WITH trip_dur_perc AS (
    SELECT
        pickup_zone,
        dropoff_zone,
        year,
        month,
        PERCENTILE_CONT(TIMESTAMP_DIFF(pickup_datetime, dropoff_datetime, SECOND), 0.90) OVER (PARTITION BY year, month, pickup_locationid, dropoff_locationid) AS p90
    FROM {{ ref('dim_fhv_trips') }}
)

-- Compute the **continous** `p90` of `trip_duration` partitioning by
-- year, month, pickup_location_id, and dropoff_location_id

SELECT * FROM trip_dur_perc

-- Query
SELECT *
FROM `taxi-rides-ny-448101.module_4_dbt_model.fct_fhv_monthly_zone_traveltime_p90`
WHERE pickup_zone IN ('SoHo') AND year = 2019 and month = 11
ORDER BY p90 DESC
LIMIT 100;
```
