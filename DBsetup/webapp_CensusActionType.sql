USE [HHdev]
GO

/****** Object:  Table [dbo].[webapp_CensusActionType]    Script Date: 02/11/2020 11:34:05 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[webapp_CensusActionType](
	[Id] [nvarchar](10) NOT NULL,
	[Description] [nvarchar](80) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

