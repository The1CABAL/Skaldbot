CREATE TABLE [dbo].[Stories] (
    [Id]              INT            NOT NULL,
    [Title]           NVARCHAR (255) NOT NULL,
    [Story]           NVARCHAR (MAX) NOT NULL,
    [WasSubmitted]    BIT            CONSTRAINT [DF_Stories_WasSubmitted] DEFAULT ((0)) NOT NULL,
    [SubmittedItemId] INT            NULL,
    [IsActive]        BIT            CONSTRAINT [DF_Stories_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]      DATETIME       NULL,
    CONSTRAINT [PK_Stories] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Stories_SubmittedItems] FOREIGN KEY ([SubmittedItemId]) REFERENCES [dbo].[SubmittedItems] ([Id])
);

