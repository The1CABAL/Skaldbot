CREATE TABLE [dbo].[Roles] (
    [Id]       INT            IDENTITY (1, 1) NOT NULL,
    [Role]     NVARCHAR (255) NOT NULL,
    [RoleName] NVARCHAR (255) NOT NULL,
    [IsActive] BIT            NOT NULL,
    CONSTRAINT [PK_Roles] PRIMARY KEY CLUSTERED ([Id] ASC)
);

