from sqlalchemy import Column, DateTime, Integer, String

from src.main.api.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username}, "
            f"role={self.role}, deleted_at={self.deleted_at})"
        )
