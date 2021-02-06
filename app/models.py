from app.database import Column, UUIDModel, db


class People(UUIDModel):
    __tablename__ = "people"
    titles = Column(db.Text, nullable=True)
    initials = Column(db.Text, nullable=True)
    first_name = Column(db.Text, nullable=True)
    last_name = Column(db.Text, nullable=True)
    gender = Column(db.Text, nullable=True)
