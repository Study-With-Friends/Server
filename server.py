from api import app
import os
PORT = os.environ.get('PORT') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT if PORT else 5000, debug=True)
