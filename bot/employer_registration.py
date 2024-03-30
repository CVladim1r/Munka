from database.db_connector import add_user_to_db
from database.db_connector import update_user_type

async def register_employer(message, user_id, user_name, user):
    await add_user_to_db(message, user_id, user, user_name, user_type="EMPLOYER")
    await update_user_type(user_id, "EMPLOYER")