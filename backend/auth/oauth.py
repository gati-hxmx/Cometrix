from flask_dance.contrib.google import make_google_blueprint

def create_google_blueprint():
    return make_google_blueprint(
        client_id=None,  # configから読み込まれるのでNoneでOK
        client_secret=None,
        scope=["profile", "email"],
        redirect_url="/login/google/authorized"
    )
