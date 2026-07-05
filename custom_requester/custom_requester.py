class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.session.headers.update(self.base_headers)

    def send_request(self, method, endpoint, data=None):
        url = f'{self.base_url}{endpoint}'
        response = self.session.request(method, url, json=data)
        return response