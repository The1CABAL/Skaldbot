
BEGIN
SET IDENTITY_INSERT dbo.Wisdoms ON
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 1)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (1, 1, 'Shields grow back.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 2)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (2, 1, 'Gravity is heavy.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 3)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (3, 1, 'If you want to get out of going on a date, pull a spark plug out of your car and send a snap of the car not starting.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 4)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (4, 1, 'Space is hard.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 5)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (5, 1, 'You need to prospect to see things.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 6)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (6, 1, 'We are all egg.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 7)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (7, 1, 'Jormungandr in English is Jormungandr.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 8)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (8, 1, 'A jumo is approximately 6 jumps. Only a Diamondback Explorer is capable of a jumo.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 9)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (9, 1, 'Everything is either a banana or not a banana.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 10)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (10, 1, 'Driving is just reall slow teleportation.', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 11)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (11, 2, 'Test Wisdom One', 0, 1)
IF NOT EXISTS (SELECT * FROM Wisdoms WHERE Id = 12)
INSERT INTO Wisdoms (Id, ServerId, Wisdom, WasSubmitted, IsActive) VALUES (12, 2, 'Test Wisdom Two', 0, 1)
SET IDENTITY_INSERT dbo.Wisdoms OFF
END