from app import create_app
application = create_app()

#from app import db
#with application.app_context():
    #db.create_all()


if __name__ == "__main__":
    application.run(debug=True,host='0.0.0.0')
