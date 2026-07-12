# Este import permite crear un motor de base de datos para interactuar con la base de datos
from sqlalchemy import create_engine

# Este import permite crear una sesión de base de datos para interactuar con la base de datos
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Este import permite obtener la configuración de la base de datos
from app.config import settings

# Este import permite crear un motor de base de datos para interactuar con la base de datos
engine = create_engine(settings.DATABASE_URL)

# Este import permite crear una sesión de base de datos para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta clase permite crear una base de datos para interactuar con la base de datos
class Base(DeclarativeBase):
    pass

# Esta función permite obtener una sesión de base de datos para interactuar con la base de datos
def get_db():
    db = SessionLocal()
    try:
        # Yield entrega algo temporal abre sesion y se usa
        yield db
    finally:
        db.close()


