from app.database import Column, UUIDModel, db, reference_col, relationship
from app.util import determine_gender, extract_initials, parse_rechtspraak_datetime


class PersonVerdict(UUIDModel):
    __tablename__ = "person_verdict"
    verdict_id = reference_col("verdict", column_kwargs={"primary_key": False})
    person_id = reference_col("person", column_kwargs={"primary_key": False})
    role = Column(db.Text, nullable=True)
    verdict = relationship("Verdict", back_populates="people")
    person = relationship("Person", back_populates="verdicts")


class Person(UUIDModel):
    __tablename__ = "person"
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
    removed_from_rechtspraak_at = Column(db.DateTime, nullable=True)
    verdicts = relationship("PersonVerdict", back_populates="person")

    @property
    def former_judge(self):
        return True if self.removed_from_rechtspraak_at else False

    @staticmethod
    def from_dict(d):
        toon_naam = (d.get("toonnaam") or "").strip()
        toon_naam_kort = (d.get("toonnaamkort") or "").strip()
        len_last_name = len(toon_naam) - len(toon_naam_kort)
        titles = d.get("toonnaam", "")[0:len_last_name].strip()

        return dict(
            rechtspraak_id=(d.get("persoonId") or "").strip(),
            last_name=(d.get("ACHTERNAAM") or "").strip(),
            gender=determine_gender(toon_naam),
            toon_naam=toon_naam,
            toon_naam_kort=toon_naam_kort,
            titles=titles,
            initials=extract_initials(toon_naam_kort),
        )


class ProfessionalDetail(UUIDModel):
    __tablename__ = "professional_detail"
    start_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)
    main_job = Column(db.Boolean, default=False)
    function = Column(db.Text, nullable=False)
    organisation = Column(db.Text, nullable=True)
    remarks = Column(db.Text, nullable=True)
    person_id = reference_col("person", nullable=False)
    person = relationship("Person", backref="professional_detail", lazy="select")
    institution_id = reference_col("institution", nullable=True)
    institution = relationship(
        "Institution", backref="professional_detail", lazy="select"
    )

    @staticmethod
    def transform_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            main_job=bool(d.get("hoofdfunctie")),
            function=(d.get("functieOmschrijving") or "").strip(),
            organisation=(d.get("instantieOmschrijving") or "").strip(),
            remarks=(d.get("opmerkingen") or "").strip(),
        )

    @staticmethod
    def transform_historisch_beroepsgegevens_dict(d):
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            end_date=parse_rechtspraak_datetime(d.get("einddatum") or ""),
            main_job=bool(d.get("hoofdfunctie")),
            function=(d.get("functie") or "").strip(),
            organisation=(d.get("instantie") or "").strip(),
        )


class SideJob(UUIDModel):
    __tablename__ = "side_job"
    start_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)
    function = Column(db.Text, nullable=False)
    place = Column(db.Text, nullable=True)
    paid = Column(db.Text, nullable=True)
    organisation_name = Column(db.Text, nullable=True)
    organisation_type = Column(db.Text, nullable=True)
    person_id = reference_col("person", nullable=False)
    person = relationship("Person", backref="side_job", lazy="select")

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


class Verdict(UUIDModel):
    __tablename__ = "verdict"
    ecli = Column(db.Text, nullable=False, unique=True)
    title = Column(db.Text, nullable=True)
    summary = Column(db.Text, nullable=True)
    uri = Column(db.Text, nullable=True)
    issued = Column(db.DateTime, nullable=True)
    zaak_nummer = Column(db.Text, nullable=True)
    type = Column(db.Text, nullable=True)
    coverage = Column(db.Text, nullable=True)
    subject = Column(db.Text, nullable=True)
    spatial = Column(db.Text, nullable=True)
    procedure = Column(db.Text, nullable=True)
    raw_xml = Column(db.Text, nullable=True)
    last_scraped_at = Column(db.DateTime, nullable=True)
    people = relationship("PersonVerdict", back_populates="verdict")
    contains_beslissing = Column(db.Boolean, nullable=False, default=False)
    beslissings_text = Column(db.Text, nullable=True)
    institution_id = reference_col("institution", nullable=True)
    institution = relationship("Institution", backref="verdict", lazy="select")
    procedure_type_id = reference_col("procedure_type", nullable=True)
    procedure_type = relationship("ProcedureType", backref="verdict", lazy="select")
    legal_area_id = reference_col("legal_area", nullable=True)
    legal_area = relationship("LegalArea", backref="verdict", lazy="select")


class Institution(UUIDModel):
    __tablename__ = "institution"
    lido_id = Column(db.Text, nullable=False, unique=True)
    name = Column(db.Text, nullable=False)
    abbrevation = Column(db.Text, nullable=True)
    type = Column(db.Text, nullable=False)
    begin_date = Column(db.DateTime, nullable=True)
    end_date = Column(db.DateTime, nullable=True)


class ProcedureType(UUIDModel):
    __tablename__ = "procedure_type"
    lido_id = Column(db.Text, nullable=False, unique=True)
    name = Column(db.Text, nullable=False)


class LegalArea(UUIDModel):
    __tablename__ = "legal_area"
    legal_area_lido_id = Column(db.Text, nullable=False, unique=True)
    legal_area_name = Column(db.Text, nullable=False)
