import pyodbc

def get_connection():
    return pyodbc.connect("Driver=SQL Server; Server=HAO\SQLEXPRESS; Database=VoresDB; Trusted_Connection=yes; UID=sa; PWD=123456789")

connection = get_connection()  # Establish a connection to the SQL Server database using the provided connection string
