CREATE TABLE [dbo].[Wisdoms] (
    [Id]              INT            IDENTITY (1, 1) NOT NULL,
    [Title]           NVARCHAR (255) NOT NULL,
    [Wisdom]          NVARCHAR (MAX) NOT NULL,
    [WasSubmitted]    BIT            CONSTRAINT [DF_Wisdoms_WasSubmitted] DEFAULT ((0)) NOT NULL,
    [SubmittedItemId] INT            NULL,
    [IsActive]        BIT            CONSTRAINT [DF_Wisdoms_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]      DATETIME       NULL,
    CONSTRAINT [PK_Wisdoms] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Wisdoms_SubmittedItems] FOREIGN KEY ([SubmittedItemId]) REFERENCES [dbo].[SubmittedItems] ([Id])
);

