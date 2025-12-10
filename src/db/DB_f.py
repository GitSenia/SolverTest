import asyncpg
from src.bot_tg import config as c


async def insert_user(user_name: str, password: str, tg_id: int, tg_name: str) -> bool:
    try:
        conn = await asyncpg.connect(host=c.HOST,user=c.USER,password=c.PASSWORD,database=c.DATABASE,port=c.PORT)
        await conn.execute(
            "INSERT INTO users (username, password_user, id_tg, tg_name) "
            "VALUES ($1, $2, $3, $4);",user_name, password, tg_id, tg_name)
        await conn.close()
        return True
    except asyncpg.exceptions.UniqueViolationError:
        return False  # пользователь с таким id_tg уже существует


async def user_info(id_tg:int):
    conn = await asyncpg.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, database=c.DATABASE ,port=c.PORT)
    row= await conn.fetchrow("Select username,password_user,tg_name from users where id_tg=$1 and payment is TRUE",id_tg)
    await conn.close()
    return row

async def update_info(username: str) -> bool:
    conn = await asyncpg.connect(host=c.HOST,user=c.USER,password=c.PASSWORD,database=c.DATABASE,port=c.PORT)
    result = await conn.execute("UPDATE users SET payment = TRUE WHERE username = $1;", username)
    await conn.close()
    updated_rows = int(result.split()[-1])
    return updated_rows > 0



# async def main():
#     info = await user_info(1243262357)
#     print(info[0])
#
# import asyncio
# asyncio.run(main())