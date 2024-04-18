CREATE TABLE CropData (
    State VARCHAR,
    District VARCHAR,
    Crop VARCHAR,
    Year VARCHAR,
    Season VARCHAR(50),
    Area FLOAT,
    Area_Units VARCHAR(50),
    Production FLOAT,
    Production_Units VARCHAR(50),
    Yield FLOAT
);

SELECT * FROM CropData limit 10;

DROP TABLE CropData;


