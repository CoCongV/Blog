from flask import g

from app.api_v1 import BaseResource


class Token(BaseResource):

    def get(self):
        if g.current_user is None or g.token_used:
            return {"message": "Invalid credentials"},
        return {
            "token": g.current_user.generate_confirm_token(),
            "expiration": 86400
        }, self.SUCCESS
