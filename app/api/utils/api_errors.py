from enum import Enum
class ApiError(Exception):
    def __init__(self,cause,status):
        self.cause = cause 
        self.status = status

    def __str__(self):
        return f"{self.cause}" 

    @staticmethod
    def internal_server_error():
        return ApiError("internal server error", 500)  
    @staticmethod
    def unauthorized():
        return ApiError("unauthorized", 401) 