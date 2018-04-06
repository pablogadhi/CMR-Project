
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def resetAllTables(cursor):
    cursor.execute("DELETE FROM dbconnection_propiedad")
    cursor.execute("DELETE FROM dbconnection_propietario")
    cursor.execute("DELETE FROM dbconnection_comprador")
    cursor.execute("DELETE FROM dbconnection_intermediario")
    cursor.execute("DELETE FROM dbconnection_visita")
    cursor.execute("DELETE FROM dbconnection_administra")
    cursor.execute("DELETE FROM dbconnection_valoresadicionales")
    cursor.execute("DELETE FROM dbconnection_camposadicionales")
    cursor.execute("DELETE FROM dbconnection_cantidadtuplas")

    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (0,'propiedad',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (1,'propietario',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (2,'comprador',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (3,'intermediario',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (4,'visita',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (6,'adminsitra',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (7,'camposadicionales',0)")
    cursor.execute("INSERT INTO dbconnection_cantidadtuplas VALUES (8,'valoresadicionales',0)")
