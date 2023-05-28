from requests import Session
from requests.adapters import HTTPAdapter, Retry


class RechtspraakScrapeSession(Session):
    """
    This class contains:
    - maximum of 3 retries
    - timeout of 2 seconds per request
    - backoff factor of 1 (.5s, 1s, 2s, 4s, 8s etc.)

    Hence, it has a maximum request time of 9.5s (3*2s + .5s + 1s + 2s).
    """

    def __init__(self):
        super().__init__()
        retries = Retry(
            total=3,
            backoff_factor=2,
            raise_on_status=False,
            status_forcelist=tuple(range(401, 600)),
        )
        self.mount("http://", HTTPAdapter(max_retries=retries))
        self.mount("https://", HTTPAdapter(max_retries=retries))

    def request(self, *args, **kwargs):
        kwargs.setdefault("timeout", 2)
        return super(RechtspraakScrapeSession, self).request(*args, **kwargs)
