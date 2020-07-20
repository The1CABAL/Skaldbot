-- =============================================
-- Author:		Devin
-- Create date: 07/19/2020
-- Description:	Upsert for CodeVueForms
-- =============================================
CREATE PROCEDURE UpsertCodeVueForms
	-- Add the parameters for the stored procedure here
	@FormKey nvarchar(255),
	@FormName nvarchar(255),
	@isActive bit
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodeVueForms WHERE FormKey = @FormKey)
	BEGIN
		INSERT INTO CodeVueForms (FormKey, FormName, IsActive) VALUES (@FormKey, @FormName, @isActive)
	END
	ELSE
	BEGIN
		UPDATE CodeVueForms SET FormName = @FormName, IsActive = @isActive WHERE FormKey = @FormKey
	END
END