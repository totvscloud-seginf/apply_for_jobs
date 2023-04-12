from datetime import datetime

from src.app.database.database import Database


class ShowPasswordController:
    def __init__(self):
        self.db = Database("passwords")

    def show_password(self, password_uuid):
        password_data = self.db.find_one(str(password_uuid))
        if not password_data:
            return 'URL inválida'
        if password_data['views_left'] == 0:
            self.db.delete_one(str(password_uuid))
            return 'Visualizações esgotadas'
        if datetime.strptime(password_data['expires_at'], '%Y-%m-%d %H:%M:%S.%f') < datetime.utcnow():
            self.db.delete_one({'id': str(password_uuid)})
            return 'URL expirada'
        password = password_data['password']
        self.db.update_one(str(password_uuid), 'SET views_left = views_left - :val')
        return 'Sua senha é: ' + password
