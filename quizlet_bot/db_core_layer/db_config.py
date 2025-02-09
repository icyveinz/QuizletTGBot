from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

# Database URL for async connection
db_url = "mysql+aiomysql://myuser:mypassword@db:3306/user_management"

# Create the async engine
engine = create_async_engine(db_url, echo=True)

# Base for declarative models
Base = declarative_base()

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
)
