import pyodbc

def get_connection():
    return pyodbc.connect("Driver=SQL Server; Server=HAO\SQLEXPRESS; Database=VoresDB; Trusted_Connection=yes; UID=sa; PWD=123456789")

connection = get_connection()