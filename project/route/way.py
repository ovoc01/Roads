import math
from database import Connection

class Way:
    
    __name = ''
    __length_max = 0
    __width = 0
    __depart = 0
    __arrive = 0
    __niveau = 0
    
    def __init__(self, name, length_max, width):
        self.set_name(name)
        self.set_length_max(length_max)
        self.set_width(width)
        
    def __set_depart(self, depart):
        try:
            value = float(depart)
            if value < 0: raise Exception("Depart doit être positive")
            if value > self.get_length_max(): raise Exception("Depart a dépassé la longueur maximum")
            self.__depart = round(value)
        except ValueError:
            raise Exception("Depart doit être un nombre")
        
    def get_depart(self):
        return self.__depart
        
    def __set_arrive(self, arrive):
        try:
            value = float(arrive)
            if value < 0: raise Exception("Arrive doit être positive")
            if value > self.get_length_max(): raise Exception("Arrive a dépassé la longueur maximum")
            self.__arrive = round(value)
        except ValueError:
            raise Exception("Arrive doit être un nombre")
        
    def get_arrive(self):
        return self.__arrive
    
    def set_point_kilometrique(self, depart, arrive):
        self.__set_arrive(arrive)
        self.__set_depart(depart)
        if float(depart) > float(arrive): raise Exception("Depart doit être inférieur à l'arrive")
    
    def set_niveau(self, niveau):
        try:
            value = float(niveau)
            if value < 0: raise Exception("Niveau doit être positive") 
            self.__niveau = round(value)
        except ValueError:
            raise Exception("Niveau doit être un nombre")
    
    def get_niveau(self):
        return self.__niveau
        
    def set_name(self, name):
        self.__name = str(name)
        
    def get_name(self):
        return self.__name
        
    def set_width(self, width):
        try:
            value = float(width)
            if value < 0: raise Exception("Width is must be positive")
            self.__width = value
        except ValueError:
            raise Exception("Width is not valid")
        
    def get_width(self):
        return self.__width
    
    def set_length_max(self, length_max):
        try:
            value = float(length_max)
            if value < 0: raise Exception("Length is must be positive")
            self.__length_max = round(value)
        except ValueError:
            raise Exception("Length is not valid")
        
    def get_length_max(self):
        return self.__length_max
    
    def get_length(self):
        return math.fabs(self.get_depart() - self.get_arrive())
    
    def get_volume(self):
        return self.get_length() * self.get_width() * (self.get_niveau() / 10)
    
    def get_prix_reparation(self):
        somme = 0
        roads = self.get_bad_roads()
        for road in roads:
            if road.get_depart() < self.get_depart():
                road.__set_depart(self.get_depart())
            if road.get_arrive() > self.get_arrive():
                road.__set_arrive(self.get_arrive())
            somme += road.get_volume() * road.get_prix_unitaire()
        return round(somme, 3)
    
    def get_duree_reparation(self):
        value = round(self.get_prix_reparation() / self.get_duree_unitaire())
        if value > 24:
            return str(round(value / 24, 3)) + " jour"
        return str(round(value, 3)) + " heure"
    
    def get_prix_unitaire(self):
        return 30000
    
    def get_duree_unitaire(self):
        return 20000
        
    def get_bad_roads(self):
        connection = Connection.getPostgreSQL()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM route_reparation WHERE ((%s <= depart AND depart <= %s) OR (%s <= arrive AND arrive <= %s)) AND name = %s", 
                       (self.get_depart(), self.get_arrive(), self.get_depart(), self.get_arrive(), self.get_name()))
        array = []
        for component in cursor.fetchall():
            way = Way(component[0], component[1], component[2])
            way.set_point_kilometrique(component[3], component[4])
            way.set_niveau(component[5])
            array.append(way)
            print(way.get_depart())
        cursor.close()
        connection.commit()
        connection.close()
        return array
        
    def insert(self):
        connection = Connection.getPostgreSQL()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO bad_roads(roadno, depart, arrive, niveau) VALUES (%s, %s, %s, %s)",
                       (self.get_name(), self.get_depart(), self.get_arrive(), self.get_niveau()))
        cursor.close()
        connection.commit()
        connection.close()
        
    def get_liste_route_nationale():
        connection = Connection.getPostgreSQL()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM route_nationale")
        array = []
        for component in cursor.fetchall():
            array.append(Way(component[0], component[1], component[2]))
        cursor.close()
        connection.commit() 
        connection.close()
        return array
    
    def get_route_nationale(id):
        connection = Connection.getPostgreSQL()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM route_nationale WHERE name='" + id + "'")
        component = cursor.fetchone()
        value = Way(component[0], component[1], component[2])
        cursor.close()
        connection.commit()
        connection.close()
        return value