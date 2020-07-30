CREATE TABLE [dbo].[UserRoles] (
    [UserId] UNIQUEIDENTIFIER NOT NULL,
    [RoleId] INT              NOT NULL,
    CONSTRAINT [FK_UserRoles_Roles] FOREIGN KEY ([RoleId]) REFERENCES [dbo].[Roles] ([Id]),
    CONSTRAINT [FK_UserRoles_Users] FOREIGN KEY ([UserId]) REFERENCES [dbo].[Users] ([Id])
);

