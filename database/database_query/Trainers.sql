
--use VoresDB;

CREATE TABLE Trainers_table (
    id int identity primary key,
    name nvarchar(255),
    pokemon nvarchar(255)
);

insert dbo.Trainers_table( name, pokemon)
values('Ash Ketchum', 'Pikachu'),
	('Brock', 'Onix')

select * from dbo.Trainers_table
