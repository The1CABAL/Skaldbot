-- =============================================
-- Author:		Devin Walkup
-- Create date: 04/25/2021
-- Description:	Upsert for vue form fields
-- =============================================
CREATE PROCEDURE UpsertVueFormFields
	@FormKey NVARCHAR(255),
	@FieldSchema NVARCHAR(MAX),
	@ActionLink NVARCHAR(255),
	@IsActive BIT
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM VueFormFields WHERE FormKey = @FormKey)
		BEGIN
			INSERT INTO VueFormFields (FormKey, FieldSchema, ActionLink, IsActive) VALUES (@FormKey, @FieldSchema, @ActionLink, @IsActive)
		END
	ELSE
	BEGIN
		UPDATE VueFormFields SET FieldSchema = @FieldSchema, ActionLink = @ActionLink, IsActive = 1 WHERE FormKey = @FormKey
	END
END