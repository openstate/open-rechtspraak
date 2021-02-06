from app.database import Column, UUIDModel, db


class People(UUIDModel):
    __tablename__ = "people"
    titles = Column(db.Text, nullable=True)
    initials = Column(db.Text, nullable=True)
    first_name = Column(db.Text, nullable=True)
    last_name = Column(db.Text, nullable=True)
    gender = Column(db.Text, nullable=True)
    toon_naam = Column(db.Text, nullable=True, unique=True)
    toon_naam_kort = Column(db.Text, nullable=True)
    rechtspraak_id = Column(db.Text, nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "titles": self.titles,
            "initials": self.initials,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "toon_naam": self.toon_naam,
            "toon_naam_kort": self.toon_naam_kort,
            "rechtspraak_id": self.rechtspraak_id,
        }

    @staticmethod
    def from_dict(d):
        len_last_name = len(d.get("toonnaam").strip()) - len(d.get("toonnaamkort", ""))
        titles = d.get("toonnaam", "")[0:len_last_name].strip()

        return dict(
            rechtspraak_id=d.get("persoonId", "").strip(),
            last_name=d.get("ACHTERNAAM", "").strip(),
            toon_naam=d.get("toonnaam", "").strip(),
            toon_naam_kort=d.get("toonnaamkort", "").strip(),
            titles=titles,
        )
