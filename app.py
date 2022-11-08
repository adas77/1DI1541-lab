from flask import session
from src import init_app
from src.database.order_drop import drop

app = init_app()


@app.before_first_request
def clear_session_vars():
    session.clear()
    


if __name__ == "__main__":
    app.run()
    drop()
    
