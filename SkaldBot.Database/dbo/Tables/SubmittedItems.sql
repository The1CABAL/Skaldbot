﻿CREATE TABLE [dbo].[SubmittedItems] (
    [Id]               INT              IDENTITY (1, 1) NOT NULL,
    [ItemTypeId]       INT              NOT NULL,
    [Title]            NVARCHAR (255)   NULL,
    [ItemText]         NVARCHAR (MAX)   NOT NULL,
    [ServerId]         BIGINT           NOT NULL,
    [DiscordUserId]    BIGINT           NOT NULL,
    [CreateDate]       DATETIME         NOT NULL,
    [IsApproved]       BIT              CONSTRAINT [DF_SubmittedItems_IsApproved] DEFAULT ((0)) NOT NULL,
    [IsReviewed]       BIT              CONSTRAINT [DF_SubmittedItems_IsReviewed] DEFAULT ((0)) NOT NULL,
    [ReviewedByUserId] UNIQUEIDENTIFIER NULL,
    [ReviewedDate]     DATETIME         NULL,
    CONSTRAINT [PK_SubmittedItems] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SubmittedItems_CodeItemType] FOREIGN KEY ([ItemTypeId]) REFERENCES [dbo].[CodeItemType] ([Id])
);









