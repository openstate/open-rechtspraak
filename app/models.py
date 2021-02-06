from app.database import Column, UUIDModel, db, reference_col, relationship
from app.util import parse_rechtspraak_datetime


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
    last_scraped_at = Column(db.DateTime, nullable=True)

    @property
    def serialize(self):
        professional_details = ProfessionalDetails.query.filter(
            ProfessionalDetails.person_id == self.id
        ).filter(ProfessionalDetails.historical.is_(False))
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
            "beroepsgegevens": [
                {"function": pd.function} for pd in professional_details
            ],
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


class ProfessionalDetails(UUIDModel):
    __tablename__ = "professional_details"
    start_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)
    main_job = Column(db.Boolean, default=False)
    function = Column(db.Text, nullable=False)
    historical = Column(db.Boolean, default=False)
    remarks = Column(db.Text, nullable=True)
    person_id = reference_col("people", nullable=False)
    person = relationship("People", backref="professional_details", lazy="select")

    @staticmethod
    def transform_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum")),
            main_job=bool(d.get("hoofdfunctie")),
            function=d.get("functieOmschrijving", "").strip(),
            remarks=(d.get("opmerkingen", "") or "").strip(),
        )

    @staticmethod
    def transform_historisch_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum")),
            end_date=parse_rechtspraak_datetime(d.get("einddatum")),
            main_job=bool(d.get("hoofdfunctie")),
            historical=True,
            function=d.get("functie", "").strip(),
        )
