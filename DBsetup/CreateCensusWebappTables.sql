CREATE TABLE [dbo].[NightlyBedCheck](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Unit] [nvarchar](50) NULL,
	[Room] [nvarchar](50) NULL,
	[ResidentNumber] [nvarchar](50) NULL,
	[ResidentName] [nvarchar](50) NULL,
	[Status] [nvarchar](50) NULL,
	[LevelOfCare] [nvarchar](50) NULL,
	[Gender] [nvarchar](50) NULL,
	[CurrentAdmitDate] [datetime] NULL,
	[Inbed] [nvarchar](50) NULL,
	[Reason] [varchar](300) NULL,
	[RepDate] [date] NULL,
	[Comments] [nvarchar](max) NULL,
	[UpdateByID] [int] NULL,
	[UpdateDatetime] [datetime] NULL,
	[CreateDatetime] [datetime] NULL,
	[UpdateByName] [varchar](100) NULL,
	[Obsolete] [int] NULL,
 CONSTRAINT [PK_PositiveCensusReport_MYI] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

CREATE TABLE [dbo].[CensusChangeLog](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[action] [nvarchar](50) NOT NULL,
	[firstname] [nvarchar](50) NOT NULL,
	[lastname] [nvarchar](50) NOT NULL,
	[eventtime] [datetime2](7) NULL,
	[oldbed] [nvarchar](10) NOT NULL,
	[newbed] [nvarchar](10) NOT NULL,
	[newloc] [nvarchar](20) NOT NULL,
	[oldloc] [nvarchar](20) NOT NULL,
	[admitfrom] [nvarchar](50) NOT NULL,
	[dischargeto] [nvarchar](50) NOT NULL,
	[user] [nvarchar](50) NOT NULL,
	[timestamp] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
