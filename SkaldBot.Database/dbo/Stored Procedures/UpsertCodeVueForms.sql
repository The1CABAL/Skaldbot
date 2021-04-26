-- =============================================
-- Author:		Devin
-- Create date: 07/19/2020
-- Description:	Upsert for CodeVueForms
-- =============================================
CREATE PROCEDURE [dbo].[UpsertCodeVueForms]
	-- Add the parameters for the stored procedure here
	@FormKey nvarchar(255),
	@FormName nvarchar(255),
	@PageId int,
	@IsActive bit,
	@ShowFormName bit
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodeVueForms WHERE FormKey = @FormKey)
	BEGIN
		INSERT INTO CodeVueForms (FormKey, FormName, PageId, IsActive, ShowFormName) VALUES (@FormKey, @FormName, @PageId, @IsActive, @ShowFormName)
	END
	ELSE
	BEGIN
		UPDATE CodeVueForms SET FormName = @FormName, PageId = @PageId, IsActive = @IsActive, ShowFormName = @ShowFormName WHERE FormKey = @FormKey
	END
END