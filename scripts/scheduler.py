from app.tasks.tasks import Tasks
from app.database import engine, Base
from app.dependencies import get_db

Base.metadata.create_all(bind=engine)
db = next(get_db())

Tasks.send_report(db)
