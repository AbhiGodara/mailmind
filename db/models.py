from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db.database import Base

class EmailSummary(Base):
    __tablename__ = "email_summaries"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, index=True)
    sender = Column(String, index=True)
    subject = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    key_points = Column(Text) # Text containing bullets points
    action_items = Column(Text) # Text containing action items to be taken on the email 
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
