from bot.database.methods.create import add_user_to_db_type_user, add_employer_to_db

async def register_job_seeker(user_tgid, user_tgname, user_fullname):
    await add_user_to_db_type_user(user_tgid, user_tgname, user_fullname, user_type="USER")

async def register_employer(message, employer_id, employer_name, employer_username):
    await add_employer_to_db(message, employer_id, employer_username, employer_name, employer_type="EMPLOYER")
