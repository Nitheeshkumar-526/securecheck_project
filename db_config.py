from sqlalchemy import create_engine

def get_engine():
    return create_engine("mysql+mysqlconnector://root:nithi@localhost/police_db")
    
    
