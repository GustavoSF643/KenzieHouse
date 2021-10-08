from app.configs.database import db

class DefaultModel:

    def save_self(self):
        db.session.add(self)
        db.session.commit()

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()
