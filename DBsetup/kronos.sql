USE [CensusApps]
GO
CREATE VIEW mydata.vwInhousePatients AS
select psel.PatientID, psel.BedID, LastName, FirstName, pat.Sex [Gender], psel.AdmitDate, UnitName, RoomName, psel.StartCensusID
  from mydata.vwPatientStayElementLatest as psel
  --JOIN mydata.PatientCensus AS pc ON pc.CensusID=psel.EndCensusID
  --JOIN mydata.Census_Types AS ct ON ct.CensusType = pc.CensusType
  JOIN mydata.Patient as pat ON pat.PatientID=psel.PatientID
  JOIN mydata.FacilityUnitRoomBed AS bed on bed.BedID=psel.Bedid
  where LastStatus='In House'

  