USE [CensusApps]
GO

/****** Object:  View [mydata].[vwPatientStayElementLatest]    Script Date: 2/7/2022 8:21:35 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


ALTER VIEW [mydata].[vwPatientStayElementLatest] AS
SELECT pat.MedicalRecordNumber, pse.*
FROM mydata.PatientStayElement AS pse
JOIN mydata.patient AS pat ON pat.PatientID=pse.PatientID
 JOIN (
	 SELECT PatientID, MAX(StartDate) AS StartDate
	 FROM mydata.PatientStayElement 
	 GROUP BY PatientID
	 ) AS last ON last.PatientID=pse.PatientID AND last.StartDate=pse.StartDate
	 

GO

