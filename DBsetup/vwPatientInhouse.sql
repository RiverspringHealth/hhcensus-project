USE [CensusApps]
GO

/****** Object:  View [mydata].[vwPatientInhouse]    Script Date: 2/7/2022 8:20:55 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



ALTER VIEW [mydata].[vwPatientInhouse] AS
select psel.PatientID, psel.MedicalRecordNumber, psel.BedID
	   , LastName, FirstName, pat.Sex [Gender], psel.AdmitDate, UnitName, RoomName, psel.StartCensusID
	   ,fac.Name
  from mydata.vwPatientStayElementLatest as psel
  --JOIN mydata.PatientCensus AS pc ON pc.CensusID=psel.EndCensusID
  --JOIN mydata.Census_Types AS ct ON ct.CensusType = pc.CensusType
  JOIN mydata.Patient as pat ON pat.PatientID=psel.PatientID
  JOIN mydata.FacilityUnitRoomBed AS bed on bed.BedID=psel.Bedid
  JOIN mydata.Facility as fac on fac.FacilityID=psel.FacilityID
  where LastStatus='In House'


GO

