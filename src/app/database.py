from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+mysqldb://root:ramidatabase@localhost:3306/3d_printing_project',
    connect_args={"host": "127.0.0.1"},
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    return SessionLocal()