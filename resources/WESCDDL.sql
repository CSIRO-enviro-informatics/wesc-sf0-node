CREATE TABLE CombinedMeterReadings ( 
	"aggregationEndDateTime" timestamp,
	"aggregationID" Text,
	"aggregationStartDateTime" timestamp,
	"commodityType" Text,
	"geometryID" Text,
	"numberOfMeters" Integer,
	"numberOfReadings" Integer,
	"propertyType" Text,
	"propertyTypeURI" Text,
	"resultAverage" Real,
	"resultMedian" Real,
	"resultProcedure" Text,
	"resultTotal" numeric,
	"timeName" Text,
	"unitsLabel" Text,
	"unitsURI" Text,
	"utilityID" Text,
	"utilityName" Text,
	"combinedMeterReadingsPoints" Text,
	"combinedMeterReadingsID" Integer NOT NULL
)
;
CREATE TABLE ElectricityMeterReading ( 
	"readingType" Text,
	"electricityMeterReadingID" Integer NOT NULL
);

CREATE TABLE ElectricitySupply ( 
	"supplyID" Text,
	"electricitySupplyID" Integer NOT NULL
)
;

CREATE TABLE GasMeterReading ( 
	"gasMeterReadingID" Integer NOT NULL
)
;

CREATE TABLE MeterReading ( 
	"GNAF_ID" Integer,
	"lotSize" Real,
	"meterID" Text,
	"propertyID" Text,
	"propertyType" Text,
	"readingDate" Date,
	"resultID" Text,
	"resultMethod" Text,
	"resultUnitsOfMeasure" Text,
	"utilityID" Text,
	"utilityName" Text,
	"readingValue" Real,
	"latitude" Text,
	"longitude" Text,
	"meterReadingID" Integer NOT NULL
)
;

CREATE TABLE UtilitySupplyData ( 
	"supplyRegionPoints" Text,
	"endDeliveryTime" timestamp,
	"startDeliveryTime" timestamp,
	"supplyRegionName" Text,
	"supplyUnitsOfMeasureURI" Text,
	"supplyUnitsOfMeasureLabel" Text,
	"utilityID" Text,
	"utilityName" Text,
	"utilitySupplyDataID" Integer NOT NULL,
	"totalSupply" Real,
        "supplyRegionID" Text,
        "timeName" Text
)
;

CREATE TABLE WaterMeterReading ( 
	"waterMeterReadingID" Integer NOT NULL
)
;

CREATE TABLE WaterSupply ( 
	"consumerOutflows" Real,
	"environmentOutflows" Real,
	"outflowID" Text,
	"waterSupplyID" Integer NOT NULL
)
;


ALTER TABLE CombinedMeterReadings ADD CONSTRAINT PK_CombinedMeterReadings 
	PRIMARY KEY ("combinedMeterReadingsID")
;

ALTER TABLE ElectricityMeterReading ADD CONSTRAINT PK_ElectricityMeterReading 
	PRIMARY KEY ("electricityMeterReadingID")
;

ALTER TABLE ElectricitySupply ADD CONSTRAINT PK_ElectricitySupply 
	PRIMARY KEY ("electricitySupplyID")
;

ALTER TABLE GasMeterReading ADD CONSTRAINT PK_GasMeterReading 
	PRIMARY KEY ("gasMeterReadingID")
;

ALTER TABLE MeterReading ADD CONSTRAINT PK_MeterReading 
	PRIMARY KEY ("meterReadingID")
;

ALTER TABLE UtilitySupplyData ADD CONSTRAINT PK_UtilitySupplyData 
	PRIMARY KEY ("utilitySupplyDataID")
;

ALTER TABLE WaterMeterReading ADD CONSTRAINT PK_WaterMeterReading 
	PRIMARY KEY ("waterMeterReadingID")
;

ALTER TABLE WaterSupply ADD CONSTRAINT PK_WaterSupply 
	PRIMARY KEY ("waterSupplyID")
;

ALTER TABLE ElectricityMeterReading ADD CONSTRAINT FK_ElectricityMeterReading_MeterReading 
	FOREIGN KEY ("electricityMeterReadingID") REFERENCES MeterReading ("meterReadingID")
;

ALTER TABLE ElectricitySupply ADD CONSTRAINT FK_ElectricitySupply_UtilitySupplyData 
	FOREIGN KEY ("electricitySupplyID") REFERENCES UtilitySupplyData ("utilitySupplyDataID") ON DELETE CASCADE
;

ALTER TABLE GasMeterReading ADD CONSTRAINT FK_GasMeterReading_MeterReading 
	FOREIGN KEY ("gasMeterReadingID") REFERENCES MeterReading ("meterReadingID")
;

ALTER TABLE WaterMeterReading ADD CONSTRAINT FK_WaterMeterReading_MeterReading 
	FOREIGN KEY ("waterMeterReadingID") REFERENCES MeterReading ("meterReadingID")
;

ALTER TABLE WaterSupply ADD CONSTRAINT FK_WaterSupply_UtilitySupplyData 
	FOREIGN KEY ("waterSupplyID") REFERENCES UtilitySupplyData ("utilitySupplyDataID") ON DELETE CASCADE
;

SELECT AddGeometryColumn('meterreading', 'spatialGeometry', 4283, 'GEOMETRY', 2);
SELECT AddGeometryColumn('utilitysupplydata', 'utilitySupplyRegion', 4283, 'GEOMETRY', 2);
SELECT AddGeometryColumn('combinedmeterreadings', 'spatialRepresentation', 4283, 'GEOMETRY', 2);
