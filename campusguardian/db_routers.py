# db_routers.py
class BlockAuthRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['auth', 'admin', 'sessions', 'contenttypes']:
            return False
        return None