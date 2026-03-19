-- Users Table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Users]') AND type in (N'U'))
BEGIN
    CREATE TABLE Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        Username NVARCHAR(100) NOT NULL UNIQUE,
        PasswordHash NVARCHAR(256) NOT NULL,
        CreatedAt DATETIME DEFAULT GETDATE()
    );
END
GO

-- Categories Table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Categories]') AND type in (N'U'))
BEGIN
    CREATE TABLE Categories (
        CategoryID INT IDENTITY(1,1) PRIMARY KEY,
        CategoryName NVARCHAR(50) NOT NULL UNIQUE
    );
END
GO

-- Items Table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Items]') AND type in (N'U'))
BEGIN
    CREATE TABLE Items (
        ItemID INT IDENTITY(1,1) PRIMARY KEY,
        UserID INT NOT NULL,
        CategoryID INT NOT NULL,
        ItemName NVARCHAR(100) NOT NULL,
        Description NVARCHAR(255) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    );
END
GO

-- UserPatterns Table (Tracks Forget History)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[UserPatterns]') AND type in (N'U'))
BEGIN
    CREATE TABLE UserPatterns (
        PatternID INT IDENTITY(1,1) PRIMARY KEY,
        UserID INT NOT NULL,
        ItemID INT NOT NULL,
        LastRememberedDate DATETIME NULL,
        LastForgottenDate DATETIME NULL,
        ForgetCount INT DEFAULT 0,
        CurrentScore FLOAT DEFAULT 0.0,
        CHECK (LastForgottenDate IS NOT NULL OR LastRememberedDate IS NOT NULL),
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    );
END
GO

-- Insert Default Categories
IF NOT EXISTS (SELECT * FROM Categories WHERE CategoryName = 'Medicine')
    INSERT INTO Categories (CategoryName) VALUES ('Medicine');
IF NOT EXISTS (SELECT * FROM Categories WHERE CategoryName = 'Documents')
    INSERT INTO Categories (CategoryName) VALUES ('Documents');
IF NOT EXISTS (SELECT * FROM Categories WHERE CategoryName = 'Electronics')
    INSERT INTO Categories (CategoryName) VALUES ('Electronics');
IF NOT EXISTS (SELECT * FROM Categories WHERE CategoryName = 'Personal Items')
    INSERT INTO Categories (CategoryName) VALUES ('Personal Items');
GO


select * from Users;