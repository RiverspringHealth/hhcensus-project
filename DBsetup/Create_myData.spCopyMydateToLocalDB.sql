USE [CensusApps]
GO

/****** Object:  StoredProcedure [mydata].[spCopyMyDataToLocalDB]    Script Date: 5/6/2020 3:43:51 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

 
    /*ALTER   PROCEDURE  mydata.spCopyMyDataToLocalDB  
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
    ***************************************************************************** */
  








ALTER  PROCEDURE [mydata].[spCopyMyDataToLocalDB] AS
BEGIN
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
----------------------------------------------------------------------------------------
--tables needed for Sagely2

TRUNCATE TABLE                        mydata.Contact
TRUNCATE TABLE                        mydata.PatientContact
TRUNCATE TABLE                        mydata.Phone; 
TRUNCATE TABLE                        mydata.PhoneType; 
TRUNCATE TABLE                        mydata.Address; 
TRUNCATE TABLE                        mydata.ContactPhoneXref
TRUNCATE TABLE                        mydata.PatientPhoneXref


INSERT	INTO	mydata.Contact
SELECT [ContactID]
      ,[Prefix]
      ,[FirstName]
      ,[MiddleName]
      ,[LastName]
      ,[Suffix]
      ,[PhoneNumberAreaCode]
      ,[PhoneNumberPrefix]
      ,[PhoneNumberSuffix]
      ,[PhoneNumberExtension]
      ,[FaxNumberAreaCode]
      ,[FaxNumberPrefix]
      ,[FaxNumberSuffix]
      ,[EmailAddress]
      ,[AddressID]
      ,[PagerNumberAreaCode]
      ,[PagerNumberPrefix]
      ,[PagerNumberSuffix]
      ,[InheritedSuperPayerID]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.[Contact]
WHERE DeletedFlag=0;


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


INSERT INTO [mydata].[PatientPhoneXref]
SELECT [PatientID]
      ,[PhoneID]
      ,[InsertDate]
      ,[UpdateDate]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].STVSNF.PatientPhoneXref
WHERE DeletedFlag=0;


INSERT INTO mydata.logMydataRefresh (LastRefresh) values(GETDATE());



--INSERT INTO mydata.logMydataRefresh (LastRefresh) values(GETDATE());

/******************************** add new tables for RXNT export ******************************************/

TRUNCATE TABLE  mydata.FacilityPayers
INSERT INTO mydata.FacilityPayers 
SELECT 
       [PayerID]
      ,[SuperPayerID]
      ,[FacilityID]
      ,[PayerType]
      ,[Name]
      ,[ContactID]
      ,[Plan_Name]
      ,[Group_Name]
      ,[Provider_No]
      ,[AR_Acct]
      ,[CoPay_AR_Acct]
      ,[Percentage]
      ,[Deductable]
      ,[Statement_Form]
      ,[Place_of_Service]
      ,[County_Code]
      ,[Locator_Code]
      ,[Category_of_Service]
      ,[Rate_Code]
      ,[Day_of_Death]
      ,[Day_of_Disch]
      ,[PreBill]
      ,[InActive]
      ,[CarrierID]
      ,[ECS_Status]
      ,[CoveredCoPayDays]
      ,[AdjAcct]
      ,[ContAcct]
      ,[MedACoPay]
      ,[MedACoPayPercent]
      ,[MedACoPayAmount]
      ,[MedBCoPay]
      ,[MedBCoPayPercent]
      ,[PrimaryRmChgs]
      ,[RmChgPercent]
      ,[PrimaryAnc]
      ,[AncPercent]
      ,[PatLiabOnHold]
      ,[SplitClaims]
      ,[UB_Rm_Rate]
      ,[UB_Anc_Rate]
      ,[ClaimSignature]
      ,[AdmitDate]
      ,[PatLiab]
      ,[WriteOffAcct]
      ,[RefundAcct]
      ,[GL_Segment]
      ,[CorpPayerID]
      ,[PartA_Xover]
      ,[PartB_Xover]
      ,[UB_view_single]
      ,[StateID]
      ,[EnhancedRate]
      ,[DefaultPvtPay]
      ,[ChargePatLiabOnHold]
      ,[PvtPayHoldSame]
      ,[HospHoldAmount]
      ,[HospHoldPercent]
      ,[TherLvHoldAmount]
      ,[TherLvHoldPercent]
      ,[ContactName]
      ,[Address]
      ,[Suite]
      ,[City]
      ,[Zip]
      ,[PhoneAreaCode]
      ,[PhonePrefix]
      ,[PhoneSuffix]
      ,[FaxAreaCode]
      ,[FaxPrefix]
      ,[FaxSuffix]
      ,[SplitClaimsLOC]
      ,[Mcr24Bill]
      ,[CreateDate]
      ,[BillDayOfAdmit]
      ,[ProratePatientLiability]
      ,[SubPayerTypeID]
      ,[ChargeSplitHeaderID]
      ,[NationalProviderID]
      ,[PayerCode]
      ,[AnnualNoPayClaimsThroughMonth]
      ,[TaxonomyCode]
      ,[CarrierCode]
      ,[DefaultHcpcsModifier1]
      ,[OccupancyTypeID]
      ,[FiscalYearStartMonth]
      ,[OccupancyOverrideBeginDate]
      ,[OccupancyOverrideEndDate]
      ,[OriginalPayerTypeID]
      ,[FL50MedicaidIsLastPayer]
      ,[ShowSpecialRatesRoom]
      ,[ShowSpecialRatesAnc]
      ,[DefaultClinicalPayer]
      ,[ShowRugOverrideInSpecialRates]
      ,[OverpaymentMaximumAdjustment]
      ,[UnderpaymentMaximumAdjustment]
      ,[NoPaymentClaimsAutoCreationFrequency]
      ,[UseGrossRateInsteadOfReimbursementRateOnStatement]
      ,[ICD10StartDate]
      ,[RemitAdjustmentAcctID]
      ,[RemitAdjustmentGroupCode]
      ,[RemitAdjustmentReasonCode]
      ,[VeteranPayer]
      ,[PayerGroupID]
      ,[MedicareDirect]
      ,[UseClinicalDiagnosisCodes]
      ,[PBJCensusClassificationID]
      ,[PendingInsurancePayer]
      ,[PendingInsuranceMinimumBalance]
      ,[UsePendingInsuranceMinimumBalance]
      ,[TherapyCapModifier]
      ,[CensusPayerDefaultDischargeExpire]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].FacilityPayers
