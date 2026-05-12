import base64
from datetime import datetime

from app.database import Column, UUIDModel, db, reference_col, relationship
from app.util import determine_gender, extract_initials, parse_rechtspraak_datetime

EXPECTED_LENGTH_DECODED_RECHTSPRAAK_ID = 24


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
    last_name = Column(db.Text, nullable=True)
    last_name_own = Column(db.Text, nullable=True)
    last_name_partner = Column(db.Text, nullable=True)
    did_not_self_report_side_jobs = Column(db.Boolean, nullable=True)
    has_no_side_jobs = Column(db.Boolean, nullable=True)
    gender = Column(db.Text, nullable=True)
    toon_naam = Column(db.Text, nullable=True)
    toon_naam_kort = Column(db.Text, nullable=True)
    rechtspraak_id = Column(db.Text, nullable=False, unique=True)
    rechtspraak_internal_id = Column(db.Text, nullable=False, unique=True)
    first_scraped_at = Column(db.DateTime, default=datetime.now, nullable=False)
    last_scraped_at = Column(db.DateTime, nullable=True)
    protected = Column(db.Boolean, default=False)
    removed_from_rechtspraak_at = Column(db.DateTime, nullable=True)
    verdicts = relationship("PersonVerdict", back_populates="person")

    @property
    def former_judge(self) -> bool:
        return True if self.removed_from_rechtspraak_at else False

    @staticmethod
    def extract_rechtspraak_internal_id(rechtspraak_id: str) -> str:
        """
        The 32 bytes base64 encoded rechtspraak_id is not unique. When you search for the same person twice, you will
        get a different rechtspraak_id value. Hence we update this value. The value does contain a hidden constant
        identifier that is actually unique.

        I.e. the rechtspraak_identifiers for 'Aalbers' are (this wroked on April 26, 2026):
            Gdt0tdGIIuzw8KSh2gMpRWZbZSWiGKxR
            5dw03zI8T6G2KSdAjiB3KmZbZSWiGKxR
            36Kwhv2cTaPtkHp4IuuRvmZbZSWiGKxR
            HkSJNxWvetDolZ_2HMHWimZbZSWiGKxR
            WCYcEezsc9aHgX6zzdSDFWZbZSWiGKxR
            glQd8FEdhZQtGPPnaJC6NGZbZSWiGKxR
            wS8idUKONa5z7FnZY2iQX2ZbZSWiGKxR
            kXxH0Vc_efNFkJTNsSkkG2ZbZSWiGKxR
            sP0mz6Lag5_M8psivG9BYGZbZSWiGKxR
            qAKJ16y3iaSH3HJN_nT3hGZbZSWiGKxR
            i8k3m3IJGzFpR2nUqO_pDmZbZSWiGKxR
            mWxMsW1oKLbpzS2nxr9gY2ZbZSWiGKxR
            F_ZlpgPY_nnHlxuhpxzU8mZbZSWiGKxR

        The 'identifier' is always 32 characters long. They use HTTP safe base64 encoding where + is replaced by -
        and / by _. Decoding yields 24 bytes. Of those 24 bytes, the last 8 bytes of the identifier is constant
        per person. If you change any of the first 16 bytes, you will always end up on the same page.

        It is currently unknown what any of the first 16 bytes mean, but entropy analysis indicates it is either
        compressed or encrypted. Regardless, this is a solid way to identify people across name changes.
        """
        encoded_id = rechtspraak_id.encode()
        decoded_id = base64.b64decode(encoded_id, altchars=b"-_")
        if len(decoded_id) != EXPECTED_LENGTH_DECODED_RECHTSPRAAK_ID:
            raise ValueError(f"length of rechtspraak_id is not {EXPECTED_LENGTH_DECODED_RECHTSPRAAK_ID}: {decoded_id}")
        return decoded_id[16:].hex()

    @staticmethod
    def from_dict(d: dict) -> dict:
        toon_naam = (d.get("toonnaam") or "").strip()
        toon_naam_kort = (d.get("toonnaamkort") or "").strip()
        len_last_name = len(toon_naam) - len(toon_naam_kort)
        titles = d.get("toonnaam", "")[0:len_last_name].strip()
        rechtspraak_id = (d.get("persoonId") or "").strip()
        rechtspraak_internal_id = Person.extract_rechtspraak_internal_id(rechtspraak_id)

        return dict(
            rechtspraak_id=rechtspraak_id,
            rechtspraak_internal_id=rechtspraak_internal_id,
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
    institution = relationship("Institution", backref="professional_detail", lazy="select")

    @staticmethod
    def transform_beroepsgegevens_dict(d: dict) -> dict:
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            main_job=bool(d.get("hoofdfunctie")),
            function=(d.get("functieOmschrijving") or "").strip(),
            organisation=(d.get("instantieOmschrijving") or "").strip(),
            remarks=(d.get("opmerkingen") or "").strip(),
        )

    @staticmethod
    def transform_historisch_beroepsgegevens_dict(d: dict) -> dict:
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
    def transform_huidige_nevenbetrekkingen_dict(d: dict) -> dict:
        return dict(
            start_date=parse_rechtspraak_datetime(d.get("begindatum") or ""),
            paid=(d.get("bezoldigd") or "").strip(),
            function=(d.get("functie") or "").strip(),
            organisation_name=(d.get("instantie") or "").strip(),
            place=(d.get("plaats") or "").strip(),
            organisation_type=(d.get("soortbedrijf") or "").strip(),
        )

    @staticmethod
    def transform_voorgaande_nevenbetrekkingen_dict(d: dict) -> dict:
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
