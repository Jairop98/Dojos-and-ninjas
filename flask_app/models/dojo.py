from flask_app.config.mysqlconnection import connectToMySQL
from .ninja import Ninja
# gets all the dojos and returns them in a list of dojo objects

class Dojo:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []
    # We create a list so that later we can add in all the ninjas that are associated with a dojo

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query) #list of dictionaries
        dojos = []
        for d in results:
            dojos.append( cls(d) )
        return dojos

    @classmethod
    def save(cls, data):
        query= "INSERT INTO dojos (name) VALUES (%(name)s);"
        result = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        return result

    @classmethod
    def get_one_with_ninjas(cls, data ):
        query = "SELECT * FROM dojos LEFT JOIN ninjas on dojos.id = ninjas.dojos_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
            # results will print list with the ninjas name attached
        print(results)
        dojo = cls(results[0]) 
        for row in results:
            n = {
                'id': row['ninjas.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'age': row['age'],
                'created_at': row['ninjas.created_at'],
                'updated_at': row['ninjas.updated_at']
            }
            dojo.ninjas.append( Ninja(n) )
        return dojo