DELETE FROM mydata.FacilityPayers WHERE DeletedFlag = 1

TRUNCATE TABLE [mydata].[FacilityFacilityGroupXref]
INSERT INTO [mydata].[FacilityFacilityGroupXref]
SELECT [FacilityGroupID]
      ,[FacilityID]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
  FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].[FacilityFacilityGroupXref]
  DELETE FROM mydata.FacilityFacilityGroupXref WHERE DeletedFlag=1

  TRUNCATE TABLE mydata.AR_PayerGroup 
  INSERT INTO mydata.AR_PayerGroup 
  SELECT [PayerGroupID]
      ,[PayerGroupName]
      ,[CorporateFacilityID]
      ,[PayerGroupAbbrev]
      ,[Active]
      ,[CreatedDate]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
  FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].AR_PayerGroup
  DELETE FROM mydata.AR_PayerGroup WHERE DeletedFlag=1


  TRUNCATE TABLE mydata.AR_Patient_Payer 
  INSERT INTO mydata.AR_Patient_Payer 
  SELECT [Patient_PayerID]
      ,[SuperPayerID]
      ,[PatientID]
      ,[PayerID]
      ,[PayerType]
      ,[Sequence]
      ,[ContactID]
      ,[BeginDate]
      ,[EndDate]
      ,[Deductable_Left]
      ,[California_TAR]
      ,[Release_Signed]
      ,[Assignment]
      ,[Insured_First_Name]
      ,[Insured_Mid_Initial]
      ,[Insured_Last_Name]
      ,[Relationship_Code]
      ,[Group_Name]
      ,[Group_Number]
      ,[Treatment_Auth]
      ,[ESC]
      ,[Employer_Name]
      ,[Employer_Location]
      ,[Print_Statements]
      ,[Statement_Form]
      ,[PvtRespParty]
      ,[NewPayer]
      ,[CoveredDaysUsed]
      ,[Deleted]
      ,[Active]
      ,[ID_Number]
      ,[UBContactID]
      ,[UBContactType]
      ,[UBAddress]
      ,[UBCity]
      ,[UBState]
      ,[UBZip]
      ,[MedAReplacementPayerID]
      ,[PayerNameOverrideID]
      ,[ReportAddressInFL38FL80]
      ,[Address1FL38FL80]
      ,[Address2FL38FL80]
      ,[StateFL38FL80]
      ,[CityFL38FL80]
      ,[ZipFL38FL80]
      ,[FL38FL80AddressToUse]
      ,[QmbPayer]
      ,[ReferringPhysicianProviderID]
      ,[CreatedDate]
      ,[CreatedById]
      ,[LastModifiedDate]
      ,[LastModifiedById]
      ,[DeletedDate]
      ,[DeletedById]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
  FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].AR_Patient_Payer
  DELETE FROM mydata.AR_Patient_Payer WHERE DeletedFlag=1

  TRUNCATE TABLE mydata.Facility 
  INSERT INTO mydata.Facility 
  SELECT [FacilityID]
      ,[FACILITYTYPECODE]
      ,[IsActive]
      ,[CanBeInherited]
      ,[UseDigitalSignatures]
      ,[Name]
      ,[Location]
      ,[AddressID]
      ,[MedicareNumber]
      ,[CLIANumber]
      ,[TimezoneID]
      ,[IsPOCFacility]
      ,[EOSNotification]
      ,[EMailAddress]
      ,[Password]
      ,[IsLandscape]
      ,[mdsLiveDate]
      ,[Non_CertifiedBed_Submission_Req]
      ,[mdsIsActive]
      ,[isNumaricMedicalNumber]
      ,[MedicalRecordSeed]
      ,[IsMilitaryTime]
      ,[NDC_ID]
      ,[medicalRecordLength]
      ,[hoursEventCanBeEdited]
      ,[daysAssessmentCanBeEdited]
      ,[hoursToWarnEventEditLockdown]
      ,[hoursToWarnAssessmentEditLockdown]
      ,[certificationStartDate]
      ,[daysToWarnCertificationMedicare]
      ,[OrderReqDiagnosis]
      ,[ordersRequireAmount]
      ,[daysNextCareConferenceDefault]
      ,[daysNextCareConferencePeriod]
      ,[isFaxChecked]
      ,[daysToContinueDischarged_ExpiredRecord]
      ,[printFlowsheetSignaturePerPage]
      ,[canExportToMDS]
      ,[MDS_Xtra_Discharge]
      ,[isDCFaxChecked]
      ,[measurementListingTimeframeDefault]
      ,[showMDSPreviousAnswers]
      ,[isRequireOrderCategory]
      ,[usesSecondaryAuthentication]
      ,[visitFrequency]
      ,[latePhysicianReminder]
      ,[earlyPhysicianReminder]
      ,[earlyReminderInd]
      ,[lateWarningInd]
      ,[nationalProviderId]
      ,[isInPhysicianOrderConversion]
      ,[allowsSchedule2Faxing]
      ,[faxQueueTimer]
      ,[newOrdersDefaultFax]
      ,[changeOrdersDefaultFax]
      ,[DCOrdersDefaultFax]
      ,[expirePasswords]
      ,[expirationDays]
      ,[graceLogins]
      ,[storePasswordHistory]
      ,[passwordStorageNumber]
      ,[maxLoginAttempts]
      ,[ordersSingleAgentFaxing]
      ,[ordersForceDCFaxing]
      ,[ordersDefaultOrderedBy]
      ,[IsEEFacility]
      ,[dispenseDirectivesRequired]
      ,[progress_note_late_when_backdated]
      ,[district_office]
      ,[showCarePlanEdit]
      ,[carePlanReportStyle]
      ,[achieveBillingID]
      ,[forgotPasswordActivated]
      ,[CareLevelID]
      ,[allowOrderAdminTimeOverride]
      ,[IsGoalTypeRequired]
      ,[copyPreviousObservation]
      ,[IsProblemCategoryRequired]
      ,[CreatedDateGMT]
      ,[CreatedById]
      ,[sessionTimeout]
      ,[POCSessionTimeout]
      ,[assistedLivingEnabled]
      ,[secondaryAuthEmar]
      ,[secondaryAuthPrescOrderEntry]
      ,[secondaryAuthNonPrescOrderEntry]
      ,[secondaryAuthPrescElectOrderSignature]
      ,[allowPrescriptionFaxResend]
      ,[ccdDocumentTypeId]
      ,[daysDeleteHIERequest]
      ,[hl7FacilityOid]
      ,[orderReqICD10Diagnosis]
      ,[disableDispenseDirectives]
      ,[ssoReqLogoutWarning]
      ,[PbjFacilityID]
      ,[isDischargeOrdersActive]
      ,[RequireSsnOnFaceSheet]
      ,[ResidentHieConsentDefault]
      ,[SesDirectEmailAddress]
      ,[isAncillaryStandingOrdersActive]
      ,[HasInitialMedNotesAssigned]
      ,[MaxRowsToDisplayForUserAssignments]
      ,[AllowDuplicateSSN]
      ,[EnableCarePlanEndDate]
      ,[AutoEndProbApproach]
      ,[MaxDaysToCPEndDate]
      ,[IndivServicePlans]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
  FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].Facility
  DELETE FROM mydata.Facility WHERE DeletedFlag=1


TRUNCATE TABLE mydata.AR_PayerNameOverride
INSERT INTO mydata.AR_PayerNameOverride
SELECT [PayerNameOverrideID]
      ,[FacilityID]
      ,[PayerType]
      ,[OverrideName]
      ,[Active]
      ,[CreatedDate]
      ,[PayerIDCode]
      ,[ReportAddress]
      ,[Address1]
      ,[Address2]
      ,[State]
      ,[City]
      ,[Zip]
      ,[CorpPayerNameOverrideID]
      ,[InheritFromCorp]
      ,[PhoneNumberAreaCode]
      ,[PhoneNumberPrefix]
      ,[PhoneNumberSuffix]
      ,[FaxNumberAreaCode]
      ,[FaxNumberPrefix]
      ,[FaxNumberSuffix]
      ,[ProviderNumber]
      ,[ModifiedDate]
      ,[ICD10StartDate]
      ,[PBJCensusClassificationID]
      ,[InsertDate]
      ,[UpdateDate]
      ,[DeletedFlag]
FROM [MATRIXCARE].[BIDW_50582_HebrewHome].[STVSNF].AR_PayerNameOverride
DELETE FROM mydata.AR_PayerNameOverride WHERE DeletedFlag=1

 END; 
 

GO


