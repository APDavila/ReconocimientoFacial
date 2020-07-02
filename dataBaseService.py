import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Manager123',
            db='reconocimiento_facial'
        )

        self.cursor = self.connection.cursor()

    def select_user(self, id):
        sql = 'SELECT id, nombre, apellido,tipo_documento,num_documento, telefono, direccion, email FROM user WHERE id = {}'.format(id)
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            print("id",user[0])
            print("Nombre",user[1])
            print("Apellido",user[2])
            print("Tipo documento",user[3])
            print("Numero Documento",user[4])
            print("Telefono",user[5])
            print("Direccion",user[6])
            print("Email",user[7])

        except Exception as e:
            raise    

    def insert(self, nombre,apellido,tipo_documento,num_documento,telefono,direccion,email):
        sql = """INSERT INTO user (nombre,apellido,tipo_documento,num_documento,telefono,direccion,email) 
                VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(nombre, apellido, tipo_documento, num_documento, telefono, direccion, email)
        try:
            mycursor = self.connection.cursor()
            mycursor.execute(sql)
            self.connection.commit()
            return mycursor.lastrowid
        except Exception as e:
            raise    

    def delete(self, id):
        sql = """DELETE FROM user WHERE id = '{}' """.format(id)
        try:
            mycursor = self.connection.cursor()
            mycursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise    


        
    def insert_user(nombre,apellido,tipo_documento,num_documento,telefono,direccion,email):
        database = Database()
        return database.insert(nombre,apellido,tipo_documento,num_documento,telefono,direccion,email)       
    
    def delete_user(id):
        database = Database()
        database.delete(id)       

