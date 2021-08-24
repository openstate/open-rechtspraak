from app import app
from app.extensions import db
from app.models import (
    PersonVerdict, Person, ProfessionalDetail, SideJob, Verdict, Institution,
    ProcedureType, LegalArea
)


# This piece of code automatically imports the db and models when you start a
# Flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'PersonVerdict': PersonVerdict,
        'Person': Person,
        'ProfessionalDetail': ProfessionalDetail,
        'SideJob': SideJob,
        'Verdict': Verdict,
        'Institution': Institution,
        'ProcedureType': ProcedureType,
        'LegalArea': LegalArea
    }


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
