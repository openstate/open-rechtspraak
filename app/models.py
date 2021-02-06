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
    protected = Column(db.Boolean, default=False)

    @property
    def serialize(self):
        professional_details = ProfessionalDetails.query.filter(
            ProfessionalDetails.person_id == self.id
        ).filter(ProfessionalDetails.end_date.is_(None))
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
        toon_naam = (d.get("toonnaam") or "").strip()
        toon_naam_kort = (d.get("toonnaamkort") or "").strip()
        len_last_name = len(toon_naam) - len(toon_naam_kort)
        titles = d.get("toonnaam", "")[0:len_last_name].strip()

        return dict(
            rechtspraak_id=(d.get("persoonId") or "").strip(),
            last_name=(d.get("ACHTERNAAM") or "").strip(),
            toon_naam=toon_naam,
            toon_naam_kort=toon_naam_kort,
            titles=titles,
        )


class ProfessionalDetails(UUIDModel):
    __tablename__ = "professional_details"
    start_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)
    main_job = Column(db.Boolean, default=False)
    function = Column(db.Text, nullable=False)
    remarks = Column(db.Text, nullable=True)
    person_id = reference_col("people", nullable=False)
    person = relationship("People", backref="professional_details", lazy="select")

    @staticmethod
    def transform_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            main_job=bool(d.get("hoofdfunctie")),
            function=(d.get("functieOmschrijving") or "").strip(),
            remarks=(d.get("opmerkingen") or "").strip(),
        )

    @staticmethod
    def transform_historisch_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            end_date=parse_rechtspraak_datetime(d.get("einddatum") or ""),
            main_job=bool(d.get("hoofdfunctie")),
            function=(d.get("functieOmschrijving") or "").strip(),
        )


class SideJobs(UUIDModel):
    __tablename__ = "side_jobs"
    start_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)
    function = Column(db.Text, nullable=False)
    place = Column(db.Text, nullable=True)
    paid = Column(db.Text, nullable=True)
    organisation_name = Column(db.Text, nullable=True)
    organisation_type = Column(db.Text, nullable=True)
    person_id = reference_col("people", nullable=False)
    person = relationship("People", backref="side_jobs", lazy="select")

    @staticmethod
    def transform_huidige_nevenbetrekkingen_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            paid=(d.get("bezoldigd") or "").strip(),
            function=(d.get("functie") or "").strip(),
            organisation_name=(d.get("instantie") or "").strip(),
            place=(d.get("plaats") or "").strip(),
            organisation_type=(d.get("soortbedrijf") or "").strip(),
        )

    @staticmethod
    def transform_voorgaande_nevenbetrekkingen_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            end_date=parse_rechtspraak_datetime(d.get("einddatum") or ""),
            paid=(d.get("bezoldigd") or "").strip(),
            function=(d.get("functie") or "").strip(),
            organisation_name=(d.get("instantie") or "").strip(),
            place=(d.get("plaats") or "").strip(),
            organisation_type=(d.get("soortbedrijf") or "").strip(),
        )
