import os

from app import create_app , gRPCserver

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)
    gRPCserver() 
