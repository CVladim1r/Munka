import aiomysql

class Database:
    def __init__(self, loop, **kwargs):
        self.loop = loop
        self.pool = None
        self.config = kwargs

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            db=self.config['database'],
            loop=self.loop,
            autocommit=True
        )

    # Другие методы вашего класса Database
