CREATE  OR ALTER   PROCEDURE  mydata.spCopyMyDataToLocalDB  
    /*
    This procedure just copies tables from MatrixCare MyData DB to a local DB.
    The MyData DB is connected via a linked DB: [MYDATAHOST5].[BIDW_50582_HebrewHome]...
    Note that this link is hard coded for speed; if you need to change either the 
    
    source or target database. edit this procedure with a global search and replace.
    
    All the tables correspond EXACTLY to the MyData tables with the following exceptions:
		A "WHERE isDeleted=0" is added to avoid copying deleted records.  The purpose is
		not speed but to avoid having to repeat the "isDeleted" test in all subsequent
		queries.
		
		A new Table that does not exist in Myata has been created to simplify subsequent logic.
		The table "mydata.FacilityUnitRoomBed"  represents a join of the related tables and
		uses the BedID as Primary Key although both RoomID and UnitID are available as well.
		
	The entire copy process takes about 20 seconds.
    ******************************************************************************/
  
AS  
 
BEGIN 



DELETE mydata.Census_LevelOfCare;
INSERT INTO mydata.Census_LevelOfCare
SELECT *
FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].[STVSNF].Census_LevelOfCare
WHERE DeletedFlag=0;
------------------------------------------------------------------------------------------
DELETE mydata.Patient
INSERT INTO mydata.Patient
SELECT *
FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].[STVSNF].Patient
WHERE DeletedFlag=0;
---------------------------------------------------------------------------

DELETE                       mydata.Census_AdmitDischargeLocation; 
INSERT INTO						   mydata.Census_AdmitDischargeLocation
SELECT *
FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.Census_AdmitDischargeLocation
WHERE DeletedFlag=0;

    
-- -----------------------------------------------------------------------------------------
DELETE                       mydata.Census_LOA; 
INSERT	INTO					   mydata.Census_LOA
SELECT *
FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.Census_LOA
WHERE DeletedFlag=0;
-----------------------------------------------------------------------------

DELETE           mydata.PatientCensus; 
INSERT INTO					   mydata.PatientCensus
SELECT *
FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.PatientCensus
WHERE DeletedFlag=0;
-----------------------------------------------------------------------------------


-- ------------------------------------------------------------------------------------
DELETE                       			   mydata.PatientStayElement; 
INSERT INTO 							   mydata.PatientStayElement
SELECT * FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.PatientStayElement
WHERE DeletedFlag=0;
-- ---------------------------------------------------------------------------------------------- 
DELETE                       			   mydata.FacilityBed; 
INSERT INTO 							   mydata.FacilityBed
SELECT * FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.FacilityBed
WHERE DeletedFlag=0;

-- ----------------------------------------------------------------------------------------------- 
DELETE                       			   mydata.FacilityRoom; 
INSERT INTO 							   mydata.FacilityRoom
SELECT * FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.FacilityRoom
WHERE DeletedFlag=0;
-- -----------------------------------------------------------------------------------------------
DELETE                       			   mydata.PatientGroup; 
INSERT INTO 							   mydata.PatientGroup
SELECT * FROM [MYDATAHOST5.MATRIXCARECLOUD.COM,41434].[BIDW_50582_HebrewHome].STVSNF.PatientGroup
WHERE DeletedFlag=0;
-- -----------------------------------------------------------------------------------------------
DELETE  mydata.FacilityUnitRoomBed; 
INSERT  INTO mydata.FacilityUnitRoomBed
SELECT 
       facbed.BedID
     , facbed.RoomID
     , facroom.PatientGroupID AS UnitID
	 , patgrp.FacilityID
	 , patgrp.BuildingID
     , patgrp.Description AS UnitName
     , facroom.RoomName 
     , facbed.BedName 
  FROM mydata.[FacilityBed] AS facbed
  JOIN mydata.FacilityRoom AS facroom ON  facroom.RoomID=facbed.RoomID 
  JOIN mydata.PatientGroup AS patgrp ON patgrp.PatientGroupID=facroom.PatientGroupID 

-------------------------------------------------------------------------------------------------
 END ;
 
 GO
/* testing
Use CensusApps
EXEC mydata.spCopyMyDataToLocalDB;
*/