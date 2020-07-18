-- =============================================
-- Author:		Devin
-- Create date: 07/17/2020
-- Description:	Upsert for CodeSystems
-- =============================================
CREATE PROCEDURE UpsertCodeSystems
	@id int,
	@edsm_id nvarchar(max),
	@name nvarchar(max),
	@x decimal(10, 5),
	@y decimal(10, 5),
	@z decimal(10, 5),
	@population nvarchar(max),
	@is_populated nvarchar(max),
	@government_id nvarchar(max),
	@government nvarchar(max),
	@allegiance nvarchar(max),
	@security_id nvarchar(max),
	@security nvarchar(max),
	@primary_economy_id nvarchar(max),
	@primary_economy nvarchar(max),
	@power nvarchar(max),
	@power_state nvarchar(max),
	@power_state_id nvarchar(max),
	@needs_permit nvarchar(max),
	@updated_at nvarchar(max),
	@simbad_ref nvarchar(max),
	@controlling_minor_faction_id nvarchar(max),
	@controlling_minor_faction nvarchar(max),
	@reserve_type_id nvarchar(max),
	@reserve_type nvarchar(max),
	@ed_system_address nvarchar(max)
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodeSystems WHERE id = @id)
	BEGIN
		INSERT INTO CodeSystems (id, edsm_id, [name], x, y, z, [population], is_populated, government_id, government, allegiance, security_id, [security], primary_economy_id, primary_economy, [power], power_state, power_state_id, needs_permit, updated_at, simbad_ref, controlling_minor_faction_id, controlling_minor_faction, reserve_type_id, reserve_type, ed_system_address)
		VALUES (@id, @edsm_id, @name, @x, @y, @z, @population, @is_populated, @government_id, @government, @allegiance, @security_id, @security, @primary_economy_id, @primary_economy, @power, @power_state, @power_state_id, @needs_permit, @updated_at, @simbad_ref, @controlling_minor_faction_id, @controlling_minor_faction, @reserve_type_id, @reserve_type, @ed_system_address)
	END
	ELSE
	BEGIN
		UPDATE CodeSystems SET edsm_id = @edsm_id, [name] = @name, x = @x, y = @y, z = @z, [population] = @population, is_populated = @is_populated, government_id = @government_id, government = @government, allegiance = @allegiance, security_id = @security_id, [security] = @security, primary_economy_id = @primary_economy_id, primary_economy = primary_economy, [power] = @power, 
		power_state = @power_state, power_state_id = @power_state_id, needs_permit = @needs_permit, updated_at = @updated_at, simbad_ref = @simbad_ref, controlling_minor_faction_id = @controlling_minor_faction_id, controlling_minor_faction = @controlling_minor_faction, reserve_type_id = @reserve_type_id, reserve_type = @reserve_type, ed_system_address = @ed_system_address 
		WHERE id = @id
	END
END