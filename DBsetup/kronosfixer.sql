DECLARE @testtime DateTime2(7) = '6/1/2021 6:00am'
--DECLARE @EndOfDays SMALLDateTime = '3142-12-31 11:59pm'
DECLARE @stays TABLE  (
	PatientID Integer NOT NULL PRIMARY KEY,
	TestDate DateTime2(7) NOT NULL,
	AdmitDate DateTime2(7) NOT NULL,
	DischargeDate DateTime2(7),
	InfoDate DateTime2(7),
	LastDate DateTime2(7)

	
);


INSERT INTO @stays (PatientID, Testdate, AdmitDate, DischargeDate, InfoDate)
SELECT admit.PatientID, @testtime, admit.DateTime [AdmitDate], discharge.DateTime [DischargeDate], info.DateTime--, NULL, NULL
FROM (
	SELECT PatientID, MAX(DateTime) [DateTime]
	FROM mydata.PatientCensus
	WHERE CensusType IN (1,5,6) 
	AND DateTime <= @testtime
	GROUP BY PatientID
	) as admit



LEFT JOIN (
	SELECT PatientID, MAX(DateTime) [DateTime]
	FROM mydata.PatientCensus
	WHERE CensusType IN (3,4) 
	AND DateTime <= @testtime
	GROUP BY PatientID
	) as discharge ON admit.PatientID=discharge.patientID
LEFT JOIN (
	SELECT PatientID, MAX(DateTime) [DateTime]
	FROM mydata.PatientCensus 
	WHERE CensusType = 2 
	AND DateTime <=  @testtime
	GROUP BY PatientID
	) as info ON admit.PatientID=info.patientID


DELETE FROM @Stays WHERE DischargeDate IS NOT NULL AND DischargeDate <= AdmitDate

UPDATE @stays
	SET InfoDate = NULL 
FROM @stays 
WHERE InfoDate IS NOT NULL AND (infoDate > DischargeDate OR InfoDate<=AdmitDate)


select MAX(DischargeDate) from @stays

select * from @stays order by DischargeDate desc