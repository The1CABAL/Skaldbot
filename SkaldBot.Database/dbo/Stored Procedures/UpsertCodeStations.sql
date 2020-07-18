-- =============================================
-- Author:		Devin
-- Create date: 07-17-2020
-- Description:	Upsert for Code Stations
-- =============================================
CREATE PROCEDURE [dbo].[UpsertCodeStations]
	@id								int,
	@name							nvarchar(max),
	@system_id						nvarchar(max),
	@updated_at						nvarchar(max),
	@max_landing_pad				nvarchar(max),
	@distance_to_star				nvarchar(max),
	@government_id					nvarchar(max),
	@government						nvarchar(max),
	@allegiance_id					nvarchar(max),
	@allegiance						nvarchar(max),
	@states							nvarchar(max),
	@type_id						nvarchar(max),
	@type							nvarchar(max),
	@has_blackmarket				nvarchar(max),
	@has_market						nvarchar(max),
	@has_refuel						nvarchar(max),
	@has_repair						nvarchar(max),
	@has_rearm						nvarchar(max),
	@has_outfitting					nvarchar(max),
	@has_shipyard					nvarchar(max),
	@has_docking					nvarchar(max),
	@has_commodities				nvarchar(max),
	@import_commodities				nvarchar(max),
	@export_commodities				nvarchar(max),
	@prohibited_commodities			nvarchar(max),
	@economies						nvarchar(max),
	@shipyard_updated_at			nvarchar(max),
	@outfitting_updated_at			nvarchar(max),
	@market_updated_at				nvarchar(max),
	@is_planetary					nvarchar(max),
	@selling_ships					nvarchar(max),
	@selling_modules				nvarchar(max),
	@settlement_size_id				nvarchar(max),
	@settlement_size				nvarchar(max),
	@settlement_security_id			nvarchar(max),
	@settlement_security			nvarchar(max),
	@body_id						nvarchar(max),
	@controlling_minor_faction_id	nvarchar(max),
	@ed_market_id					nvarchar(max)
AS
BEGIN
	IF NOT EXISTS(SELECT 1 FROM CodeStations WHERE id = @id)
	BEGIN
		INSERT INTO CodeStations (id, [name], system_id, updated_at, max_landing_pad, distance_to_star, government_id, government, allegiance_id, allegiance, states, [type_id], [type], has_blackmarket, has_market, has_refuel, has_repair, has_rearm, has_outfitting, has_shipyard, has_docking, has_commodities, import_commodities, export_commodities,	prohibited_commodities, economies, shipyard_updated_at, outfitting_updated_at, market_updated_at, is_planetary, selling_ships, selling_modules, settlement_size_id, settlement_size, settlement_security_id, settlement_security, body_id, controlling_minor_faction_id, ed_market_id)
		VALUES (@id, @name,	@system_id,	@updated_at, @max_landing_pad, @distance_to_star, @government_id, @government, @allegiance_id, @allegiance,	@states, @type_id, @type, @has_blackmarket, @has_market, @has_refuel, @has_repair, @has_rearm, @has_outfitting, @has_shipyard, @has_docking, @has_commodities, @import_commodities, @export_commodities,	@prohibited_commodities, @economies, @shipyard_updated_at, @outfitting_updated_at, @market_updated_at, @is_planetary, @selling_ships, @selling_modules, @settlement_size_id, @settlement_size, @settlement_security_id,	@settlement_security, @body_id,	@controlling_minor_faction_id, @ed_market_id)
	END
	ELSE
	BEGIN
		UPDATE CodeStations SET [name] = @name, system_id = @system_id, updated_at = @updated_at, max_landing_pad = @max_landing_pad, distance_to_star = @distance_to_star, government_id = @government_id, government = @government, allegiance_id = @allegiance_id, allegiance = @allegiance, states = @states, [type_id] = @type_id, [type] = @type, has_blackmarket = @has_blackmarket, has_market = @has_market, has_refuel = @has_refuel, has_repair = @has_repair, has_rearm = @has_rearm, has_outfitting = @has_outfitting, has_shipyard = @has_shipyard, has_docking = @has_docking, has_commodities = @has_commodities, 
		import_commodities = @import_commodities, export_commodities = @export_commodities, prohibited_commodities = @prohibited_commodities, economies = @economies, shipyard_updated_at = @shipyard_updated_at, outfitting_updated_at = @outfitting_updated_at, market_updated_at = @market_updated_at, is_planetary = @is_planetary, selling_ships = @selling_ships, settlement_size_id = @settlement_size_id, settlement_size = @settlement_size, settlement_security_id = @settlement_security_id, settlement_security = @settlement_security, body_id = @body_id, controlling_minor_faction_id = @controlling_minor_faction_id, ed_market_id = @ed_market_id WHERE id = @id
	END
END