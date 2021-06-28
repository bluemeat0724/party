from app import create_app, db
from flask_migrate import Migrate,MigrateCommand
import ssl

app = create_app('testing')
Migrate(app,db)




if __name__ == '__main__':
    app.run(
        port=443,
        host='0.0.0.0',
            ssl_context=('5863347_yy-test.stte.com.pem', '5863347_yy-test.stte.com.key')
    )
