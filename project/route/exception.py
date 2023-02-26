class Roads_exception(Exception):
    
    def __init__(self, message, ways):
        super().__init__(message)
        self.__ways = ways
        
    def get_ways(self):
        return self.__ways
