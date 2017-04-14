from config import OAUTH_CREDENTIALS
from flask import url_for, redirect, request
from rauth import OAuth2Service
import json


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = OAUTH_CREDENTIALS[provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.consumer_authorize_url = credentials['authorize_url']
        self.consumer_access_token_url = credentials['access_token_url']
        self.consumer_base_url = credentials['base_url']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name=self.provider_name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=self.consumer_authorize_url,
            access_token_url=self.consumer_access_token_url,
            base_url=self.consumer_base_url
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None

        def new_decoder(payload):
            return json.loads(payload.decode('utf-8'))

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=new_decoder,
        )
        me = oauth_session.get('me', params={'fields': 'id,name,email'}).json()
        social_id = 'facebook$' + me.get('id')
        name = me.get('name') or ''
        email = me.get('email') or ''
        return (
            social_id,
            name,
            email
        )

