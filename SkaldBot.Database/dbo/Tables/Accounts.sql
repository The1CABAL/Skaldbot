CREATE TABLE [dbo].[Accounts] (
    [AccountId]   BIGINT         IDENTITY (1, 1) NOT NULL,
    [AccountName] NVARCHAR (255) NOT NULL,
    [CreateDate]  DATETIME       CONSTRAINT [DF_Accounts_CreateDate] DEFAULT (getdate()) NOT NULL,
    [IsActive]    BIT            CONSTRAINT [DF_Accounts_IsActive] DEFAULT ((1)) NOT NULL,
    CONSTRAINT [PK_Accounts] PRIMARY KEY CLUSTERED ([AccountId] ASC)
);

