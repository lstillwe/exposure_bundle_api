#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS

def main():
    print("Hello Lisa!")
    app = connexion.App(__name__, specification_dir='./swagger/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Exposure Bundle API'})
    print(app)
    app.run(port=8080)



if __name__ == '__main__':
    main()
