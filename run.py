import os
from codearena import app


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1000))
    app.run(debug = True, host='0.0.0.0', port=1000)
    
        