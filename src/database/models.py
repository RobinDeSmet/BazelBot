from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, func


Base = declarative_base()
metadata = Base.metadata


class Bazel(Base):
    """Bazel Model"""

    __tablename__ = "bazels"
    id = Column(Integer, primary_key=True)
    content_hash = Column(String(64), unique=True)
    content = Column(String(512))
    create_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, content: {self.content}"
