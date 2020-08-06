CREATE TABLE [dbo].[Users] (
    [Id]            UNIQUEIDENTIFIER CONSTRAINT [DF_Table_1_id] DEFAULT (newid()) NOT NULL,
    [AccountId]     BIGINT           NULL,
    [DiscordUserId] BIGINT           NULL,
    [Username]      NVARCHAR (255)   NOT NULL,
    [FirstName]     NVARCHAR (255)   NOT NULL,
    [LastName]      NVARCHAR (255)   NOT NULL,
    [PasswordHash]  NVARCHAR (MAX)   NOT NULL,
    [Email]         NVARCHAR (128)   NULL,
    [IsLocked]      BIT              CONSTRAINT [DF_Users_IsLocked] DEFAULT ((0)) NOT NULL,
    [IsActive]      BIT              CONSTRAINT [DF_Users_IsActive] DEFAULT ((1)) NOT NULL,
    [CreateDate]    DATETIME         NULL,
    CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Users_Accounts] FOREIGN KEY ([AccountId]) REFERENCES [dbo].[Accounts] ([AccountId])
);









