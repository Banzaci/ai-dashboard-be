from app.models.user import User
from app.core.security import hash_password

def create_user(db, data):
    user = User(
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return user