USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataBed]    Script Date: 01/14/2020 10:53:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



  CREATE VIEW [dbo].[mydataBed] AS 
  SELECT facbed.BedID
     , facbed.RoomID
     , facroom.PatientGroupID AS UnitID
     , RTRIM(LTRIM(patgrp.Abbreviation)) AS UnitName
     , RTRIM(LTRIM(facroom.RoomName)) AS RoomName
     , RTRIM(LTRIM(facbed.BedName)) AS BedName
	 , RTRIM(LTRIM(facroom.RoomName)) +'/' + RTRIM(LTRIM(facbed.BedName)) AS RoomAndBed
/*	 , fac.Name [FacilityName]
	 , fac.FacilityTypeCode [FacilityTypeCode]
	 , fac.NationalProviderID */
	 , cert.BeginDate
	 , cert.EndDate
	 , cert.BedTypeID
	 , bedtype.BedTypeDesc
  FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].[FacilityBed] AS facbed
  JOIN [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.FacilityBedCert as cert ON cert.BedId=facbed.bedid
  JOIN [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.FacilityRoom AS facroom ON  facroom.RoomID=facbed.RoomID
  JOIN [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.PatientGroup AS patgrp ON patgrp.PatientGroupID=facroom.PatientGroupID
  JOIN [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.Facility AS fac ON fac.Facilityid=cert.FacilityID
  LEFT JOIN [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.FacilityBedType AS bedtype on bedtype.BedTypeID=cert.BedTypeID
  WHERE facbed.DeletedFlag=0
  OR facroom.DeletedFlag=0
  OR cert.DeletedFlag=0
  OR patgrp.DeletedFlag=0
  OR fac.DeletedFlag=0
  OR bedtype.DeletedFlag=0

GO



USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataCensus_AdmitDischargeLocation]    Script Date: 01/14/2020 10:54:14 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE VIEW [dbo].[mydataCensus_AdmitDischargeLocation] AS
SELECT *  
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.Census_AdmitDischargeLocation
WHERE DeletedFlag=0


GO



USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataCensus_LevelOfCare]    Script Date: 01/14/2020 10:54:29 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [dbo].[mydataCensus_LevelOfCare] AS 
SELECT * 
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].Census_LevelOfCare
WHERE DeletedFlag = 0

GO


USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataCensus_Types]    Script Date: 01/14/2020 10:54:44 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE VIEW [dbo].[mydataCensus_Types] AS 
SELECT * 
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].Census_Types
WHERE DeletedFlag = 0


GO

USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatient]    Script Date: 01/14/2020 10:54:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [dbo].[mydataPatient] AS
SELECT * FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].[Patient]
WHERE DeletedFlag = 0

GO



USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatientActive]    Script Date: 01/14/2020 10:55:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE  VIEW [dbo].[mydataPatientActive] AS
SELECT *
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].[Patient]
WHERE DeletedFlag = 0
AND isActive=1

GO


USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatientActiveInHouse]    Script Date: 01/14/2020 10:55:33 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE  VIEW [dbo].[mydataPatientActiveInHouse] AS
SELECT *
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].[STVSNF].[Patient]
WHERE DeletedFlag = 0
AND isActive=1
AND CensusStatus='In House'


GO


USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatientStayElement]    Script Date: 01/14/2020 10:55:51 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [dbo].[mydataPatientStayElement] AS
SELECT *  
FROM [MYDATAHOST5].[BIDW_50582_HebrewHome].STVSNF.PatientStayElement
WHERE DeletedFlag=0

GO



USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatientStayElementDischarges]    Script Date: 01/14/2020 10:56:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [dbo].[mydataPatientStayElementDischarges] AS 
SELECT changes.*
FROM dbo.mydataPatientStayElement AS changes
JOIN (
	SELECT PatientID, MAX(AdmitDate) [AdmitDate]
	FROM dbo.mydataPatientStayElement  
	WHERE CensusType=4  --stay with a DC
	GROUP BY PatientID
	) AS LastStay ON LastStay.PatientID=changes.PatientID
WHERE CensusType=4  -- only DC element in stay with a DC



GO

USE [FredTesting]
GO

/****** Object:  View [dbo].[mydataPatientStayElementLastStayOnly]    Script Date: 01/14/2020 10:56:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [dbo].[mydataPatientStayElementLastStayOnly] AS 
SELECT changes.*
FROM dbo.mydataPatientStayElement AS changes
JOIN (
	SELECT PatientID, MAX(AdmitDate) [AdmitDate]
	FROM dbo.mydataPatientStayElement  
	GROUP BY PatientID
	) AS LastStay ON LastStay.PatientID=changes.PatientID AND changes.AdmitDate=LastStay.AdmitDate



GO

















