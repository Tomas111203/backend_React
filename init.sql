-- Initial SQL script for Videogames Database

CREATE TABLE IF NOT EXISTS videogames (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    release_year INTEGER NOT NULL,
    rating NUMERIC(3, 1) NOT NULL,
    developer VARCHAR(150) NOT NULL
);

-- Seed initial videogames with name + 5 attributes (genre, platform, release_year, rating, developer)
INSERT INTO videogames (name, genre, platform, release_year, rating, developer) VALUES
('The Legend of Zelda: Breath of the Wild', 'Action-Adventure', 'Nintendo Switch', 2017, 9.7, 'Nintendo EPD'),
('Elden Ring', 'Action RPG', 'Multi-platform', 2022, 9.6, 'FromSoftware'),
('Cyberpunk 2077', 'RPG', 'Multi-platform', 2020, 8.5, 'CD Projekt Red'),
('God of War Ragnarök', 'Action-Adventure', 'PlayStation 5', 2022, 9.4, 'Santa Monica Studio'),
('Red Dead Redemption 2', 'Action-Adventure', 'Multi-platform', 2018, 9.8, 'Rockstar Games'),
('Super Mario Odyssey', 'Platformer', 'Nintendo Switch', 2017, 9.7, 'Nintendo EPD'),
('Halo Infinite', 'First-Person Shooter', 'Xbox Series X', 2021, 8.7, '343 Industries');
