import os
from front import app

if __name__ == '__main__':
    app.run(
        host=os.getenv('SERVER_ADDRESS'),
        port=os.getenv('SERVER_PORT'),
        debug=os.getenv('DEBUG_MODE')
    )