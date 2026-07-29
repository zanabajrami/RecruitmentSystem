from app.database.base_model import Base
from app.database.session import engine
from app.models import User, Company, Job, Application, Notification

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")