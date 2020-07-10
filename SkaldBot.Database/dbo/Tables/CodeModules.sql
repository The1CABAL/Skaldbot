CREATE TABLE [dbo].[CodeModules] (
    [id]           INT            NOT NULL,
    [group_id]     INT            NOT NULL,
    [class]        NVARCHAR (MAX) NULL,
    [rating]       NVARCHAR (MAX) NULL,
    [price]        INT            NULL,
    [weapon_mode]  NVARCHAR (MAX) NULL,
    [missile_type] NVARCHAR (MAX) NULL,
    [name]         NVARCHAR (MAX) NULL,
    [belongs_to]   NVARCHAR (MAX) NULL,
    [ed_id]        NVARCHAR (MAX) NULL,
    [ed_symbol]    NVARCHAR (MAX) NULL,
    [game_context] NVARCHAR (MAX) NULL,
    [mass]         NVARCHAR (MAX) NULL,
    [ship]         NVARCHAR (MAX) NULL,
    [group]        NVARCHAR (MAX) NULL,
    CONSTRAINT [PK_CodeModules] PRIMARY KEY CLUSTERED ([group_id] ASC)
);

