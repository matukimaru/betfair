import requests


class Session:

    def __init__(self):
        credentials = []
        with open('../authentication/credentials.txt') as auth_file:
            for line in auth_file:
                credentials.append(line.strip())
        self.username = credentials[0]
        self.password = credentials[1]
        self.appkey = credentials[2]
        self.endpoint = 'https://identitysso-cert.betfair.com/api/certlogin'

    @property
    def payload(self):
        return 'username={}&password={}'.format(self.username, self.password)

    @property
    def headers(self):
        return {'X-Application': self.appkey, 'Content-Type': 'application/x-www-form-urlencoded'}

    @property
    def certificate(self):
        return '../resources/certificates/jamahello.crt', '../resources/certificates/jamahello.key'

    @property
    def token(self):
        response = requests.post(self.endpoint, data=self.payload, cert=self.certificate, headers=self.headers)
        if response.status_code != 200:
            return None
        else:
            print(response.json())
            return response.json()['sessionToken']
