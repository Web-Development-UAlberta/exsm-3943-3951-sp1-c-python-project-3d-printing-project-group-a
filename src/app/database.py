from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+mysqldb://root:ramidatabase@localhost:3306/3d_printing_project',
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    return SessionLocal()