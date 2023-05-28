NO_INSTITUTIONS_XML = """
<Instanties>
</Instanties>"""

ONE_INSTITUTION_XML = """
<Instanties>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/agam</Identifier>
        <Naam>Ambtenarengerecht Amsterdam</Naam>
        <Afkorting>AGAMS</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1913-01-01</BeginDate>
    </Instantie>
</Instanties>
"""

FIVE_INSTITUTIONS_XML = """
<Instanties>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/agam</Identifier>
        <Naam>Ambtenarengerecht Amsterdam</Naam>
        <Afkorting>AGAMS</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1913-01-01</BeginDate>
    </Instantie>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/agah</Identifier>
        <Naam>Ambtenarengerecht Arnhem</Naam>
        <Afkorting>AGARN</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1913-01-01</BeginDate>
    </Instantie>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/aggr</Identifier>
        <Naam>Ambtenarengerecht Groningen</Naam>
        <Afkorting>AGGRO</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1950-01-01</BeginDate>
    </Instantie>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/aghl</Identifier>
        <Naam>Ambtenarengerecht Haarlem</Naam>
        <Afkorting>AGHAA</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1950-01-01</BeginDate>
    </Instantie>
    <Instantie>
        <Identifier>http://psi.rechtspraak.nl/agrm</Identifier>
        <Naam>Ambtenarengerecht Roermond</Naam>
        <Afkorting>AGROE</Afkorting>
        <Type>AndereGerechtelijkeInstantie</Type>
        <BeginDate>1950-01-01</BeginDate>
    </Instantie>
</Instanties>
"""

NO_LEGAL_AREAS_XML = """
<Rechtsgebieden>
</Rechtsgebieden>"""

ONE_MAIN_AND_ONE_SUB_LEGAL_AREA_XML = """
<Rechtsgebieden>
    <Rechtsgebied>
        <Identifier>http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht</Identifier>
        <Naam>Bestuursrecht</Naam>
        <Rechtsgebied>
            <Identifier>http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht_ambtenarenrecht</Identifier>
            <Naam>Ambtenarenrecht</Naam>
        </Rechtsgebied>
    </Rechtsgebied>
</Rechtsgebieden>"""

TWO_MAIN_AND_TWO_SUB_LEGAL_AREAS_XML = """
<Rechtsgebieden>
    <Rechtsgebied>
        <Identifier>
        http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht
        </Identifier>
        <Rechtsgebied>
            <Identifier>http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht_ambtenarenrecht</Identifier>
            <Naam>Ambtenarenrecht</Naam>
        </Rechtsgebied>
        <Rechtsgebied>
            <Identifier>http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht_belastingrecht</Identifier>
            <Naam>Belastingrecht</Naam>
        </Rechtsgebied>
    </Rechtsgebied>
    <Rechtsgebied>
        <Identifier>http://psi.rechtspraak.nl/rechtsgebied#civielRecht</Identifier>
        <Naam>Civiel recht</Naam>
        <Rechtsgebied>
            <Identifier>http://psi.rechtspraak.nl/rechtsgebied#civielRecht_aanbestedingsrecht</Identifier>
            <Naam>Aanbestedingsrecht</Naam>
        </Rechtsgebied>
        <Rechtsgebied>
            <Identifier>http://psi.rechtspraak.nl/rechtsgebied#civielRecht_arbeidsrecht</Identifier>
            <Naam>Arbeidsrecht</Naam>
        </Rechtsgebied>
    </Rechtsgebied>
</Rechtsgebieden>"""


NO_PROCEDURE_TYPES_XML = """
<Proceduresoorten>
</Proceduresoorten>"""

ONE_PROCEDURE_TYPE_XML = """
<Proceduresoorten>
    <Proceduresoort>
        <Identifier>http://psi.rechtspraak.nl/procedure#artikel81ROzaken</Identifier>
        <Naam>Artikel 81 RO-zaken</Naam>
    </Proceduresoort>
</Proceduresoorten>
"""

FIVE_PROCEDURE_TYPES_XML = """
<Proceduresoorten>
    <Proceduresoort>
        <Identifier>http://psi.rechtspraak.nl/procedure#artikel81ROzaken</Identifier>
        <Naam>Artikel 81 RO-zaken</Naam>
    </Proceduresoort>
    <Proceduresoort>
        <Identifier>http://psi.rechtspraak.nl/procedure#bodemzaak</Identifier>
        <Naam>Bodemzaak</Naam>
    </Proceduresoort>
    <Proceduresoort>
        <Identifier>http://psi.rechtspraak.nl/procedure#cassatie</Identifier>
        <Naam>Cassatie</Naam>
    </Proceduresoort>
    <Proceduresoort>
        <Identifier>
        http://psi.rechtspraak.nl/procedure#cassatieInHetBelangDerWet
        </Identifier>
    <Naam>Cassatie in het belang der wet</Naam>
    </Proceduresoort>
    <Proceduresoort>
        <Identifier>http://psi.rechtspraak.nl/procedure#conservatoireMaatregel</Identifier>
        <Naam>Conservatoire maatregel</Naam>
    </Proceduresoort>
</Proceduresoorten>
"""
