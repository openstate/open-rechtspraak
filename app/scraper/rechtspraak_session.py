from requests import Response, Session
from requests.adapters import Retry
from requests_ratelimiter import LimiterAdapter


class RechtspraakScrapeSession(Session):
    """This class contains:
    - maximum of 3 retries
    - timeout of 2 seconds per request
    - backoff factor of 1 (.5s, 1s, 2s, 4s, 8s etc.)

    Hence, it has a maximum request time of 9.5s (3*2s + .5s + 1s + 2s).
    """

    def __init__(self) -> None:
        super().__init__()

        retries = Retry(
            total=3,
            backoff_factor=2,
            raise_on_status=False,
            status_forcelist=tuple(range(401, 600)),
        )
        adapter = LimiterAdapter(per_second=0.5, per_minute=30, burst=1, max_retries=retries)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    def request(self, *args: int, **kwargs: dict) -> Response:
        kwargs.setdefault("timeout", 2)
        return super().request(*args, **kwargs)
