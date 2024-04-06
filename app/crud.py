
from .models import User

def query_all_users():
    users = User.query.all()
    for user in users:
        print(user.id,  user.user, '   ' , user.password)