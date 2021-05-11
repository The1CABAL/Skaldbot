BEGIN
SET IDENTITY_INSERT dbo.CodeServers ON

IF NOT EXISTS (SELECT * FROM CodeServers WHERE Id = 1)
	BEGIN
		INSERT INTO CodeServers (id, ServerId, Nickname, AccountId, DailyWisdom, WeeklyStory) VALUES (1, '725880649356935192', 'Production', 1, 1, 1)
	END

IF NOT EXISTS (SELECT * FROM CodeServers WHERE Id = 2)
	BEGIN
		INSERT INTO CodeServers (id, ServerId, Nickname, AccountId, DailyWisdom, WeeklyStory) VALUES (2, '726640547019751458', 'Test', 1, 1, 1)
	END

SET IDENTITY_INSERT dbo.CodeServers OFF
END
