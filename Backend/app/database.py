import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="postgresql://thabo:uDbgmmJwQJ9Ec3Bdm1DtlHkWG1WGd3f3@dpg-d30vgqvfte5s73ftha5g-a.oregon-postgres.render.com/postgresql_rja9"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

