'''
Created on Dec 30, 2019

@author: fsells
'''
UNIT_SUMMARY = '''SELECT 
		CONVERT(VARCHAR(10), GETDATE(), 101) [Census_Date]
		,UnitName [Location]
      , count(*) [Patient_Count]
	  , CASE 
			WHEN  DATEPART(HOUR, GETDATE()) BETWEEN 5 and 6 THEN 'Day'
			WHEN  DATEPART(HOUR, GETDATE()) BETWEEN 13 and 14 THEN 'Eve'
			WHEN  DATEPART(HOUR, GETDATE()) BETWEEN 21 and 22 THEN 'Eve'
			ELSE 'XXX'
		END [Shift]
  FROM [CensusApps].[mydata].[vwAllBedsAndCurrentOccupants]
  WHERE PatientID IS NOT NULL and LastStatus='In House'
  group by UnitName
  ORDER BY UnitName'''

ALL_BEDS = ''' SELECT * FROM mydata.FacilityUnitRoomBed ORDER BY UnitName, RoomName, BedName   '''

ALL_PATIENTS = '''
                  SELECT pat.*, stay.BedID, 
                  IIF( stay.LOCID IS NULL, '', loc.Description )  [LevelOfCare] ,
                  IIF( stay.BedID IS NULL, '', CONCAT(bed.UnitName, '-', bed.RoomName, '/', bed.BedName) ) AS RoomAndBed 
                  FROM mydata.Patient   AS pat
                  LEFT JOIN mydata.vwPatientStayElementLatest AS stay ON  stay.PatientID=pat.PatientID
                  LEFT JOIN mydata.Census_LevelOfCare AS loc on loc.LOCID = stay.LOCID and stay.FacilityID=loc.FacilityID 
                  LEFT JOIN mydata.FacilityUnitRoomBed AS bed on bed.BedID = stay.BedID
                  ORDER BY LastName, FirstName
                '''

LEVEL_OF_CARE_DEFINITIONS = '''SELECT * FROM mydata.Census_LevelOfCare WHERE FacilityID=15 --SNF'''

CENSUS_ADMIT_DISCHARGE_LOCATION = '''SELECT * FROM mydata.Census_AdmitDischargeLocation ORDER BY LocationName'''

CENSUS_LOA = '''SELECT * FROM mydata.Census_LOA   WHERE  FacilityID=15  ORDER BY Description '''

All_BEDS_AND_CURRENT_OCCUPANTS = '''
          SELECT UnitName, CONCAT(RoomName, '/', BedName) AS RoomAndBed, MedicalRecordNumber
          ,  CONCAT(LastName,' ', FirstName) [Name]
          , LastStatus, LevelOfCare, Sex, OriginalAdmtDt, AdmitDate
        FROM mydata.vwAllBedsAndCurrentOccupants 
        ORDER BY UnitName, RoomName, BedName
        '''

SAGELY2 = '''/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
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
	OR (LastStatus IN ('Expired', 'Discharged', 'Discharged RE') AND StartDate > DATEADD(day, -30, GETDATE() )  )
	) AS pse
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
ORDER BY Resident_Last, Resident_First, DOB

  '''