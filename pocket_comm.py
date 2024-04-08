from pathlib import Path
from pprint import pformat
import json
import requests
import subprocess as sp
import sys
import itertools
from starter_program import OPEN_COMMAND


class PocketItem:
    sort_idx: int
    item_id: str
    domain_name: str
    given_title: str
    given_url: str
    time_added: int
    time_to_read: int
    word_count: int

    WORDS_PER_MINUTE = 214

    def __init__(
        self,
        item_id: str,
        domain_name: str,
        given_title: str,
        given_url: str,
        time_added: str,
        time_to_read: str,
        word_count: str,
    ):
        self.sort_idx = 0
        self.item_id = item_id
        self.domain_name = domain_name
        self.given_title = given_title
        self.given_url = given_url
        self.time_added = int(time_added)
        self.time_to_read = self.get_time_to_read(int(word_count))
        self.word_count = int(word_count)

    @staticmethod
    def get_time_to_read(word_count: int):
        return int(round(word_count / PocketItem.WORDS_PER_MINUTE))

    def get_grouped_time_to_read(self):
        for limit in itertools.chain((1, 2), range(5, 1000, 5)):
            if self.time_to_read <= limit:
                return limit


class Pocket:
    POCKET_ACCESS_TOKEN_FILE = Path.home() / ".pocket"
    # you get this from Pocket after creating a new app
    CONSUMER_KEY = "104395-a466587cb5dfff975b68a80"
    REDIRECT_URI = "http://example.com/"

    def __init__(self):
        self.access_token = None
        self.username = None
        self.items = dict()
        self.batched_actions = []

    def authenticate(self):
        self.access_token, self.username = self.get_access_token_and_username()

    def send_request(self, pocket_uri: str, data: dict) -> dict:
        headers = {"X-Accept": "application/json"}
        r = requests.post(
            f"https://getpocket.com/{pocket_uri}",
            headers=headers,
            json=data,
        )
        if r.status_code != 200:
            print(
                f"Request failed with status code {r.status_code}",
                file=sys.stderr,
            )
            raise RuntimeError(pformat(dict(r.headers)))
        return r.json()

    def send_batched_requests(self) -> None:
        batched_send_requests = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "access_token": self.access_token,
            "actions": self.batched_actions,
        }
        r = requests.post(
            "https://getpocket.com/v3/send",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "X-Accept": "application/json",
            },
            json=batched_send_requests,
        )
        if r.status_code != 200:
            print(
                f"Request failed with status code {r.status_code}",
                file=sys.stderr,
            )
            raise RuntimeError(pformat(dict(r.headers)))
        self.batched_actions.clear()
        return r.json()

    def get_access_token_and_username(self) -> tuple[str, str]:
        # if we already have it stored in file, load it and return it
        if Pocket.POCKET_ACCESS_TOKEN_FILE.is_file():
            with open(Pocket.POCKET_ACCESS_TOKEN_FILE, "r") as infile:
                d = json.load(infile)
                return d["access_token"], d["username"]

        # else open a browser and proceed with the authorization process
        request_token = self.get_request_token()
        self.redirect_to_authorization(request_token)
        d = self.request_access_token(request_token)
        with open(Pocket.POCKET_ACCESS_TOKEN_FILE, "w") as outfile:
            json.dump(d, outfile)
        return d["access_token"], d["username"]

    def get_request_token(self):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "redirect_uri": Pocket.REDIRECT_URI,
        }
        return self.send_request("v3/oauth/request", data)["code"]

    def redirect_to_authorization(self, request_token):
        sp.run(
            [
                OPEN_COMMAND,
                (
                    "https://getpocket.com/auth/authorize"
                    f"?request_token={request_token}"
                    f"&redirect_uri={Pocket.REDIRECT_URI}"
                ),
            ]
        )
        input('Click "Authorize" on the window that opened, and then press Enter')

    def request_access_token(self, request_token):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "code": request_token,
        }
        return self.send_request("v3/oauth/authorize", data)

    def retrieve(
        self,
        state=None,
        favorite=None,
        tag=None,
        content_type=None,
        sort=None,
        detail_type=None,
        search=None,
        domain=None,
        since=None,
        count=None,
        offset=None,
    ) -> dict[str, PocketItem]:
        data = {"consumer_key": Pocket.CONSUMER_KEY, "access_token": self.access_token}
        if state:
            if state not in ("unread", "archive", "all"):
                raise RuntimeError(
                    f"Invalid option {state=} (valid options: unread, archive, all)"
                )
            data["state"] = state
        if favorite:
            if favorite not in ("0", "1"):
                raise RuntimeError(f"Invalid option {favorite=} (valid options: 0, 1)")
            data["favorite"] = favorite
        if tag:
            data["tag"] = tag
        if content_type:
            if content_type not in ("article", "video", "image"):
                raise RuntimeError(
                    f"Invalid option {content_type=} (valid options: article, video, image)"
                )
            data["contentType"] = content_type
        if sort:
            if state not in ("newest", "oldest", "title", "site"):
                raise RuntimeError(
                    f"Invalid option {sort=} (valid options: newest, oldest, title, site)"
                )
            data["sort"] = sort
        if detail_type:
            if detail_type not in ("simple", "complete"):
                raise RuntimeError(
                    f"Invalid option {detail_type=} (valid optiond: simple, complete)"
                )
            data["detailType"] = detail_type
        if search:
            data["search"] = search
        if domain:
            data["domain"] = domain
        if since:
            data["since"] = since
        if count:
            if int(count) < 1:
                raise RuntimeError(f"Invalid option {count=} (valid options: > 0)")
            data["count"] = count
        if offset:
            if int(offset) < 1:
                raise RuntimeError(f"Invalid option {offset=} (valid options: > 0)")
            data["offset"] = offset

        r_json = self.send_request("v3/get", data)

        if not r_json["list"]:
            return

        items = dict()
        for item_id, data in r_json["list"].items():
            items[item_id] = PocketItem(
                item_id,
                data.get("domain_metadata", {}).get("name", "N/A"),
                data.get("given_title", "N/A"),
                data.get("given_url", "N/A"),
                data.get("time_added", "N/A"),
                data.get("time_to_read", "0"),
                data.get("word_count", "0"),
            )

        return items

    def request_delete(self, item_id):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "access_token": self.access_token,
            "actions": [{"action": "delete", "item_id": item_id}],
        }
        self.send_request("v3/send", data)

    def request_tags_add(self, item_id: str, tags: str):
        """
        Add one or more tags to an item.

        item_id: The id of the item to perform the action on.
        tags: A comma-delimited list of one or more tags.
        """

        self.batched_actions.append(
            {"action": "tags_add", "item_id": item_id, "tags": tags}
        )

    def request_tags_clear(self, item_id: str):
        """
        Remove all tags from an item.

        item_id: The id of the item to perform the action on.
        tags: A comma-delimited list of one or more tags.
        """

        self.batched_actions.append({"action": "tags_clear", "item_id": item_id})
