from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import grpc
from concurrent import futures
import app.udaconnect.person_pb2 as pb2 
import app.udaconnect.person_pb2_grpc as pb2_grpc 
import app.udaconnect.services  as services

def gRPCserver() : 
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PersonServiceServicer_to_server(services.PersonServiceGRPC(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()



def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)
    gRPCserver()

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
