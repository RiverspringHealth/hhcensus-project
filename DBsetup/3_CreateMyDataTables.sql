
--USE FredTesting; -- in connection on laptop PS-6KR5WF2
--GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


--------------------------------------------------------------------------------------------------
IF OBJECT_ID('mydata.Census_AdmitDischargeLocation', 'U') IS NOT NULL DROP TABLE mydata.Census_AdmitDischargeLocation
CREATE TABLE [mydata].[Census_AdmitDischargeLocation](
	[AdmDisLocationID] [int] NOT NULL,
	[OwningCorpID] [int] NULL,
	[AdmitDischargeLocationCategoryID] [int] NULL,
	[isCorporateActive] [bit] NULL,
	[LocationName] [varchar](100) NULL,
	[Description] [varchar](100) NULL,
	[isAdmitLocation] [bit] NULL,
	[isDischargeLocation] [bit] NULL,
	[HospitalReadmissionTypeCode] [varchar](10) NULL,
 CONSTRAINT [Census_AdmitDischargeLocation_PK] PRIMARY KEY CLUSTERED 
(
	[AdmDisLocationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

--------------------------------------------------------------------------------------------------

IF OBJECT_ID('mydata.Census_LevelOfCare', 'U') IS NOT NULL DROP TABLE mydata.Census_LevelOfCare
CREATE TABLE [mydata].[Census_LevelOfCare](
	[LOCID] [int] NOT NULL,
	[FacilityID] [int] NULL,
	[Description] [varchar](50) NULL,
	
	
 CONSTRAINT [Census_LevelOfCare_PK] PRIMARY KEY CLUSTERED 
(
	[LOCID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

--------------------------------------------------------------------------------------------------
IF OBJECT_ID('mydata.Census_LOA', 'U') IS NOT NULL DROP TABLE mydata.Census_LOA
CREATE TABLE [mydata].[Census_LOA](
	[LOAID] [int] NOT NULL,
	[FacilityID] [int] NULL,
	[LOACode] [char](2) NULL,
	[Description] [varchar](25) NULL,
	[Billable] [bit] NULL,
	[WriteOff] [bit] NULL,
 CONSTRAINT [Census_LOA_PK] PRIMARY KEY CLUSTERED 
(
	[LOAID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
---------------------------------------------------------------------------------------------
IF OBJECT_ID('mydata.FacilityBed', 'U') IS NOT NULL DROP TABLE mydata.FacilityBed
CREATE TABLE [mydata].[FacilityBed](
	[BedID] [int] NOT NULL,
	[RoomID] [int] NULL,
	[BedName] [varchar](5) NULL,
 CONSTRAINT [FacilityBed_PK] PRIMARY KEY CLUSTERED 
(
	[BedID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
-- ----------------------------------------------------------------------------------------------- 
IF OBJECT_ID('mydata.FacilityRoom', 'U') IS NOT NULL DROP TABLE mydata.FacilityRoom

CREATE TABLE [mydata].[FacilityRoom](
	[RoomID] [int] NOT NULL,
	[PatientGroupID] [int] NULL,
	[RoomName] [varchar](6) NULL,
	
 CONSTRAINT [FacilityRoom_PK] PRIMARY KEY CLUSTERED 
(
	[RoomID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
-- -----------------------------------------------------------------------------------------------
IF OBJECT_ID('mydata.FacilityUnitRoomBed', 'U') IS NOT NULL DROP TABLE mydata.FacilityUnitRoomBed
CREATE TABLE [mydata].[FacilityUnitRoomBed](
	[BedID] [int] NOT NULL,
	[RoomID] [int] NULL,
	[UnitID] [int] NULL,
	[FacilityID] [int] NULL,
	[BuildingID] [int] NULL,
	[UnitName] [varchar](25) NULL,
	[RoomName] [varchar](6) NULL,
	[BedName] [varchar](5) NULL,
 CONSTRAINT [FacilityUnitRoomBed_PK] PRIMARY KEY CLUSTERED 
(
	[BedID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

-------------------------------------------------------------------------------------------------


IF OBJECT_ID('mydata.Patient', 'U') IS NOT NULL DROP TABLE mydata.Patient
CREATE TABLE [mydata].[Patient](
	[PatientID] [int] NOT NULL,
	[IsActive] [bit] NULL,
	[FirstName] [varchar](50) NULL,
	[MiddleName] [varchar](50) NULL,
	[LastName] [varchar](50) NULL,
	[SSN] [char](11) NULL,
	[AddressID] [int] NULL,
	[DateOfBirth] [datetime2](7) NULL,
	[Sex] [char](1) NULL,
	[AttendingPhysicianID] [int] NULL,
	[RACECODE] [char](10) NULL,
	[MARITALSTATUSCODE] [char](10) NULL,
	[MedicareNumber] [varchar](25) NULL,
	[MedicaidNumber] [varchar](25) NULL,
	[MothersMaidenName] [varchar](25) NULL,
	[PreferredName] [varchar](25) NULL,
	[POA] [varchar](30) NULL,
	[RELIGIONCODE] [char](10) NULL,
	[MilitaryService] [varchar](25) NULL,
	[PharmacyID] [int] NULL,
--	[Notes] [varchar](6500) NULL,
--	[IdealBodyWeight] [float] NULL,
--	[Dialysis] [bit] NULL,
--	[Insurance] [varchar](256) NULL,
	[ContactAddressID] [int] NULL,
	[DNR] [bit] NULL,
	[MedicalRecordNumber] [varchar](9) NULL,
--	[ResidentNumber] [varchar](15) NULL,
--	[PreviousOccupation] [varchar](100) NULL,
--	[FirstLanguage] [varchar](80) NULL,
	[RoomNumber] [varchar](151) NULL,
--	[LastModified] [datetime2](7) NULL,
--	[UserID] [int] NULL,
	[OriginalAdmtDt] [datetime2](7) NULL,
	[CurrentAdmtDt] [datetime2](7) NULL,
--	[PatientDnrID] [int] NULL,
	[CurrentReturnDt] [datetime2](7) NULL,
	[VisitCount] [int] NULL,
	[CensusStatus] [varchar](30) NULL,
--	[faceSheetNotes] [varchar](6500) NULL,
	[MedicareBNumber] [varchar](25) NULL,
--	[ThirdPartyId] [varchar](20) NULL,
--	[ThirdPartySource] [varchar](20) NULL,
--	[MPI] [int] NULL,
--	[ExcludeFromMPI] [bit] NULL,
--	[MPILinkDateGMT] [datetime2](7) NULL,
--	[OptIn] [bit] NULL,
--	[IsInXDS] [bit] NULL,
--	[DischargeAddressID] [int] NULL,
--	[HICNMedicareA] [varchar](25) NULL,
--	[HICNMedicareB] [varchar](25) NULL,
--	[isRRB] [bit] NULL,
	[CoveredByManagedCare] [bit] NULL,
--	[MX1_PersonID] [int] NULL,
--	[SmokingStatusID] [tinyint] NULL,
	[LanguageKey] [char](3) NULL,
--	[PatientLabelID] [int] NULL,
--	[InsertDate] [datetime2](7) NULL,
--	[UpdateDate] [datetime2](7) NULL,
--	[DeletedFlag] [bit] NULL,
 CONSTRAINT [Patient_PK] PRIMARY KEY CLUSTERED 
(
	[PatientID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
--------------------------------------------------------------------------------------------------




IF OBJECT_ID('mydata.PatientCensus', 'U') IS NOT NULL DROP TABLE mydata.PatientCensus
CREATE TABLE [mydata].[PatientCensus](
	[CensusID] [int] NOT NULL,
	[FacilityID] [int] NULL,
	[PatientID] [int] NULL,
	[DateTime] [datetime2](7) NULL,
	[CensusType] [int] NULL,
	[Payer] [int] NULL,
	[LOC] [int] NULL,
	[AdmSrc] [char](1) NULL,
	[AdmType] [char](1) NULL,
	[PSC] [char](2) NULL,
	[LOA] [int] NULL,
	[BuildingID] [int] NULL,
	[HallID] [int] NULL,
	[RoomID] [int] NULL,
	[BedID] [int] NULL,
	[NewBenefit] [bit] NULL,
	[Note] [varchar](250) NULL,
	[EndDate] [datetime2](7) NULL,
	[DischargeType] [int] NULL,
	[PartADays] [int] NULL,
--	[EnhancedDays] [int] NULL,
--	[Deleted] [bit] NULL,
--	[DeleteDate] [datetime2](7) NULL,
--	[DeletedBy] [int] NULL,
--	[LastModifiedDate] [datetime2](7) NULL,
--	[LastModifiedBy] [int] NULL,
--	[AdmitFromLocationID] [int] NULL,
--	[AdmitReferralSourceID] [int] NULL,
--	[CreatedDate] [datetime2](7) NULL,
--	[CreatedByID] [int] NULL,
--	[AcuteDischargingHospitalID] [int] NULL,
--	[AcuteReporting] [bit] NULL,
--	[ACHInpatientStay] [bit] NULL,
--	[AcuteDischargeDateTime] [datetime2](7) NULL,
--	[RestartMdsSchedule] [bit] NULL,
--	[AdmissionStatusCodeDetailID] [int] NULL,
--	[CensusSubTypeID] [int] NULL,
--	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
--	[DeletedFlag] [bit] NULL,
 CONSTRAINT [PatientCensus_PK] PRIMARY KEY CLUSTERED 
(
	[CensusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

-- ------------------------------------------------------------------------------------


IF OBJECT_ID('mydata.PatientGroup', 'U') IS NOT NULL DROP TABLE mydata.PatientGroup
CREATE TABLE [mydata].[PatientGroup](
	[PatientGroupID] [int] NOT NULL,
	[FacilityID] [int] NULL,
	[Description] [varchar](25) NULL,
	[BuildingID] [int] NULL,
	--[GL_Segment] [varchar](10) NULL,
	--[Abbreviation] [varchar](10) NULL,
	--[UsesPOC] [bit] NULL,
	--[InsertDate] [datetime2](7) NULL,
	--[UpdateDate] [datetime2](7) NULL,
	--[DeletedFlag] [bit] NULL,
 CONSTRAINT [PatientGroup_PK] PRIMARY KEY CLUSTERED 
(
	[PatientGroupID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
-- -----------------------------------------------------------------------------------------------
IF OBJECT_ID('mydata.PatientStayElement', 'U') IS NOT NULL DROP TABLE mydata.PatientStayElement
CREATE TABLE [mydata].[PatientStayElement](
	[FacilityID] [int] NOT NULL,
	[PatientID] [int] NOT NULL,
	[StartDate] [datetime2](7) NOT NULL,
	[EndDate] [datetime2](7) NULL,
	[AdmitDate] [datetime2](7) NULL,
	[CensusType] [int] NULL,
	[PayerType] [int] NULL,
	[PayerID] [int] NULL,
	[UnitID] [int] NULL,
	[RoomID] [int] NULL,
	[BedID] [int] NULL,
	[StartCensusID] [int] NULL,
	[EndCensusID] [int] NULL,
	[AdmitType] [int] NULL,
	[AdmitSource] [char](1) NULL,
	[PSCCode] [char](2) NULL,
	[DischType] [int] NULL,
	[Billable] [int] NULL,
	[Certified] [int] NULL,
	[Bedhold] [int] NULL,
	[VisitCount] [int] NULL,
	[LastStatus] [varchar](30) NULL,
	[WriteOff] [bit] NULL,
	[LOCID] [int] NULL,
	[DischargeExpireDuringLeave] [int] NULL,
	[DischargeOutpatientSameDay] [bit] NULL,
--	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
--	[DeletedFlag] [bit] NULL
) ON [PRIMARY]

GO




-- ---------------------------------------------------------------------------------------------- 

IF OBJECT_ID('mydata.Census_Types', 'U') IS NOT NULL DROP TABLE mydata.Census_Types
CREATE TABLE [mydata].[Census_Types](
	[CensusType] [int] NOT NULL,
	[Description] [varchar](20) NULL,
 CONSTRAINT [Census_Types_PK] PRIMARY KEY CLUSTERED 
(
	[CensusType] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
-- -----------------------------------------------------------------------------------------------
--CREATE  INDEX PatientStayElement_NDX ON             mydata.PatientStayElement(PatientID);

/****** Object:  Table [mydata].[LogMyDataRefresh]    Script Date: 2/24/2020 12:56:11 PM ******/
/*
CREATE TABLE [mydata].[LogMyDataRefresh](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[LastRefresh] [datetime] NOT NULL
) ON [PRIMARY]

GO
*/


-- ------------------------new tables for Sagely2-----------------------------------------------------
IF OBJECT_ID('mydata.[Address]', 'U') IS NOT NULL DROP TABLE mydata.[Address]
CREATE TABLE [mydata].[Address](
	[AddressID] [int] NOT NULL PRIMARY KEY,
	[StreetAddress] [varchar](50) NULL,
	[Suite] [varchar](20) NULL,
	[City] [varchar](50) NULL,
	[STATEID] [char](2) NULL,
	[PostalCode] [varchar](20) NULL,
	[LastModified] [datetime2](7) NULL,
	[UserID] [int] NULL,
	[County] [varchar](50) NULL,
	[InheritedAddressID] [int] NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
--not required, no deleted records are copied	[DeletedFlag] [bit] NULL
) ON [PRIMARY]

GO
 



IF OBJECT_ID('mydata.PhoneType', 'U') IS NOT NULL DROP TABLE mydata.PhoneType
CREATE TABLE [mydata].[PhoneType](
	[PhoneTypeID] [int] NOT NULL PRIMARY KEY,
	[PhoneTypeDesc] [varchar](50) NOT NULL,
	[SortOrder] [int] NOT NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL
) ON [PRIMARY]

GO


IF OBJECT_ID('mydata.Phone', 'U') IS NOT NULL DROP TABLE mydata.Phone

CREATE TABLE [mydata].[Phone](
	[PhoneID] [int] NOT NULL PRIMARY KEY,
	[PhoneTypeID] [int] NULL,
	[isPrimary] [bit] NULL,
	[AreaCode] [char](3) NULL,
	[Prefix] [char](3) NULL,
	[Suffix] [char](4) NULL,
	[Extension] [varchar](6) NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
--not needed, dont copy deleted records	[DeletedFlag] [bit] NULL
) ON [PRIMARY]

GO


IF OBJECT_ID('mydata.[PatientContact]', 'U') IS NOT NULL DROP TABLE mydata.[PatientContact]

CREATE TABLE [mydata].[PatientContact](
	[ContactID] [int] NOT NULL,
	[PatientID] [int] NOT NULL,
	[ContactType] [int] NULL,
	[IsPrimary] [bit] NULL,
	[LegalGuardian] [bit] NULL,
	[OtherLegalOversight] [bit] NULL,
	[POAHealth] [bit] NULL,
	[POAFinancial] [bit] NULL,
	[FamilyMember] [bit] NULL,
	[EmergencyContact] [bit] NULL,
	[ResponsibleParty] [bit] NULL,
	[Guardian] [bit] NULL,
	[POAHealthNonMDS] [bit] NULL,
	[POAFinancialNonMDS] [bit] NULL,
	[callPriority] [int] NULL,
	[deleted] [bit] NULL,
	[notes] [varchar](500) NULL,
	[PrimaryFinancialPatientContact] [bit] NULL,
	[PatientContactReceivesARStatement] [bit] NULL,
	[PatientContactID] [int] NULL,
	[createdDate] [datetime2](7) NULL,
	[OtherRelation] [varchar](50) NULL,
	[ResidentRepresentative] [bit] NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
-- not needed, removed during copy	[DeletedFlag] [bit] NULL,
	[MX1_PersonID] [int] NULL,
	[MX1_ContactID] [int] NULL
) ON [PRIMARY]

GO

 

IF OBJECT_ID('mydata.ContactPhoneXref', 'U') IS NOT NULL DROP TABLE mydata.ContactPhoneXref
CREATE TABLE [mydata].[ContactPhoneXref](
	[ContactID] [int] NOT NULL,
	[PhoneID] [int] NOT NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
--not needed, removed during copy	[DeletedFlag] [bit] NULL
 CONSTRAINT [ContactPhoneXref_PK] PRIMARY KEY CLUSTERED 
(
	ContactID, PhoneID
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]


IF OBJECT_ID('mydata.PatientPhoneXRef', 'U') IS NOT NULL DROP TABLE mydata.PatientPhoneXRef
CREATE TABLE [mydata].[PatientPhoneXRef](
	[PatientID] [int] NOT NULL,
	[PhoneID] [int] NOT NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
 CONSTRAINT [PatientPhoneXRef_PK] PRIMARY KEY CLUSTERED 
(
	[PatientID] ASC,
	[PhoneID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];



IF OBJECT_ID('mydata.ContactType', 'U') IS NOT NULL DROP TABLE mydata.ContactType
CREATE TABLE [mydata].[ContactType](
	[ContactTypeID] [int] NOT NULL PRIMARY KEY,
	[ContactTypeDesc] [varchar](50) NOT NULL,
	[SortOrder] [int] NULL,
	[active] [bit] NOT NULL,
	[HL7v3RoleCode] [varchar](10) NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
	
) ON [PRIMARY];


IF OBJECT_ID('mydata.Contact', 'U') IS NOT NULL DROP TABLE mydata.Contact
CREATE TABLE [mydata].[Contact](
	[ContactID] [int] NOT NULL,
	[Prefix] [varchar](10) NULL,
	[FirstName] [varchar](100) NULL,
	[MiddleName] [varchar](25) NULL,
	[LastName] [varchar](25) NULL,
	[Suffix] [varchar](10) NULL,
	[PhoneNumberAreaCode] [char](3) NULL,
	[PhoneNumberPrefix] [char](3) NULL,
	[PhoneNumberSuffix] [char](4) NULL,
	[PhoneNumberExtension] [varchar](6) NULL,
	[FaxNumberAreaCode] [char](3) NULL,
	[FaxNumberPrefix] [char](3) NULL,
	[FaxNumberSuffix] [char](4) NULL,
	[EmailAddress] [varchar](150) NULL,
	[AddressID] [int] NULL,
	[PagerNumberAreaCode] [char](3) NULL,
	[PagerNumberPrefix] [char](3) NULL,
	[PagerNumberSuffix] [char](4) NULL,
	[InheritedSuperPayerID] [int] NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL
) ON [PRIMARY];


IF OBJECT_ID('mydata.[PatientContact]', 'U') IS NOT NULL DROP TABLE mydata.[PatientContact]
CREATE TABLE [mydata].[PatientContact](
	[ContactID] [int] NOT NULL,
	[PatientID] [int] NOT NULL,
	[ContactType] [int] NULL,
	[IsPrimary] [bit] NULL,
	[LegalGuardian] [bit] NULL,
	[OtherLegalOversight] [bit] NULL,
	[POAHealth] [bit] NULL,
	[POAFinancial] [bit] NULL,
	[FamilyMember] [bit] NULL,
	[EmergencyContact] [bit] NULL,
	[ResponsibleParty] [bit] NULL,
	[Guardian] [bit] NULL,
	[POAHealthNonMDS] [bit] NULL,
	[POAFinancialNonMDS] [bit] NULL,
	[callPriority] [int] NULL,
	[deleted] [bit] NULL,
	[notes] [varchar](500) NULL,
	[PrimaryFinancialPatientContact] [bit] NULL,
	[PatientContactReceivesARStatement] [bit] NULL,
	[PatientContactID] [int] NULL,
	[createdDate] [datetime2](7) NULL,
	[OtherRelation] [varchar](50) NULL,
	[ResidentRepresentative] [bit] NULL,
	[InsertDate] [datetime2](7) NULL,
	[UpdateDate] [datetime2](7) NULL,
-- not needed, removed during copy	[DeletedFlag] [bit] NULL,
	[MX1_PersonID] [int] NULL,
	[MX1_ContactID] [int] NULL
) ON [PRIMARY];