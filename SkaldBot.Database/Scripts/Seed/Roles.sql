SET IDENTITY_INSERT [dbo].[Roles] ON
EXEC UpsertRoles 1, 'MasterAdmin', 'Master Admin', 1
EXEC UpsertRoles 2, 'Admin', 'Admin', 2
EXEC UpsertRoles 3, 'Public', 'Public User', 3
SET IDENTITY_INSERT [dbo].[Roles] OFF