import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
#Servicio en Python que consulta la base de datos por nombre de servicio db
# 2 contenedores comunicados entre sí (una API ligera en Python + base de datos PostgreSQL)

def verificar_db(host: str | None = None, port: int | None = None) -> dict:
    db_host = host or os.getenv("DB_HOST", "db")
    db_port = int(port or os.getenv("DB_PORT", "5432"))
    try:
        ip = socket.gethostbyname(db_host)
        with socket.create_connection((db_host, db_port), timeout=3):
            return {"status": "ok", "db_host": db_host, "db_ip": ip, "db_port": db_port}
    except OSError as exc:
        return {"status": "error", "db_host": db_host, "db_port": db_port, "detail": str(exc)}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/salud":
            resultado = verificar_db()
            codigo = 200 if resultado["status"] == "ok" else 503
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    server.serve_forever()