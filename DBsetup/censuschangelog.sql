USE [HHdev]
GO

/****** Object:  Table [dbo].[webapp_censuschangelog]    Script Date: 02/11/2020 11:35:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[webapp_censuschangelog](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[action] [nvarchar](50) NOT NULL,
	[firstname] [nvarchar](50) NOT NULL,
	[lastname] [nvarchar](50) NOT NULL,
	[eventtime] [datetime] NULL,
	[oldbed] [nvarchar](10) NULL,
	[newbed] [nvarchar](10) NULL,
	[newloc] [nvarchar](20) NULL,
	[oldloc] [nvarchar](20) NULL,
	[admitfrom] [nvarchar](50) NULL,
	[dischargeto] [nvarchar](50) NULL,
	[user] [nvarchar](50) NULL,
	[timestamp] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

