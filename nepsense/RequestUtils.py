import requests


class RequestAdapter:
    def __init__(self, tls_verification=False, headers={}, base_url="https://nepalstock.com"):
        self.tls_verification = tls_verification
        self.alt_headers = headers
        self.base_url = base_url

    def get(self, url, include_authorization_headers=True, headers={}):
        headers = headers or self.alt_headers

        # if include_authorization_headers:
        #     headers = self.get_authorization_headers()

        response = requests.get(url, headers=headers, verify=self.tls_verification)
        return response
