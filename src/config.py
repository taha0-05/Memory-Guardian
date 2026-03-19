
class Config:

    SERVER = 'localhost'  
    DATABASE = 'MemoryGuardianDB'

    CONNECTION_STRING = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'Trusted_Connection=yes;'
    )
