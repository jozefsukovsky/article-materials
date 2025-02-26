from django.contrib.sessions.backends.db import SessionStore as DBStore
from .models import PublicSession


class SessionStore(DBStore):

    @classmethod
    def get_model_class(cls):
        return PublicSession
