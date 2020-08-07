CREATE TABLE [dbo].[CodeServers] (
    [Id]          INT            IDENTITY (1, 1) NOT NULL,
    [ServerId]    BIGINT         NOT NULL,
    [Nickname]    NVARCHAR (255) NULL,
    [AccountId]   BIGINT         NULL,
    [DailyWisdom] BIT            CONSTRAINT [DF_CodeServers_DailyWisdom] DEFAULT ((1)) NOT NULL,
    [UpdateDate]  DATETIME       CONSTRAINT [DF_CodeServers_UpdateDate] DEFAULT (getdate()) NULL,
    CONSTRAINT [PK_CodeServers] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_CodeServers_Accounts] FOREIGN KEY ([AccountId]) REFERENCES [dbo].[Accounts] ([AccountId])
);









