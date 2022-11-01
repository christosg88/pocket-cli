from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from pprint import pformat
from tabulate import tabulate
import json
import readline
import requests
import subprocess as sp
import sys


class PocketItem:
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

    def get_given_title(self, max_width=60):
        if len(self.given_title) <= max_width:
            return self.given_title
        else:
            return self.given_title[: max_width - 2] + "..."

    def get_given_url(self, max_width=60):
        if len(self.given_url) <= max_width:
            return self.given_url
        else:
            return self.given_url[: max_width - 2] + "..."

    @staticmethod
    def get_time_to_read(word_count: int):
        return int(round(word_count / PocketItem.WORDS_PER_MINUTE))


class Pocket:
    POCKET_ACCESS_TOKEN_FILE = Path.home() / ".pocket"
    # you get this from Pocket after creating a new app
    CONSUMER_KEY = "104395-a466587cb5dfff975b68a80"
    REDIRECT_URI = "http://example.com/"

    valid_commands = {
        "v": "[v]iew <index>",
        "d": "[d]elete <index>",
        "vd": "[vd] <index>",
        "u": "[u]pdate",
        "s": "[s]tatistics",
        "q": "[q]uit",
    }

    def __init__(self):
        self.access_token = None
        self.username = None
        self.since = "0"
        self.items = dict()

    def authenticate(self):
        self.access_token, self.username = self.__get_access_token_and_username()

    def prompt(self):
        self.__retrieve()
        self.__display()

        while True:
            tokens = self.__get_cmd_and_idx()
            cmd = tokens[0]

            if cmd == "q":
                return
            elif cmd == "u":
                self.__retrieve()
                self.__display()
            elif cmd == "s":
                self.__show_statistics()
            else:
                idx = int(tokens[1])

                # search for the index
                item_id = None
                for k, v in self.items.items():
                    if v.sort_idx == idx:
                        item_id = k
                        break

                if not item_id:
                    continue

                if cmd == "v":
                    sp.Popen(
                        ["xdg-open", self.items[item_id].given_url],
                        stdout=sp.DEVNULL,
                        stderr=sp.DEVNULL,
                    )
                elif cmd == "d":
                    self.__delete(item_id)
                    del self.items[item_id]
                    self.__display()
                elif cmd == "vd":
                    sp.Popen(
                        ["xdg-open", self.items[item_id].given_url],
                        stdout=sp.DEVNULL,
                        stderr=sp.DEVNULL,
                    )
                    self.__delete(item_id)
                    del self.items[item_id]
                    self.__display()

    def __send_request(self, pocket_uri: str, data: dict) -> dict:
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

    def __get_access_token_and_username(self):
        if Pocket.POCKET_ACCESS_TOKEN_FILE.is_file():
            with open(Pocket.POCKET_ACCESS_TOKEN_FILE, "r") as infile:
                d = json.load(infile)
                return d["access_token"], d["username"]
        else:
            request_token = self.__get_request_token()
            self.__redirect_to_authorization(request_token)
            d = self.__request_access_token(request_token)
            with open(Pocket.POCKET_ACCESS_TOKEN_FILE, "w") as outfile:
                json.dump(d, outfile)

        return d["access_token"], d["username"]

    def __get_request_token(self):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "redirect_uri": Pocket.REDIRECT_URI,
        }
        return self.__send_request("v3/oauth/request", data)["code"]

    def __redirect_to_authorization(self, request_token):
        sp.run(
            [
                "xdg-open",
                (
                    "https://getpocket.com/auth/authorize?request_token=",
                    request_token,
                    "&redirect_uri=",
                    Pocket.REDIRECT_URI,
                ),
            ]
        )
        input('Click "Authorize" on the window that opened, and then press Enter')

    def __request_access_token(self, request_token):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "code": request_token,
        }
        return self.__send_request("v3/oauth/authorize", data)

    def __get_cmd_and_idx(self):
        while True:
            tokens = input("  |  ".join(Pocket.valid_commands.values()) + " > ").split()

            if not tokens:
                continue
            if tokens[0] not in Pocket.valid_commands.keys():
                continue
            if tokens[0] in ("u", "q") and len(tokens) != 1:
                continue
            if tokens[0] in ("v", "d", "vd") and len(tokens) != 2:
                continue

            return tokens

    def __display(self):
        # split into groups of 5 minutes increment
        groups = defaultdict(list)
        for data in self.items.values():
            groups[data.time_to_read // 5].append(data)

        for k in sorted(groups.keys()):
            groups[k] = sorted(groups[k], key=lambda v: v.time_added)

        idx = 1
        for k, v in sorted(groups.items()):
            for item in v:
                item.sort_idx = idx
                idx += 1

        for minutes, items in sorted(groups.items(), reverse=True):
            print("=" * 5 + f" {minutes * 5}–{(minutes + 1)*5} minutes " + "=" * 5)
            print(
                tabulate(
                    (
                        (
                            item.sort_idx,
                            item.domain_name,
                            item.get_given_title(),
                            item.get_given_url(),
                            date.fromtimestamp(item.time_added),
                            item.time_to_read,
                            item.word_count,
                        )
                        for item in reversed(items)
                    ),
                    headers=(
                        "Index",
                        "Domain Name",
                        "Title",
                        "URL",
                        "Added",
                        "Time to Read",
                        "Word Count",
                    ),
                )
            )
            print()

    def __show_statistics(self):
        word_count_per_group = defaultdict(list)
        for data in self.items.values():
            word_count_per_group[data.time_to_read // 5].append(data.word_count)

        num_tot_items = 0
        num_tot_min_to_read = 0

        for group_minutes, minutes in sorted(
            word_count_per_group.items(), reverse=True
        ):
            num_items = len(minutes)
            num_tot_items += num_items
            num_min_to_read = PocketItem.get_time_to_read(sum(minutes))
            num_tot_min_to_read += num_min_to_read

            print(
                "=" * 5
                + f" {group_minutes * 5}–{(group_minutes + 1)*5} minutes "
                + "=" * 5
            )
            print(f"#items: {num_items}")
            print(f"time to read: {timedelta(minutes=num_min_to_read)}")
            print()

        print("=" * 5 + f" TOTAL " + "=" * 5)
        print(f"#items: {num_tot_items}")
        print(f"time to read: {timedelta(minutes=num_tot_min_to_read)}")
        print()

    def __retrieve(
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
    ):
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
        else:
            data["since"] = self.since
        if count:
            if int(count) < 1:
                raise RuntimeError(f"Invalid option {count=} (valid options: > 0)")
            data["count"] = count
        if offset:
            if int(offset) < 1:
                raise RuntimeError(f"Invalid option {offset=} (valid options: > 0)")
            data["offset"] = offset

        r_json = self.__send_request("v3/get", data)

        if "list" not in r_json.keys():
            print(
                f"Nothing new since {date.fromtimestamp(self.since)} until {date.fromtimestamp(r_json['since'])}"
            )
            self.since = r_json["since"]
            return

        for item_id, data in r_json["list"].items():
            if item_id in self.items.keys():
                if data["status"] == "2":
                    del self.items[item_id]
                continue

            self.items[item_id] = PocketItem(
                item_id,
                data.get("domain_metadata", {}).get("name", "N/A"),
                data.get("given_title", "N/A"),
                data.get("given_url", "N/A"),
                data.get("time_added", "N/A"),
                data.get("time_to_read", "0"),
                data.get("word_count", "0"),
            )

    def __delete(self, item_id):
        data = {
            "consumer_key": Pocket.CONSUMER_KEY,
            "access_token": self.access_token,
            "actions": [{"action": "delete", "item_id": item_id}],
        }
        self.__send_request("v3/send", data)
