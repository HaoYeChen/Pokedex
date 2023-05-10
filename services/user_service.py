# from database.db import conn
# from models.user import User

# def register_user(username, password):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
#     conn.commit()

# def login_user(username, password):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE username=? AND password=?", username, password)
#     user_row = cursor.fetchone()
#     if user_row:
#         user = User(*user_row)
#         return user
#     else:
#         return None