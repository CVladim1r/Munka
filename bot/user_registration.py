from database.db_connector import add_user_to_db_type_user, add_employer_to_db, update_user_type, update_employer_type

async def register_job_seeker(message, user_id, user_name, user):
    await add_user_to_db_type_user(message, user_id, user, user_name, user_type="USER")
    await update_user_type(user_id, "USER")

async def register_employer(message, employer_id, employer_name, employer_username):
    await add_employer_to_db(message, employer_id, employer_username, employer_name, employer_type="EMPLOYER")
    await update_employer_type(employer_id, "EMPLOYER")