import json
import uuid
import firebase_admin
from firebase_admin import credentials, auth

credentials_path = '/path/downladed/in/firebase/credentials.json'

cred = credentials.Certificate(credentials_path)
FIRE_APP = firebase_admin.initialize_app(cred)


class FireApp():
    def __init__(self):
        self.error_reponses = dict()
        self.error_reponses['USER_CREATE_ERROR'] = "Failed to create user"
        self.error_reponses['EMAIL_EXISTS'] = "Email Already Exist."

    def create_user(self, username, first_name, last_name, email, password):
        user_data = dict()
        user_data['uid'] = username
        user_data['display_name'] = first_name + " " + last_name
        user_data['email'] = email
        user_data['password'] = password

        try:
            user_auth = auth.create_user(
                uid=user_data['uid'],
                display_name=user_data['display_name'],
                email=user_data['email'],
                password=user_data['password'], app=FIRE_APP)
        except auth.AuthError as e:
            cause = (e.detail.response._content).decode()
            self.error_reponse = dict()
            self.error_reponse['text'] = 'Failed to create user'
            self.error_reponse['code'] = e.code
            self.error_reponse['info'] = json.loads(
                cause)['error']['message']

            error_code = json.loads(
                cause)['error']['message']
            raise Exception(self.error_reponses[error_code])

        return user_auth

    def generate_custom_token(self, uid):
        custom_token = auth.create_custom_token(uid, app=FIRE_APP)
        return (custom_token).decode()

    def verify_token(self, token):
        decoded_token = auth.verify_id_token(token, app=FIRE_APP)
        uid = decoded_token['uid']

        return decoded_token
