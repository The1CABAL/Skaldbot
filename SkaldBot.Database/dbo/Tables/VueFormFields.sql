CREATE TABLE [dbo].[VueFormFields] (
    [Id]             INT            IDENTITY (1, 1) NOT NULL,
    [FormKey]        NVARCHAR (255) NOT NULL,
    [FieldSchema]    NVARCHAR (MAX) NOT NULL,
    [PageId]         INT            NOT NULL,
    [ActionLink]     NVARCHAR (255) NOT NULL,
    [IsActive]       BIT            CONSTRAINT [DF_VueForms_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]     DATETIME       NULL,
    [UpdateByUserId] INT            NULL,
    CONSTRAINT [PK_VueForms_1] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_CodePages_VueFormFields] FOREIGN KEY ([PageId]) REFERENCES [dbo].[CodePages] ([Id]) NOT FOR REPLICATION,
    CONSTRAINT [FK_VueFormFields_CodeVueForms] FOREIGN KEY ([FormKey]) REFERENCES [dbo].[CodeVueForms] ([FormKey])
);


GO
ALTER TABLE [dbo].[VueFormFields] NOCHECK CONSTRAINT [FK_CodePages_VueFormFields];



