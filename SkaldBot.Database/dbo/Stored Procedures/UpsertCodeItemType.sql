-- =============================================
-- Author:		Devin
-- Create date: 07/20/2020
-- Description:	Upsert for CodeItemType
-- =============================================
CREATE PROCEDURE UpsertCodeItemType
	-- Add the parameters for the stored procedure here
	@Id int,
	@ItemType nvarchar(255),
	@IsActive bit
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodePages WHERE Id = @Id)
	BEGIN
		INSERT INTO CodeItemType(ItemType, IsActive) VALUES (@ItemType, @IsActive)
	END
	ELSE
	BEGIN
		UPDATE CodeItemType SET ItemType = @ItemType, IsActive = @IsActive WHERE Id = @Id
	END
END