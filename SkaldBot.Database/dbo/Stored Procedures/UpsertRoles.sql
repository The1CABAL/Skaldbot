-- =============================================
-- Author:		Devin
-- Create date: 07/23/2020
-- Description:	Upsert for Roles Table
-- =============================================
CREATE PROCEDURE UpsertRoles
	-- Add the parameters for the stored procedure here
	@Id INT,
	@Role NVARCHAR(255),
	@RoleName NVARCHAR(255),
	@IsActive BIT
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM Roles WHERE Id = @Id)
	BEGIN
		INSERT INTO Roles (Id, [Role], RoleName, IsActive) VALUES (@Id, @Role, @RoleName, @IsActive)
	END
	ELSE
	BEGIN
		UPDATE Roles SET [Role] = @Role, RoleName = @RoleName, IsActive = @IsActive WHERE Id = @Id
	END
END