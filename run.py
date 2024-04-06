import os
from app import db
from app.models import User
from app.crud import query_all_users
from app import app as app_runner

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	
    with app_runner.app_context():
        db.create_all()
        # new_user = User(id=1345, user='123456',password='1234646')
        # db.session.add(new_user)
        # db.session.commit()
        # query_all_users()


    port = int(os.environ.get("PORT", 5000))
    app_runner.run(host='0.0.0.0', port=port)
