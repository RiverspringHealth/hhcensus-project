USE [HHdev]
GO

/****** Object:  Table [dbo].[bedcheck]    Script Date: 02/11/2020 11:36:10 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[bedcheck](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[unit] [nvarchar](10) NOT NULL,
	[room] [nvarchar](6) NOT NULL,
	[bed] [nvarchar](5) NOT NULL,
	[mrn] [nvarchar](9) NULL,
	[patientID] [int] NULL,
	[lastname] [nvarchar](50) NULL,
	[firstname] [nvarchar](50) NULL,
	[CurrentAdmitDate] [datetime2](7) NULL,
	[CensusStatus] [nvarchar](30) NULL,
	[SweepTime] [datetime2](7) NOT NULL,
	[Obsolete] [int] NOT NULL,
	[gender] [nvarchar](1) NULL,
	[inbed] [nvarchar](6) NULL,
	[reason] [nvarchar](80) NULL,
	[updatedby] [nvarchar](80) NULL,
	[updatetime] [datetime2](7) NULL,
	[LevelOfCare] [nvarchar](20) NULL,
	[comment] [nvarchar](80) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

