from sqlalchemy import Column, Integer, String, Boolean, JSON
from .database import Base  # Import the Base from database.py


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String, unique=True)
    trade_enabled = Column(Boolean)
    abi = Column(JSON)
    chain_id = Column(Integer)
    pair_address = Column(String)
    monitor_event = Column(String)

    def __repr__(self):
        return f"<Token(name={self.name}, address={self.address}, trade_enabled={self.trade_enabled}), chain_id={self.chain_id}>"
