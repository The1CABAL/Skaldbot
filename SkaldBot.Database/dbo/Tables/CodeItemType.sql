CREATE TABLE [dbo].[CodeItemType] (
    [Id]       INT            IDENTITY (1, 1) NOT NULL,
    [ItemType] NVARCHAR (255) NOT NULL,
    [IsActive] BIT            CONSTRAINT [DF_CodeItemType_IsActive] DEFAULT ((1)) NOT NULL,
    CONSTRAINT [PK_CodeItemType] PRIMARY KEY CLUSTERED ([Id] ASC)
);

