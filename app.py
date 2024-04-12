from flask import Flask
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.user import blp as UserBlueprint
from flask_smorest import Api
from flask_jwt_extended import JWTManager



app = Flask(__name__)

app.config["Propogate_Exception"] =True
app.config["API_TITLE"] = "Items Rest API"
app.config["API_VERSION"] ="v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["JWT_SECRET_KEY"] = "10005016358686330700584599846934291736"

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
    
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        
        {
          "Description":"User has been logout",
          "error": "token_revoked"  
        },
        401
        
    )

api.register_blueprint(ItemBlueprint)
api.register_blueprint(UserBlueprint)

