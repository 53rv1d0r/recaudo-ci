from app.main import verificar_db


def test_resuelve_nombre_servicio_db():
    # Valida que el nombre de servicio 'db' se resuelve en la red de Docker
    resultado = verificar_db(host="db", port=5432)
    assert resultado["db_host"] == "db"
    assert resultado["db_port"] == 5432


def test_detecta_host_invalido():
    resultado = verificar_db(host="host_que_no_existe_123", port=5432)
    assert resultado["status"] == "error"