INHOUSE_PATIENTS = '''
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
	inhouse.MedicalRecordNumber [Unique Patient ID]
	,'' 						[Chart Number]
	, inhouse.FirstName 		[First Name]  
	,'' 						[Middle Initial]
	, inhouse.LastName 			[Last Name]
	, CASE  inhouse.Gender 
		WHEN 'M' THEN 'Male'
		ELSE 'Female'
	END							[Gender]
	, FORMAT( pat.DateOfBirth, 'MM/dd/yyyy') [Date of Birth]
	, CONCAT(bed.UnitName,'-',bed.RoomName, '-', bed.BedName) [Address]
	, '5901 Palisade Avenue'	[Address (cont)]
	,'10471' 					[Zip Code]
	,'' 						[Zip Code Extention]
	,'Riverdale' 				[City]
	,'NY' 						[State Abbreviation]
	,'' 						[Email Address]
	,'718-581-1000' 			[Home Phone Number]  
	,'' 						[Cell Phone Number]
	,'' 						[Work Phone Number]
	,'' 						[Other Phone Number]

  FROM [mydata].[vwPatientInhouse] AS inhouse
  LEFT JOIN [mydata].Patient AS pat ON pat.PatientID=inhouse.PatientID
  JOIN mydata.FacilityUnitRoomBed AS bed ON bed.BedID=inhouse.BedID
  Order BY pat.LastName, pat.FirstName
'''

PAYERS = '''
select fp.PayerID			[Unique Payer ID]
	 , fp.Name 				[Payer Name]
--	 , pt.Payer 			[PayerTypeName]
	 , NULL 				[Payer Address]  --address required only for paper invoices, skip until other resolved.
	 , NULL 				[Payer Address 2]
	 , NULL 				[Payer Zip Code]
	 , NULL 				[Payer Zip Code Extension]
	 , NULL 				[Payer City]
	 , NULL 				[Payor State Code]
     , NULL   [Electronic Payer ID]
     , NULL   [ERA Electronic ID]
     , NULL   [UBO4 ERA Electronic ID]
     , NULL   [UBO4 Claim Electronic ID]
     , NULL   [Eligibility Electronic ID]
     , NULL   [Type of Claim]
     , NULL   [Code - Type of claim]
     , NULL   [Health Insurance Type Name]
     , NULL   [Health Insurance Type Code]
     , NULL   [Primary Filing Method]
     , NULL   [Primary Filing Method Code]
     , NULL   [Secondary Filing Method]
     , NULL   [Secondary Filing Method Code]
--	, fac.Name
FROM mydata.FacilityPayers fp
--LEFT JOIN mydata.AR_PayerType pt ON pt.PayerType=fp.PayerType
--LEFT JOIN mydata.Facility AS fac on fac.FacilityID=fp.FacilityID
--LEFT JOIN mydata.AR_PayerGroup AS pg on pg.PayerGroupID = fp.PayerGroupID
ORDER BY fp.Name
'''

CASES = '''
	SELECT 
	 	 NULL   [Unique Case ID]
        ,pat.MedicalRecordNumber   [Unique Patient ID]
        ,NULL   [Case Name]
        ,NULL   [Case Type code]
        ,NULL   [Case Type Description]
        ,p1.PayerID   [Unique Payer ID]
        ,NULL   [Case Priority Code]
        ,NULL   [Case Priority Name]
        ,p1.PolicyNum   [Policy Number]
        ,NULL   [Group Number]
        ,NULL   [Group Name]
        ,FORMAT(p2.BeginDate, 'MM/dd/yyyy')    [Insurance Effective Start Date]
        ,FORMAT(p1.EndDate, 'MM/dd/yyyy')   [Insurance Effective End Date]
        ,p2.PayerID   [Unique Payer ID]
        ,NULL   [Case Priority Code]
        ,NULL   [Case Priority Name]
        ,p2.PolicyNum   [Policy Number]
        ,NULL   [Group Number]
        ,NULL   [Group Name]
        ,FORMAT(p2.BeginDate, 'MM/dd/yyyy')   [Insurance Effective Start Date]
        ,FORMAT(p2.EndDate, 'MM/dd/yyyy')   [Insurance Effecive End Date]
	FROM mydata.vwPatientInhouse AS pat
	LEFT JOIN(
			SELECT PayerID,'P' [PriorityCode], 'Priority' [PriorityName], pt.Payer [PayerType], ID_Number [PolicyNum], BeginDate, EndDate, Patient_PayerID, PatientID, Sequence
				, ROW_NUMBER() OVER(PARTITION BY PatientID  ORDER BY Sequence )     AS rk
			FROM mydata.AR_Patient_Payer as pp
			LEFT JOIN mydata.AR_PayerType AS pt ON pt.PayerType=pp.PayerType
			WHERE BeginDate <= GETDATE() AND COALESCE(EndDate, GETDATE()) >= GETDATE()
		  ) AS p1 ON p1.PatientID=pat.PatientID AND p1.rk=1
	LEFT JOIN(
			SELECT PayerID,'S' [PriorityCode], 'Secondary' [PriorityName], pt.Payer [PayerType], ID_Number [PolicyNum], BeginDate, EndDate, Patient_PayerID, PatientID, Sequence
				, ROW_NUMBER() OVER(PARTITION BY PatientID  ORDER BY Sequence )     AS rk
			FROM mydata.AR_Patient_Payer as pp
			LEFT JOIN mydata.AR_PayerType AS pt ON pt.PayerType=pp.PayerType
			WHERE BeginDate <= GETDATE() AND COALESCE(EndDate, GETDATE()) >= GETDATE()
		  ) AS p2 ON p2.PatientID=pat.PatientID AND p2.rk=2
	ORDER BY pat.LastName, pat.FirstName

'''