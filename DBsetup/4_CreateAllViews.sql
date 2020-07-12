CREATE VIEW mydata.vwPatientStayElementLatest AS
SELECT pse.*
FROM mydata.PatientStayElement AS pse
 JOIN (
	 SELECT PatientID, MAX(StartDate) AS StartDate
	 FROM mydata.PatientStayElement 
	 GROUP BY PatientID
	 ) AS last ON last.PatientID=pse.PatientID AND last.StartDate=pse.StartDate
	 
	 
CREATE VIEW mydata.vwAllBedsAndCurrentOccupants AS
 SELECT   bed.BedID
		, bed.RoomID
		, bed.UnitID
		, bed.FacilityID
		, bed.BuildingID
		, bed.UnitName
		, bed.RoomName
		, bed.BedName
		, stay.PatientID
		, stay.StartDate
		, stay.EndDate
		, stay.AdmitDate
		, stay.CensusType
		, stay.PayerType
		, stay.PayerID
		, stay.StartCensusID
		, stay.EndCensusID
		, stay.AdmitType
		, stay.AdmitSource
		, stay.BedHold
		, stay.VisitCount
		, stay.LastStatus
		, stay.LOCID
		, loc.Description [LevelOfCare]
		, pat.IsActive
		, pat.FirstName
		, pat.MiddleName
		, pat.LastName
		, pat.SSN
		, pat.AddressID
		, pat.DateOfBirth
		, pat.Sex
		, pat.AttendingPhysicianID
		, pat.RACECODE
		, pat.MARITALSTATUSCODE
		, pat.MedicareNumber
		, pat.MedicaidNumber
		, pat.PreferredName
		, pat.RELIGIONCODE
		, pat.MilitaryService
		, pat.MedicalRecordNumber
		, pat.OriginalAdmtDt
		, pat.CurrentAdmtDt
		, pat.CurrentReturnDt
		, pat.CensusStatus
		, pat.MedicareBNumber
		, pat.LanguageKey
 FROM mydata.FacilityUnitRoomBed AS bed
 LEFT JOIN mydata.vwPatientStayElementLatest AS stay ON  stay.BedID=bed.BedID AND stay.CensusType IN (1,2,5,6)
 LEFT JOIN mydata.Patient AS pat on pat.PatientID=stay.PatientID AND pat.CensusStatus='In House'
 LEFT JOIN mydata.Census_LevelOfCare AS loc on loc.LOCID = stay.LOCID and stay.FacilityID=loc.FacilityID 
  