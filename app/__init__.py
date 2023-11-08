from .database import init_db


def create_app():
    # Initialize your application
    init_db()
    # Here you can add more initialization code if needed
    # Since you're not running a web server, you don't need to return anything
