-- =============================================
-- Author:		Devin
-- Create date: 07/20/2020
-- Description:	Upsert for CodePages
-- =============================================
CREATE PROCEDURE UpsertCodePages
	-- Add the parameters for the stored procedure here
	@Id int,
	@PageName nvarchar(255),
	@IsActive bit
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodePages WHERE Id = @Id)
	BEGIN
		INSERT INTO CodePages (PageName, IsActive) VALUES (@PageName, @IsActive)
	END
	ELSE
	BEGIN
		UPDATE CodePages SET PageName = @PageName, IsActive = @IsActive WHERE Id = @Id
	END
END