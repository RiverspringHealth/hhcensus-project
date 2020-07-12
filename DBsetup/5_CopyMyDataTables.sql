ALTER  PROCEDURE mydata.CopyMyDataToLocalDB
AS
SET ANSI_NULLS ON;
SET ANSI_PADDING OFF;
SET QUOTED_IDENTIFIER ON;


-- -----------------------------------------------------------------------------------------
TRUNCATE TABLE                     mydata.Census_AdmitDischargeLocation; 
INSERT INTO						   mydata.Census_AdmitDischargeLocation
SELECT [AdmDisLocationID]
      ,[OwningCorpID]
      ,[AdmitDischargeLocationCategoryID]
      ,[isCorporateActive]
      ,[LocationName]
      ,[Description]
      ,[isAdmitLocation]
      ,[isDischargeLocation]
      ,[HospitalReadmissionTypeCode]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.Census_AdmitDischargeLocation
WHERE DeletedFlag=0;

------------------------------------------------------------------------------------------------

TRUNCATE TABLE  mydata.Census_LevelOfCare;
INSERT INTO     mydata.Census_LevelOfCare
SELECT [LOCID]
      ,[FacilityID]
      ,[Description]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].Census_LevelOfCare
WHERE DeletedFlag=0;
------------------------------------------------------------------------------------------
TRUNCATE TABLE                     mydata.Census_LOA; 
INSERT	INTO					   mydata.Census_LOA
SELECT [LOAID]
      ,[FacilityID]
      ,[LOACode]
      ,[Description]
      ,[Billable]
      ,[WriteOff]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.Census_LOA
WHERE DeletedFlag=0;
-----------------------------------------------------------------------------
TRUNCATE TABLE      mydata.Census_Types; 
INSERT INTO 		mydata.Census_Types
  SELECT [CensusType]
      ,[Description]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.Census_Types
WHERE DeletedFlag=0;

-----------------------------------------------------------------------------
TRUNCATE TABLE                        	mydata.FacilityBed; 
INSERT INTO 							mydata.FacilityBed
SELECT [BedID]
      ,[RoomID]
      ,[BedName] 
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.FacilityBed
WHERE DeletedFlag=0;

-- ----------------------------------------------------------------------------------------------- 

TRUNCATE TABLE                        	mydata.FacilityRoom; 
INSERT INTO 							mydata.FacilityRoom
SELECT [RoomID]
      ,[PatientGroupID]
      ,[RoomName] 
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.FacilityRoom
WHERE DeletedFlag=0;
-- -----------------------------------------------------------------------------------------------


TRUNCATE TABLE mydata.FacilityUnitRoomBed; 
INSERT  INTO   mydata.FacilityUnitRoomBed
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
---------------------------------------------------------------------------------------------



TRUNCATE TABLE  mydata.Patient
INSERT INTO mydata.Patient
SELECT [PatientID]
      ,[IsActive]
      ,[FirstName]
      ,[MiddleName]
      ,[LastName]
      ,[SSN]
      ,[AddressID]
      ,[DateOfBirth]
      ,[Sex]
      ,[AttendingPhysicianID]
      ,[RACECODE]
      ,[MARITALSTATUSCODE]
      ,[MedicareNumber]
      ,[MedicaidNumber]
      ,[MothersMaidenName]
      ,[PreferredName]
      ,[POA]
      ,[RELIGIONCODE]
      ,[MilitaryService]
      ,[PharmacyID]
      ,[ContactAddressID]
      ,[DNR]
      ,[MedicalRecordNumber]
      ,[RoomNumber]
      ,[OriginalAdmtDt]
      ,[CurrentAdmtDt]
      ,[CurrentReturnDt]
      ,[VisitCount]
      ,[CensusStatus]
      ,[MedicareBNumber]
      ,[CoveredByManagedCare]
      ,[LanguageKey]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].Patient
WHERE DeletedFlag=0;
---------------------------------------------------------------------------



    
-- -----------------------------------------------------------------------------------------


TRUNCATE TABLE            mydata.PatientCensus; 
INSERT INTO				  mydata.PatientCensus
SELECT [CensusID]
      ,[FacilityID]
      ,[PatientID]
      ,[DateTime]
      ,[CensusType]
      ,[Payer]
      ,[LOC]
      ,[AdmSrc]
      ,[AdmType]
      ,[PSC]
      ,[LOA]
      ,[BuildingID]
      ,[HallID]
      ,[RoomID]
      ,[BedID]
      ,[NewBenefit]
      ,[Note]
      ,[EndDate]
      ,[DischargeType]
      ,[PartADays]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientCensus
