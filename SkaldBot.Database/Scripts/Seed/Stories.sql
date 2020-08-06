
BEGIN
SET IDENTITY_INSERT dbo.Stories ON
IF NOT EXISTS (SELECT * FROM Stories WHERE Id = 1)
INSERT INTO Stories (Id, ServerId, Title, Story, WasSubmitted, IsActive) VALUES (1, 1, 'The Tragedy of The Gungnir', 'This is the story of the brave I.N.S. Gungnir. 
It is not a story you will hear often,  but the Gungnir died for this squadron. 
The Gungnir selfishly launched to earn several million credits for the poor unfortunate souls who are too weak to earn credits for themselves in any way other than mining. 
Yet despite the numerous foes who fell at the hands of her brave captain,  the Gungnir fell to a simple Fer De Lance who shall not be named. 
Though resurrected,  the Gungnir will be forever immortalized in the memories of the Jotun''s Angels. 
Gods speed to the Gungnir and her captain. o7', 0, 1)
IF NOT EXISTS (SELECT * FROM Stories WHERE Id = 2)
INSERT INTO Stories (Id, ServerId, Title, Story, WasSubmitted, IsActive) VALUES (2, 1, 'The Great Famine', 'Once,  after a full day of battle,  Our brave pilots of Jotun''s Angels heard of a system experiencing famine. 
Selflessly and for no personal gain,  our heroes flew 6 round trips filling their holds up to the brim with food cartidges.
They had stripped their glorious warships of the tools that gave them their combat abilities,  so that they could deliver the precious food faster.

This mission was not without adversity. Our heroes were beset by an evil man named James Draco who multiplied himself in a terrible attempt to foil the selfless actions of the pilots.
Finally,  the mission was complete and all our pilots had FOR SURE contributed evenly.
The station that needed the food was so grateful they awarded all our pilots 10 Million credits and some critical items needed for an engineering deal. But I assure you the pilots of Jotun''s Angels did not expect or even want this.', 0, 1)
IF NOT EXISTS (SELECT * FROM Stories WHERE Id = 3)
INSERT INTO Stories (Id, ServerId, Title, Story, WasSubmitted, IsActive) VALUES (3, 2, 'Test Story 01', 'This is one of two possible test stories.', 0, 1)
IF NOT EXISTS (SELECT * FROM Stories WHERE Id = 4)
INSERT INTO Stories (Id, ServerId, Title, Story, WasSubmitted, IsActive) VALUES (4, 2, 'Test Story 02', 'This is one of two possible test stories, the second in fact', 0, 1)
SET IDENTITY_INSERT dbo.Stories OFF
END