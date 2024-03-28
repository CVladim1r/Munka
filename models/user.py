from database.db_connector import Database

class User:
    def __init__(self, user_type, user_name, age=None, description=None, company_name=None):
        self.user_type = user_type
        self.user_name = user_name
        self.age = age
        self.description = description
        self.company_name = company_name

    async def save(self):
        db = Database()
        await db.connect()
        query = "INSERT INTO USERS (USER, USER_NAME, AGE, DESCRIPTION, COMPANY_NAME) VALUES (%s, %s, %s, %s, %s)"
        await db.execute(query, self.user_type, self.user_name, self.age, self.description, self.company_name)
