from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, func


Base = declarative_base()
metadata = Base.metadata


class Bazel(Base):
    __tablename__ = "bazels"
    id = Column(Integer, primary_key=True)
    content = Column(String(512))
    create_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
