select patient.PatientID, LastName, FirstName, CensusStatus, MedicareNumber, discharged.DateTime AS [DischargedDate]
from mydata.Patient AS patient
JOIN (
	SELECT lastevent.PatientID, lastEvent.DateTime [DateTime]
	FROM (
		SELECT PatientID, MAX(DateTime) [DateTime]
		FROM mydata.PatientCensus 
		GROUP BY PatientID
		) as lastevent 
	JOIN (
			SELECT PatientID, CensusType, DateTime
			FROM mydata.PatientCensus 
			WHERE CensusType IN (3,4) -- DC or death
			AND  DateTime  >= DATEADD(day, -30, GETDATE() )
			) as dc on dc.PatientID =lastevent.PatientID 
				AND dc.DateTime=lastevent.DateTime
	) AS discharged ON discharged.PatientID=patient.PatientID
UNION (
	SELECT  PatientID, LastName, FirstName, CensusStatus, MedicareNumber , NULL [DateTime]
	FROM  mydata.Patient 
	WHERE CensusStatus='In House'
	) 
order by CensusStatus  -- optional for debugging