WHERE DeletedFlag=0;
-----------------------------------------------------------------------------------


TRUNCATE TABLE                        	   mydata.PatientGroup; 
INSERT INTO 							   mydata.PatientGroup
SELECT [PatientGroupID]
      ,[FacilityID]
      ,[Description]
      ,[BuildingID] 
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientGroup
WHERE DeletedFlag=0;
-- -----------------------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------------
TRUNCATE TABLE                        	mydata.PatientStayElement; 
INSERT INTO 							mydata.PatientStayElement
SELECT [FacilityID]
      ,[PatientID]
      ,[StartDate]
      ,[EndDate]
      ,[AdmitDate]
      ,[CensusType]
      ,[PayerType]
      ,[PayerID]
      ,[UnitID]
      ,[RoomID]
      ,[BedID]
      ,[StartCensusID]
      ,[EndCensusID]
      ,[AdmitType]
      ,[AdmitSource]
      ,[PSCCode]
      ,[DischType]
      ,[Billable]
      ,[Certified]
      ,[Bedhold]
      ,[VisitCount]
      ,[LastStatus]
      ,[WriteOff]
      ,[LOCID]
      ,[DischargeExpireDuringLeave]
      ,[DischargeOutpatientSameDay]
      ,[UpdateDate] 
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientStayElement
WHERE DeletedFlag=0;
----------------------------------------------------------------------------------------
--tables needed for Sagely2

TRUNCATE TABLE                        mydata.PatientContact
TRUNCATE TABLE                        mydata.Phone; 
TRUNCATE TABLE                        mydata.PhoneType; 
TRUNCATE TABLE                        mydata.Address; 
TRUNCATE TABLE                        mydata.ContactPhoneXref
TRUNCATE TABLE                        mydata.PatientPhoneXref


INSERT	INTO	mydata.PhoneType
SELECT [PhoneTypeID]
      ,[PhoneTypeDesc]
      ,[SortOrder]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PhoneType
WHERE DeletedFlag=0;

INSERT	INTO					   mydata.Phone
SELECT [PhoneID]
      ,[PhoneTypeID]
      ,[isPrimary]
      ,[AreaCode]
      ,[Prefix]
      ,[Suffix]
      ,[Extension]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.Phone
WHERE DeletedFlag=0;


INSERT	INTO mydata.Address
SELECT [AddressID]
      ,[StreetAddress]
      ,[Suite]
      ,[City]
      ,[STATEID]
      ,[PostalCode]
      ,[LastModified]
      ,[UserID]
      ,[County]
      ,[InheritedAddressID]
      ,[InsertDate]
      ,[UpdateDate]
 FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.Address
WHERE DeletedFlag=0;

INSERT	INTO mydata.PatientContact
SELECT [ContactID]
      ,[PatientID]
      ,[ContactType]
      ,[IsPrimary]
      ,[LegalGuardian]
      ,[OtherLegalOversight]
      ,[POAHealth]
      ,[POAFinancial]
      ,[FamilyMember]
      ,[EmergencyContact]
      ,[ResponsibleParty]
      ,[Guardian]
      ,[POAHealthNonMDS]
      ,[POAFinancialNonMDS]
      ,[callPriority]
      ,[deleted]
      ,[notes]
      ,[PrimaryFinancialPatientContact]
      ,[PatientContactReceivesARStatement]
      ,[PatientContactID]
      ,[createdDate]
      ,[OtherRelation]
      ,[ResidentRepresentative]
      ,[InsertDate]
      ,[UpdateDate]
      ,[MX1_PersonID]
      ,[MX1_ContactID]
 FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientContact
WHERE DeletedFlag=0;

INSERT INTO [mydata].[ContactPhoneXref]
SELECT [ContactID]
      ,[PhoneID]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.ContactPhoneXref
WHERE DeletedFlag=0;

INSERT INTO mydata.PatientPhoneXref
SELECT [ContactID]
      ,[PhoneID]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientPhoneXref
WHERE DeletedFlag=0;



INSERT INTO mydata.logMydataRefresh (LastRefresh) values(GETDATE())

