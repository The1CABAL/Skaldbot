CREATE TABLE [dbo].[CodePages] (
    [Id]       INT            IDENTITY (1, 1) NOT NULL,
    [PageName] NVARCHAR (255) NOT NULL,
    [IsActive] BIT            CONSTRAINT [DF_CodePages_IsActive] DEFAULT ((1)) NOT NULL,
    CONSTRAINT [PK_CodePages] PRIMARY KEY CLUSTERED ([Id] ASC)
);

