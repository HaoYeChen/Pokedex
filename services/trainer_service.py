from database.db import get_connection
from models.trainer import Trainer


def create_trainer(name, pokemon):
    # Get database connection
    connection = get_connection()
    # Create cursor object
    cursor = connection.cursor()
    # Execute SQL query & insert a new trainer into Trainers_table
    cursor.execute(
        "INSERT INTO Trainers_table (Name, Pokemon) VALUES (?, ?)", (name, pokemon))
    # Commit transaction
    connection.commit()


def read_trainers():
    connection = get_connection()
    cursor = connection.cursor()
    # Execute SQL query & retrieve all trainers from Trainers_table
    cursor.execute("SELECT Id, Name, Pokemon FROM Trainers_table")
    # Create empty list & store trainers
    trainers = []
    # Looping fetched rows
    for row in cursor.fetchall():
        # Create Trainer object from fetched data
        trainer = Trainer(row.Id, row.Name, row.Pokemon)
        # Append trainer to list
        trainers.append(trainer)
    # Return list of trainers
    return trainers


def update_trainer(trainer_id, name, pokemon):
    connection = get_connection()
    cursor = connection.cursor()
    # Execute SQL query & update trainer in Trainers_table
    cursor.execute("UPDATE Trainers_table SET Name = ?, Pokemon = ? WHERE Id = ?",
                   (name, pokemon, trainer_id))
    connection.commit()


def delete_trainer(trainer_id):
    connection = get_connection()
    cursor = connection.cursor()
    # Execute SQL query & delete trainer from Trainers_table
    cursor.execute("DELETE FROM Trainers_table WHERE Id = ?", (trainer_id,))
    connection.commit()
