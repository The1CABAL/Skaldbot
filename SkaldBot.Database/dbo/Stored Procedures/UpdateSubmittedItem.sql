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
	DECLARE @ServerId BIGINT = (SELECT ServerId FROM SubmittedItems WHERE Id = @Id)
	DECLARE @ServerExists BIT = 0
	DECLARE @Date DATETIMEOFFSET = GETDATE()

	IF NOT EXISTS(SELECT 1 FROM CodeServers WHERE ServerId = @ServerId)
	BEGIN
		SET @ServerExists = 0
	END
	ELSE
	BEGIN
		SET @ServerExists = 1
	END

	IF @IsApproved = 0
	BEGIN
		UPDATE SubmittedItems SET IsReviewed = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id
	END
	ELSE
	BEGIN
		IF @ServerExists = 0
		BEGIN
			INSERT INTO CodeServers (ServerId, UpdateDate) VALUES (@ServerId, @Date)
			
		END

		SET @ServerId = (SELECT Id FROM CodeServers WHERE ServerId = @ServerId)

		IF @ItemTypeId = 1 --Story
		BEGIN
			
			UPDATE SubmittedItems SET IsReviewed = 1, IsApproved = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id

			INSERT INTO Stories (Title, Story, WasSubmitted, ServerId, SubmittedItemId, UpdateDate)
			VALUES (
				(SELECT Title FROM SubmittedItems WHERE Id = @Id), 
				(SELECT ItemText FROM SubmittedItems WHERE Id = @Id), 
				1,
				@ServerId,
				@Id, 
				@Date
			)
		END
		IF @ItemTypeId = 2 --Wisdom
		BEGIN
			UPDATE SubmittedItems SET IsReviewed = 1, IsApproved = 1, ReviewedByUserId = @UserId, ReviewedDate = @Date WHERE Id = @Id

			INSERT INTO Wisdoms (Wisdom, WasSubmitted, ServerId, SubmittedItemId, UpdateDate)
			VALUES ( 
				(SELECT ItemText FROM SubmittedItems WHERE Id = @Id), 
				1, 
				@ServerId,
				@Id, 
				@Date
			)
		END
	END
END