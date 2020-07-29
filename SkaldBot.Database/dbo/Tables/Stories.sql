CREATE TABLE [dbo].[Stories] (
    [Id]              INT            IDENTITY (1, 1) NOT NULL,
    [ServerId]        INT            NOT NULL,
    [Title]           NVARCHAR (255) NOT NULL,
    [Story]           NVARCHAR (MAX) NOT NULL,
    [WasSubmitted]    BIT            CONSTRAINT [DF_Stories_WasSubmitted] DEFAULT ((0)) NOT NULL,
    [SubmittedItemId] INT            NULL,
    [IsActive]        BIT            CONSTRAINT [DF_Stories_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]      DATETIME       CONSTRAINT [DF_Stories_UpdateDate] DEFAULT (getdate()) NULL,
    CONSTRAINT [PK_Stories] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Stories_SubmittedItems] FOREIGN KEY ([ServerId]) REFERENCES [dbo].[CodeServers] ([Id])
);





