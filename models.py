from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class WalletRequest(Base):
    __tablename__ = 'wallet_requests'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'id={self.id}, address="{self.address}", created_at="{self.created_at}"'