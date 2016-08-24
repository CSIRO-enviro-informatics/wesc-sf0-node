UPDATE meterreading
SET "spatialGeometry" = CASE WHEN longitude = '' THEN ST_GeomFromText(NULL,4283)
	ELSE ST_GeomFromText('POINT(' || longitude || ' ' || latitude || ')',4283) END;

UPDATE utilitysupplydata  
SET "utilitySupplyRegion" = ST_GeomFromText('POINT(' || "supplyRegionPoints" || ')',4283);

UPDATE combinedmeterreadings 
SET "spatialRepresentation" = ST_GeomFromText('POLYGON((' || "combinedMeterReadingsPoints" || '))',4283);
