-- =============================================
-- Author:		Devin
-- Create date: 07-17-2020
-- Description:	Upsert for Code Modules
-- =============================================
CREATE PROCEDURE UpsertCodeModules 
	-- Column Parameters
	@id int,
	@group_id int,
	@class nvarchar(max),
	@rating nvarchar(max),
	@price nvarchar(max),
	@weapon_mode nvarchar(max),
	@missile_type nvarchar(max),
	@name nvarchar(max),
	@belongs_to nvarchar(max),
	@ed_id nvarchar(max),
	@ed_symbol nvarchar(max),
	@game_context nvarchar(max),
	@mass nvarchar(max),
	@ship nvarchar(max),
	@group nvarchar(max),
	@game_context_id nvarchar(max),
	@dps nvarchar(max),
	@power nvarchar(max),
	@damage nvarchar(max),
	@ammo nvarchar(max),
	@range_km nvarchar(max),
	@efficiency nvarchar(max),
	@power_produced nvarchar(max),
	@duration nvarchar(max),
	@cells nvarchar(max),
	@recharge_rating nvarchar(max),
	@capacity nvarchar(max),
	@count nvarchar(max),
	@rate nvarchar(max),
	@bins nvarchar(max),
	@additional_armour nvarchar(max),
	@vehicle_count nvarchar(max)
AS
BEGIN
    --Check if record exists, if it doesn't then insert the record else update it
	IF NOT EXISTS(SELECT 1 FROM CodeModules WHERE id = @id)
	BEGIN
		INSERT INTO CodeModules (id, group_id, class, rating, price, weapon_mode, missile_type, [name], belongs_to, ed_id, ed_symbol, game_context, mass, ship, [group], game_context_id, dps, [power], damage, ammo, range_km, efficiency, power_produced, duration, cells, recharge_rating, capacity, [count], rate, bins, additional_armour, vehicle_count)
		VALUES (@id, @group_id, @class, @rating, @price, @weapon_mode, @missile_type, @name, @belongs_to, @ed_id, @ed_symbol, @game_context, @mass, @ship, @group, @game_context_id, @dps, @power, @damage, @ammo, @range_km, @efficiency, @power_produced, @duration, @cells, @recharge_rating, @capacity, @count, @rate, @bins, @additional_armour, @vehicle_count)
	END
	ELSE
	BEGIN
		UPDATE CodeModules SET group_id = @group_id, class = @class, rating = @rating, price = @price, weapon_mode = @weapon_mode, missile_type = @missile_type, [name] = @name, belongs_to = @belongs_to, ed_id = @ed_id, ed_symbol = @ed_symbol, game_context = @game_context, mass = @mass, ship = @ship, [group] = @group, game_context_id = @game_context_id, dps = @dps, [power] = @power, 
		damage = @damage, ammo = @ammo, range_km = @range_km, efficiency = @efficiency, power_produced = @power_produced, duration = @duration, cells = @cells, recharge_rating = @recharge_rating, capacity = @capacity, [count] = @count, rate = @rate, bins = @bins, additional_armour = @additional_armour, vehicle_count = @vehicle_count
		WHERE id = @id
	END
END