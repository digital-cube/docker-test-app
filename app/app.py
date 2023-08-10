import os
import sys
import asyncio
import tornado
import json
import datetime
import time
import logging
from tortoise import Tortoise, fields
from tortoise.models import Model

POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')


def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler('/var/log/app/app.log')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL) 
    console_handler.setLevel(logging.ERROR) 
    console_handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
    
log = setup_logger()



TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}",
    },
    "apps": {
        "models": {
            "models": ["__main__"], 
            "default_connection": "default",
        }
    }
}

class TestModel(Model):
    id = fields.IntField(pk=True)
    data = fields.CharField(max_length=255)

    class Meta:
        table = "test_table"

async def init():
    log.debug('Initialising DB')
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close():
    log.debug('Closing connections')
    await Tortoise.close_connections()

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        result = str(datetime.datetime.now())
        log.debug(f'GET server-time-route has been triggered, returning {result}')
        self.write(json.dumps({"now": result}))

class DBHandler(tornado.web.RequestHandler):
    async def get(self):
        result = [row.data for row in await TestModel.filter().all()]
        log.debug(f'GET table-content has been triggered, returning {len(result)} rows')
        self.write(json.dumps({"rows": result}))

    async def post(self):
        item = TestModel(data=str(datetime.datetime.now()))
        log.debug(f'POST table-content has been triggered, adding new row with content {item.data}')
        await item.save()
        self.write(json.dumps({'message': 'row added'}))
            

def make_app():
    return tornado.web.Application([
        (r"/api/server-time", MainHandler),
        (r"/api/table-content", DBHandler),
    ])

async def main():
    app = make_app()
    
    iter = 0
    while True:
        protected_str = TORTOISE_ORM["connections"]["default"].replace(f':{POSTGRES_PASSWORD}@',':*******@')
        try:
            log.debug(f'connecting to database {protected_str}')
            await init()
            log.debug(f'successfully connected')
            break
        except Exception as e:
            iter+=1
            to_wait = iter * 0.2
            if to_wait > 5:
                to_wait = 5
                
            if iter > 100:
                log.critical(f'connecting to database {protected_str} is not possible after {iter} attempts, stopping application')
                sys.exit()
                
            log.error(f'error connecting to database {protected_str}, attempt {iter}, waiting {to_wait} sec for another attempt')
            time.sleep(to_wait)
            continue
            
    log.info('running app on port 80')
    try:
        app.listen(80)
        await asyncio.Event().wait()
    except Exception as e:
        log.critical(f"error occured {e}")
    await close()

if __name__ == "__main__":
    log.info('starting service')
    asyncio.run(main())