CREATE TABLE [dbo].[HelpDocumentation] (
    [HelpContentKey] NVARCHAR (255)   NOT NULL,
    [HelpTitle]      NVARCHAR (255)   NOT NULL,
    [HelpContent]    NVARCHAR (MAX)   NOT NULL,
    [IsActive]       BIT              CONSTRAINT [DF_HelpDocumentation_IsActive] DEFAULT ((1)) NOT NULL,
    [UpdateDate]     DATETIME         CONSTRAINT [DF_HelpDocumentation_UpdateDate] DEFAULT (getdate()) NULL,
    [UpdateByUserId] UNIQUEIDENTIFIER NULL,
    CONSTRAINT [FK_HelpDocumentation_Users] FOREIGN KEY ([UpdateByUserId]) REFERENCES [dbo].[Users] ([Id])
);

