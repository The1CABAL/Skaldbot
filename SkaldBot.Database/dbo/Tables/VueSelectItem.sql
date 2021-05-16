CREATE TABLE [dbo].[VueSelectItem]
(
	[VueSelectItemId] INT NOT NULL PRIMARY KEY IDENTITY (1, 1), 
    [ItemColumn] NVARCHAR(255) NOT NULL, 
    [ValueColumn] NVARCHAR(255) NOT NULL, 
    [TableName] NVARCHAR(255) NOT NULL, 
    [WhereClause] NVARCHAR(MAX) NULL, 
    [IsActive] BIT NOT NULL DEFAULT 1, 
    [CreateDate] DATETIME NOT NULL DEFAULT getdate(),
)
