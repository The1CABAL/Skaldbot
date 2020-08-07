IF NOT EXISTS(SELECT 1 FROM Accounts WHERE AccountId = 1)
BEGIN
	INSERT INTO Accounts (AccountName) VALUES ('SkaldBot Admin')
END