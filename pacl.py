from app import create_app, db
from app.models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db,
            'User':User,
            "Invitation": Invitation,
            'Term': Term,
            'Domain': Domain,
            'Morph': Morph,
            'Gloss': Gloss,
            'Language': Language}

