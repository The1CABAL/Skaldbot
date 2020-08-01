-- =============================================
-- Author:		Devin
-- Create date: 08/01/2020
-- Description:	Upsert for help documentation
-- =============================================
CREATE PROCEDURE UpsertHelpDocumentation
	-- Add the parameters for the stored procedure here
	@HelpContentKey NVARCHAR(255),
	@HelpTitle NVARCHAR(255),
	@HelpContent NVARCHAR(MAX),
	@IsActive BIT
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    IF NOT EXISTS(SELECT 1 FROM HelpDocumentation WHERE HelpContentKey = @HelpContentKey)
	BEGIN
		INSERT INTO HelpDocumentation (HelpContentKey, HelpTitle, HelpContent, IsActive) VALUES (@HelpContentKey, @HelpTitle, @HelpContent, @IsActive)
	END
	ELSE
	BEGIN
		UPDATE HelpDocumentation SET HelpTitle = @HelpTitle, HelpContent = @HelpContent, IsActive = @IsActive WHERE HelpContentKey = @HelpContentKey
	END
END