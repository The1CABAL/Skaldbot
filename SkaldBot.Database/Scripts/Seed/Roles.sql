SET IDENTITY_INSERT [dbo].[Roles] ON
EXEC UpsertRoles 1, 'MasterAdmin', 'Master Admin', 1
EXEC UpsertRoles 2, 'Admin', 'Admin', 1
EXEC UpsertRoles 3, 'ClientAdmin', 'Client Administrator', 1
EXEC UpsertRoles 4, 'ClientUser', 'Client User', 1
SET IDENTITY_INSERT [dbo].[Roles] OFF