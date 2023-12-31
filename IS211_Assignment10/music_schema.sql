
CREATE TABLE IF NOT EXISTS Artists (
    ArtistId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Albums (
    AlbumId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    ArtistId INTEGER,
    FOREIGN KEY (ArtistId) REFERENCES Artists (ArtistId)
);

CREATE TABLE IF NOT EXISTS Songs (
    SongId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    AlbumId INTEGER,
    TrackNumber INTEGER NOT NULL,
    LengthSeconds INTEGER NOT NULL,
    FOREIGN KEY (AlbumId) REFERENCES Albums (AlbumId)
);
