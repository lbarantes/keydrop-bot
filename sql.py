import pymysql
from datetime import datetime
import os
import getmac

host = os.getenv("DB_HOST", "host_padrao")
user = os.getenv("DB_USER", "usuario_padrao")
password = os.getenv("DB_PASSWORD", "senha_padrao")
database = os.getenv("DB_NAME", "database_padrao")

def getConnection():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=3306,
    )

try:
    with getConnection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

def getMac():
    try:
        return getmac.get_mac_address()
    except:
        return None

def checkKey(key):
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT `expiresOn`, `macAddress` FROM `userKeys` WHERE userKey = %s;"
                cursor.execute(query, (key,))
                result = cursor.fetchone()
        
        if not result:
            return {"status": False, "message": "Chave não existente"}
        
        expiresOn = result[0]
        savedMac = result[1]
        currentMac = getMac()
        
        if expiresOn < datetime.now():
            return {"status": False, "message": "Essa chave expirou"}
            
        if savedMac is None and currentMac:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    query = "UPDATE userKeys SET macAddress = %s WHERE userKey = %s"
                    cursor.execute(query, (currentMac, key))
                    connection.commit()
            savedMac = currentMac
        elif savedMac is not None and currentMac != savedMac:
            return {"status": False, "message": "Esta chave já está registrada em outro computador"}
        
        return {"status": True, "message": "Acesso válido", "macAddress": savedMac}
        
    except Exception as e:
        return {"status": False, "message": f"Erro ao verificar chave: {e}"}
