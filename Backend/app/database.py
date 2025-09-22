# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session, declarative_base

# DATABASE_URL="postgresql://thabo:uDbgmmJwQJ9Ec3Bdm1DtlHkWG1WGd3f3@dpg-d30vgqvfte5s73ftha5g-a.oregon-postgres.render.com/postgresql_rja9"

# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
# Base = declarative_base()

# # Dependency
# def get_db():
#     db: Session = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual DB URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual DB URL
DATABASE_URL="postgresql://thabo:uDbgmmJwQJ9Ec3Bdm1DtlHkWG1WGd3f3@dpg-d30vgqvfte5s73ftha5g-a.oregon-postgres.render.com/postgresql_rja9"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


