import os
from flask import Flask, request, jsonify
from data_product_api import db
from data_product_api import auth

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance path exists; otherwise the SQLite db cannot be initialized
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Ignore if it already exists
        pass

    db.init_app(app)


    data_assets = [
      {
        "name": "Chemicals",
        "status": "InDevelopment"
      },
      {
        "name": "Customers",
        "status": "Deprecated"
      },
      {
        "name": "Countries",
        "status": "Released"
      },
      {
        "name": "Companies",
        "status": "InDevelopment"
      }
    ]
    @app.route("/dataassets")
    def get_data_assets():
      return data_assets

    @app.route("/dataassets/<data_asset_name>/datacontracts",methods=["POST"])
    @auth.require_oauth()
    def post_data_contracts(data_asset_name):
        print(data_asset_name)
        print(request.json)

        connection = db.get_connection()
        
        sql = '''INSERT INTO contracts(consumer_data_product_name,consumer_data_product_contact,data_asset_name)
              VALUES(?,?,?) '''
        cur = connection.cursor()
        cur.execute(
            sql, 
            (
                request.json["consumerProduct"]["name"], 
                request.json["consumerProduct"]["responsibleContact"], 
                data_asset_name
            )
        )
        connection.commit()
        print(f"created {cur.lastrowid}")
        print("Data contract is inserted")
        return ""

    @app.route("/dataassets/<data_asset_name>/datacontracts", methods=["GET"])
    def get_data_contracts(data_asset_name):
        print(data_asset_name)
        print(request.json)

        connection = db.get_connection()
        
        sql = '''SELECT * FROM contracts'''
        cur = connection.cursor()
        res = cur.execute(sql)
        
        rows = res.fetchall()
        contracts = []
        for row in rows:
            print(row)
            contracts.append({ "consumerProduct": { "name": row["consumer_data_product_name"] }})

        return contracts

    return app