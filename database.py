from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ✅ 1️⃣ Try to use Render’s DATABASE_URL (from environment variable)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:aryan512@localhost:5432/bg_remover"  # fallback for local dev
)

# ✅ 2️⃣ (Optional) If you want to override manually, uncomment this:
# DATABASE_URL = "postgresql://remove_bg_db_user:1GXasLjW4uMeU7YThL9o5oRgMC2VuHo2@dpg-d42uus9r0fns739pbjmg-a/remove_bg_db"

# ✅ 3️⃣ Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# ✅ 4️⃣ Create SessionLocal and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ 5️⃣ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
