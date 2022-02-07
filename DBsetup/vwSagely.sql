USE [CensusApps]
GO

/****** Object:  View [mydata].[vwSagely]    Script Date: 2/7/2022 8:17:47 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE VIEW [mydata].[vwSagely] AS

SELECT --* --MedicalRecordNumber, count(*)
	  pat.MedicalRecordNumber
	, pat.LastName [Resident_Last]
	, pat.FirstName [Resident_First]
	, CONVERT(VARCHAR(12), DateOfBirth, 101) [DOB]
	, bed.UnitName [LevelOfCare] --unit goes here
	, pat.MiddleName [MiddleName]
	, NULL [MaidenName] -- not used
	, pat.PreferredName [Nickname]
	, CASE 
			WHEN patphone.AreaCode IS NOT NULL THEN  CONCAT('(', patphone.AreaCode, ') ', patphone.Prefix, '-', patphone.Suffix) 
			ELSE NULL
	  END [Phone] 
	, NULL [Email] -- not used
	, CONCAT(ec.FirstName, ' ', ec.LastName) [EmergencyName] --@
	, CASE 
			WHEN ecphone.AreaCode IS NOT NULL THEN  CONCAT('(', ecphone.AreaCode, ') ', ecphone.Prefix, '-', ecphone.Suffix) 
			ELSE NULL
	  END [EmergencyPhone] 
	, pat.Sex [Gender]
	, NULL [Ethnicity] --not used
	, NULL [HomeTown] -- not used
	, pse.LastStatus [Status]
	, CONVERT(VARCHAR(12), pse.AdmitDate, 101) [MoveInDate]
	, bed.RoomName [Room]
	, SUBSTRING(bed.UnitName, 2, 1) [Floor]
	, NULL [Diabetic]
	, NULL [HearingImpairment]
	, NULL [SpeechImpairment]
	, NULL [VisionImpairment]
	, NULL [TherapyAnimal]
	, NULL [RequireCaine]
	, NULL [RequiresMotorScooter]
	, NULL [RequiresWalker]
	, NULL [RequiresWheelchair]
	, NULL [AdvanceCareDirective]
	, NULL [Excursions]
	, 'Form not Received' [three commas]
FROM (
	SELECT * 
	FROM mydata.vwPatientStayElementLatest
	WHERE LastStatus='In House'
UNION

	SELECT *
	FROM mydata.vwPatientStayElementLatest
	WHERE LastStatus IN ('Expired', 'Discharged', 'Discharged RE') 
		AND StartDate > DATEADD(day, -30, GETDATE() )  
		AND MedicalRecordNumber NOT IN (SELECT MedicalRecordNumber FROM mydata.vwPatientInHouse)
) AS pse
	--GROUP BY MedicalRecordNumber
	--having count(*) > 1
	JOIN mydata.Patient AS pat ON pat.PatientID = pse.PatientID
	JOIN mydata.FacilityUnitRoomBed AS bed ON bed.BedID=pse.BedID
---------------------------------------------- Emergency Contact ------------------------------------------
OUTER APPLY (
		SELECT TOP 1 PatientID, AreaCode, Prefix, Suffix
		FROM mydata.Phone AS ph
		JOIN mydata.PatientPhoneXRef AS x ON x.PhoneID=ph.PhoneID
		JOIN mydata.PhoneType AS pt ON pt.PhoneTypeID=ph.PhoneTypeID
		WHERE pt.PhoneTypeID NOT IN (5,6) --eliminate fax, leave pager
			AND x.PatientID = pat.PatientID
			AND ph.AreaCode IS NOT NULL
			AND LEN(ph.AreaCode) >1
		ORDER BY ph.isPrimary DESC, pt.SortOrder
		) AS patphone




OUTER APPLY (  -- get contact with lowest priority number which we assume is highest priority.
		SELECT TOP 1 * 
		FROM mydata.PatientContact
		WHERE  EmergencyContact=1
		AND PatientID = pat.PatientID
		ORDER BY callPriority
		) AS pcx  




LEFT JOIN mydata.Contact AS ec ON ec.ContactID = pcx.ContactID  --emergency contact
OUTER APPLY (
			select top 1 ph.AreaCode, ph.Prefix, ph.Suffix
			FROM mydata.ContactPhoneXref AS xph
			JOIN mydata.Phone AS ph ON ph.PhoneID = xph.PhoneID
			JOIN mydata.PhoneType AS pt ON pt.PhoneTypeID=ph.PhoneTypeID
			WHERE pt.PHoneTypeID   NOT IN(5,6)  -- eliminate fax
				AND xph.ContactID= ec.ContactID
				AND LEN(ph.AreaCode)>0
			ORDER BY pt.SortOrder
	) AS ecphone 
--ORDER BY pat.LastName, pat.FirstName, pat.DateOfBirth


GO

