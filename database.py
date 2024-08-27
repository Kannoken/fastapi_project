from schemas import Base
from workers import engine
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
