import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://postgres:Qazxsw2016@db:5432/postgres')

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
Base = declarative_base()
