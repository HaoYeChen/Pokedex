from database.db import get_connection
from models.trainer import Trainer

def create_trainer(name, pokemon):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Trainers_table (Name, Pokemon) VALUES (?, ?)", (name, pokemon))
    connection.commit()

def read_trainers():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Id, Name, Pokemon FROM Trainers_table")
    trainers = []
    for row in cursor.fetchall():
        trainer = Trainer(row.Id, row.Name, row.Pokemon)
        trainers.append(trainer)
    return trainers

def update_trainer(trainer_id, name, pokemon):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Trainers_table SET Name = ?, Pokemon = ? WHERE Id = ?", (name, pokemon, trainer_id))
    connection.commit()

def delete_trainer(trainer_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Trainers_table WHERE Id = ?", (trainer_id,))
    connection.commit()