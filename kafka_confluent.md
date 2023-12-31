## ksqlDB
#### Create stream
This stream will be used to store the raw data from the MARTA API.
```SQL
CREATE STREAM marta_stream (
    TRAIN_ID VARCHAR,
    DESTINATION VARCHAR,
    DIRECTION VARCHAR,
    EVENT_TIME TIMESTAMP,
    HEAD_SIGN VARCHAR,
    LINE VARCHAR,
    NEXT_ARR TIMESTAMP,
    STATION VARCHAR,
    WAITING_SECONDS INTEGER,
    WAITING_TIME VARCHAR,
    RESPONSETIMESTAMP TIMESTAMP,
    VEHICLELONGITUDE DOUBLE,
    VEHICLELATITUDE DOUBLE,
    DELAY VARCHAR,
    TRIP_ID VARCHAR
) WITH (
    KAFKA_TOPIC='marta',
    KEY_FORMAT='KAFKA',
    VALUE_FORMAT='JSON'
);
```

#### Create table
This table will be used to store the latest data for each train at each station.
```SQL
CREATE TABLE marta_table WITH ( KEY_FORMAT = 'JSON' ) AS
SELECT 
    TRAIN_ID,
    STATION,
    LATEST_BY_OFFSET(DESTINATION) AS DESTINATION,
    LATEST_BY_OFFSET(DIRECTION) AS DIRECTION,
    LATEST_BY_OFFSET(EVENT_TIME) AS EVENT_TIME,
    LATEST_BY_OFFSET(HEAD_SIGN) AS HEAD_SIGN,
    LATEST_BY_OFFSET(LINE) AS LINE,
    LATEST_BY_OFFSET(NEXT_ARR) AS NEXT_ARR,
    LATEST_BY_OFFSET(WAITING_SECONDS) AS WAITING_SECONDS,
    LATEST_BY_OFFSET(WAITING_TIME) AS WAITING_TIME,
    LATEST_BY_OFFSET(VEHICLELONGITUDE) AS VEHICLELONGITUDE,
    LATEST_BY_OFFSET(VEHICLELATITUDE) AS VEHICLELATITUDE,
    LATEST_BY_OFFSET(DELAY) AS DELAY
FROM MARTA_STREAM
GROUP BY TRAIN_ID, STATION;
```