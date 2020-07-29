-- =============================================
-- Author:		Devin
-- Create date: 07/26/2020
-- Description:	Procedure to update a submitted item to approved or not approved
-- =============================================
CREATE PROCEDURE [dbo].[UpdateSubmittedItem]
	-- Add the parameters for the stored procedure here
	@IsApproved INT, 
	@Id INT,
	@UserId UNIQUEIDENTIFIER
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @ItemTypeId INT = (SELECT ItemTypeId FROM SubmittedItems WHERE Id = @Id)
	DECLARE @Date DATETIMEOFFSET = GETDATE()

	IF @IsApproved = 0
	BEGIN
		UPDATE SubmittedItems SET IsReviewed = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id
	END
	ELSE
	BEGIN
		IF @ItemTypeId = 1 --Story
		BEGIN
			
			UPDATE SubmittedItems SET IsReviewed = 1, IsApproved = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id

			INSERT INTO Stories (Title, Story, WasSubmitted, SubmittedItemId, UpdateDate)
			VALUES (
				(SELECT Title FROM SubmittedItems WHERE Id = @Id), 
				(SELECT ItemText FROM SubmittedItems WHERE Id = @Id), 
				1, 
				@Id, 
				@Date
			)
		END
		IF @ItemTypeId = 2 --Wisdom
		BEGIN
			UPDATE SubmittedItems SET IsReviewed = 1, IsApproved = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id

			INSERT INTO Wisdoms (Wisdom, WasSubmitted, SubmittedItemId, UpdateDate)
			VALUES ( 
				(SELECT ItemText FROM SubmittedItems WHERE Id = @Id), 
				1, 
				@Id, 
				@Date
			)
		END
	END
END