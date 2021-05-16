-- =============================================
-- Author:		Devin
-- Create date: 05/15/2021
-- Description:	Upsert for VueSelectItem
-- =============================================
CREATE PROCEDURE UpsertVueSelectItem
	@VueSelectItemId int,
	@ItemColumn nvarchar(255),
	@ValueColumn nvarchar(255),
	@TableName nvarchar(255),
	@WhereClause nvarchar(MAX),
	@IsActive bit
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM VueSelectItem WHERE VueSelectItemId = @VueSelectItemId)
	BEGIN
		SET IDENTITY_INSERT VueSelectItem ON

		INSERT INTO VueSelectItem (VueSelectItemId, ItemColumn, ValueColumn, TableName, WhereClause, IsActive)
		VALUES (@VueSelectItemId, @ItemColumn, @ValueColumn, @TableName, @WhereClause, @IsActive)

		SET IDENTITY_INSERT VueSelectItem OFF
	END
	ELSE
	BEGIN
		UPDATE
			VueSelectItem
		SET
			ItemColumn = @ItemColumn,
			ValueColumn = @ValueColumn,
			TableName = @TableName,
			WhereClause = @WhereClause,
			IsActive = @IsActive
		WHERE
			VueSelectItemId = @VueSelectItemId
	END
END