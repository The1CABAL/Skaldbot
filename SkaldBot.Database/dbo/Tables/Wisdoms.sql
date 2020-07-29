CREATE TABLE [dbo].[Wisdoms] (
    [Id]              INT            IDENTITY (1, 1) NOT NULL,
    [ServerId]        INT            NOT NULL,
    [Wisdom]          NVARCHAR (MAX) NOT NULL,
    [WasSubmitted]    BIT            CONSTRAINT [DF_Wisdoms_WasSubmitted] DEFAULT ((0)) NOT NULL,
    [SubmittedItemId] INT            NULL,
    [IsActive]        BIT            CONSTRAINT [DF_Wisdoms_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]      DATETIME       CONSTRAINT [DF_Wisdoms_UpdateDate] DEFAULT (getdate()) NULL,
    CONSTRAINT [PK_Wisdoms] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Wisdoms_SubmittedItems] FOREIGN KEY ([ServerId]) REFERENCES [dbo].[CodeServers] ([Id])
);



