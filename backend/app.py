from flask import Flask
from flask_restx import Resource
from flask_restx import Api
from flask_cors import CORS
from backend.database.config import init_db, db
from backend.routes.usuarios_routes import api as usuarios_ns
from backend.routes.produtos_base_routes import api as produtos_base_ns
from backend.routes.unidades_routes import api as unidades_ns
from backend.routes.itens_usuario_routes import api as itens_usuario_ns
from backend.routes.eventos_routes import api as eventos_ns

app = Flask(__name__)
api = Api(app, doc="/swagger", title="API MVP", description="Documentação da API com Flask-RESTX")

api.add_namespace(usuarios_ns, path="/usuarios")
api.add_namespace(unidades_ns, path="/unidades")
api.add_namespace(produtos_base_ns, path="/produtos_base")
api.add_namespace(itens_usuario_ns, path="/itens_usuario")
api.add_namespace(eventos_ns, path="/eventos")

CORS(app)

# Inicializa o banco
init_db(app)
with app.app_context():
    db.create_all()
# 🔹 Importa e registra o namespace de usuários
from backend.routes.usuarios_routes import api as usuarios_ns
api.add_namespace(usuarios_ns, path="/usuarios")

# 🔹 Endpoint básico de teste
@api.route('/ping')
class PingResource(Resource):  # <--- herda de Resource!
    def get(self):
        return {"message": "Servidor Flask funcionando 🚀"}

if __name__ == "__main__":
    app.run(debug=True)
