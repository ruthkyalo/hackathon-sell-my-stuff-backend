from mangum import Mangum

from sell_my_stuff.main import app

handler = Mangum(app, lifespan="off")
