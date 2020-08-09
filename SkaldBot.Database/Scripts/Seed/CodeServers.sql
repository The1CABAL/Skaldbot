BEGIN
SET IDENTITY_INSERT dbo.CodeServers ON

IF NOT EXISTS (SELECT * FROM CodeServers WHERE Id = 1)
	BEGIN
		INSERT INTO CodeServers (id, ServerId, Nickname, DailyWisdom) VALUES (1, '725880649356935192', 'Production', 1)
	END
ELSE
	BEGIN
		UPDATE CodeServers SET ServerId = '725880649356935192', Nickname = 'Production', DailyWisdom = 1 WHERE id = 1
	END

IF NOT EXISTS (SELECT * FROM CodeServers WHERE Id = 2)
	BEGIN
		INSERT INTO CodeServers (id, ServerId, Nickname, DailyWisdom) VALUES (2, '726640547019751458', 'Test', 1)
	END
ELSE
	BEGIN
		UPDATE CodeServers SET ServerId = '726640547019751458', Nickname = 'Test', DailyWisdom = 0 WHERE id = 2
	END

SET IDENTITY_INSERT dbo.CodeServers OFF
END