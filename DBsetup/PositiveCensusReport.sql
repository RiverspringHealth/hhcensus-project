USE [HHdev]
GO

/****** Object:  Table [dbo].[PositiveCensusReport]    Script Date: 02/11/2020 11:35:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[PositiveCensusReport](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[PositiveCensusReport] ADD  CONSTRAINT [DF_PositiveCensusReport_create_dt]  DEFAULT (getdate()) FOR [CreateDatetime]
GO

ALTER TABLE [dbo].[PositiveCensusReport] ADD  DEFAULT ((1)) FOR [Obsolete]
GO

