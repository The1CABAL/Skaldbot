CREATE TABLE [dbo].[SubmittedItems] (
    [Id]               INT            IDENTITY (1, 1) NOT NULL,
    [ItemTypeId]       INT            NOT NULL,
    [Title]            NVARCHAR (255) NOT NULL,
    [ItemText]         NVARCHAR (MAX) NOT NULL,
    [SubmitterEmail]   NVARCHAR (255) NOT NULL,
    [CreateDate]       DATETIME       NOT NULL,
    [IsApproved]       BIT            CONSTRAINT [DF_SubmittedItems_IsApproved] DEFAULT ((0)) NOT NULL,
    [ApprovedByUserId] INT            NULL,
    [ApprovedDate]     DATETIME       NULL,
    CONSTRAINT [PK_SubmittedItems] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SubmittedItems_CodeItemType] FOREIGN KEY ([ItemTypeId]) REFERENCES [dbo].[CodeItemType] ([Id])
);

