import logging
import requests
from requests import Response, RequestException, Session


class BaseClient:
    def __init__(self, session: Session = None):
        self.session = session or requests.Session()
        self.logger = logging.getLogger(__name__)

    def send_request(
            self,
            method: str,
            url: str,
            params = None,
            headers = None,
            json = None,
            data = None,
            files = None,
            timeout: int = 30
    ) -> Response:

        self.logger.info(f"==> Sending: {method.upper()} {url}")
        if params: self.logger.info(f"==> Params: {params}")
        if headers: self.logger.info(f"==> Headers: {headers}")
        if json: self.logger.info(f"==> JSON: {json}")
        if data: self.logger.info(f"==> Data: {data}")
        if timeout: self.logger.info(f"==> Timeout: {timeout}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json,
                data=data,
                files=files,
                timeout=timeout
            )

            if response.status_code:
                self.logger.info(f"<== Response status: {response.status_code}")

            try:
                self.logger.info(f"<== Response body: {response.json()}")

            except:
                self.logger.info(f"<== Response body: {response.text[:800]}")

            if response.headers:
                self.logger.info(f"<== Response headers: {response.headers}")

            return response


        except RequestException as e:
            self.logger.error(f"❌ Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response body: {e.response.text[:800]}")

            raise