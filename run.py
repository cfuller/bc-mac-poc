import os
from app import app

#print os.environ['base_url']

#if os.environ['environment'] == 'dev':
app.run(host='0.0.0.0', port=5000, debug=True)
#else:
#    app.run(host='0.0.0.0', port=5000, debug=False)