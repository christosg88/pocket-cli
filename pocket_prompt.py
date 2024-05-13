from datetime import datetime
from pocket_comm import PocketItem, Pocket
import readline
import shutil
import subprocess as sp
from urllib.parse import urlparse
from starter_program import OPEN_COMMAND
from tabulate import tabulate
from collections import defaultdict

def get_trimmed(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len]
    return s


class PocketPrompt:
    valid_commands = {
        "v": "[v]iew <index>",
        "d": "[d]elete <index>",
        "da": "[d]elete [a]ll",
        ".": "[.] domains",
        "vd": "[vd] <index>",
        "u": "[u]pdate",
        "l": "by [l]ength",
        "f": "[f]ilter <keyword>",
        "s": "[s]ort",
        "t": "[t]ag",
        "q": "[q]uit",
    }

    def __init__(self, pocket: Pocket):
        self.pocket: Pocket = pocket
        self.items: dict[str, PocketItem] = {}
        self.sort_by = 1

    def update(self):
        new_items = self.pocket.retrieve()
        if new_items is not None:
            self.items = new_items

    def sort_by_time_added(self, reverse=False) -> None:
        idx = 1
        for item in sorted(
            self.items.values(), key=lambda item: item.time_added, reverse=reverse
        ):
            item.sort_idx = idx
            idx += 1

    def sort_by_time_to_read(self, reverse=False) -> None:
        idx = 1
        for item in sorted(
            self.items.values(), key=lambda item: item.time_to_read, reverse=reverse
        ):
            item.sort_idx = idx
            idx += 1

    def display(self):
        if not self.items or len(self.items) == 0:
            print("\n\nNo items found\n\n")
            return

        match self.sort_by:
            case 1:
                self.sort_by_time_added()
            case 2:
                self.sort_by_time_added(reverse=True)
            case 3:
                self.sort_by_time_to_read()
            case 4:
                self.sort_by_time_to_read(reverse=True)

        headers = (
            "Index",
            "Domain Name",
            "Title",
            "URL",
            "Added",
            "Time to Read",
            "Word Count",
        )

        items = [(
            item.sort_idx,
            item.domain_name,
            item.given_title,
            item.given_url,
            datetime.fromtimestamp(item.time_added),
            item.time_to_read,
            item.word_count,
        ) for item in sorted(
            self.items.values(), key=lambda item: item.sort_idx, reverse=True)]

        num_columns = len(headers)
        max_len = [len(header) + 4 for header in headers]
        max_len[0] -= 1
        max_len[-1] -= 1
        for item in items:
            for i in (0, num_columns - 1):
                length = len(str(item[i])) + 1
                if max_len[i] < length:
                    max_len[i] = length

            for i in range(1, num_columns - 1):
                length = len(str(item[i])) + 2
                if max_len[i] < length:
                    max_len[i] = length

        term_cols, _ = shutil.get_terminal_size()
        remaining = term_cols - sum(max_len[:2]) - sum(max_len[4:]) - 4
        title_cols = min(max_len[2] - 2, remaining * 4 // 5)
        url_cols = remaining - title_cols
        max_len[2] = title_cols
        max_len[3] = url_cols
        for i in range(len(items)):
            item = items[i]
            items[i] = (
                item[0],
                item[1],
                get_trimmed(item[2], title_cols),
                get_trimmed(item[3], url_cols),
                item[4],
                item[5],
                item[6],
            )

        to_print = tabulate(items, headers=headers)
        lines = to_print.split("\n")
        print(to_print)
        print(lines[1])
        print(lines[0])
        print()

    def prompt_filter(self, match):
        self.items = dict(
            filter(
                lambda pair: match in pair[1].given_url or match in pair[1].given_title,
                self.items.items(),
            )
        )

    def prompt_domains(self):
        domains = defaultdict(int)
        for item in self.items.values():
            domain = urlparse(item.given_url).hostname
            domains[domain] += 1
        domains = list(domains.items())

        while True:
            for idx, (domain, count) in enumerate(domains, start=1):
                print(f"{idx}. {count}: {domain}")
            try:
                domain_idx = int(input("> "))
                if 1 <= domain_idx <= len(domains):
                    filter_domain = domains[domain_idx - 1][0]
                    break
                raise ValueError
            except ValueError:
                print("Invalid index\n")
                pass

        self.items = dict(
            filter(
                lambda pair: urlparse(pair[1].given_url).hostname ==
                filter_domain,
                self.items.items(),
            ))

    def prompt_length(self):
        # show possible groups of 5 minutes increment
        groups: set[int] = set()
        for item in self.items.values():
            groups.add(item.time_to_read // 5)

        groups = list(sorted(groups))
        while True:
            try:
                for idx, group in enumerate(groups, 1):
                    print(f"{idx}: {group * 5}–{(group + 1)*5} minutes")
                group_idx = int(input("> "))
                if 1 <= group_idx <= len(groups):
                    break
            except ValueError:
                pass

        min_time_to_read = groups[group_idx - 1] * 5
        max_time_to_read = (groups[group_idx - 1] + 1) * 5

        self.items = dict(
            filter(
                lambda pair: min_time_to_read
                <= pair[1].time_to_read
                < max_time_to_read,
                self.items.items(),
            )
        )

    def prompt_sort(self) -> None:
        while True:
            try:
                print("1: Oldest to Newest")
                print("2: Newest to Oldest")
                print("3: Shortest to Longest")
                print("4: Longest to Shortest")
                idx = int(input("> "))
                if 1 <= idx <= 4:
                    break
            except ValueError:
                pass
        self.sort_by = idx

    def get_cmd_and_idx(self):
        while True:
            tokens = input(
                "  |  ".join(PocketPrompt.valid_commands.values()) + " > "
            ).split()

            if not tokens:
                continue
            if tokens[0] not in PocketPrompt.valid_commands.keys():
                continue
            if tokens[0] in ("q", "u", "l", "s", "t") and len(tokens) != 1:
                continue
            if tokens[0] in ("v", "d", "vd", "f") and len(tokens) != 2:
                continue

            return tokens

    def prompt(self):
        self.update()
        self.display()

        while True:
            tokens = self.get_cmd_and_idx()
            cmd = tokens[0]

            match cmd:
                case "q":
                    return
                case "u":
                    self.update()
                    self.display()
                    continue
                case "l":
                    self.prompt_length()
                    self.display()
                    continue
                case ".":
                    self.prompt_domains()
                    self.display()
                    continue
                case "f":
                    match = tokens[1]
                    self.update()
                    if match:
                        self.prompt_filter(match)
                    self.display()
                    continue
                case "s":
                    self.prompt_sort()
                    self.display()
                    continue
                case "t":
                    self.update_tags()
                case "da":
                    for item_id in self.items.keys():
                        self.pocket.request_delete(item_id)
                    self.update()
                    self.display()
                    continue
                case _:
                    idx = int(tokens[1])

                    # search for the index
                    item_id = None
                    for k, v in self.items.items():
                        if v.sort_idx == idx:
                            item_id = k
                            break

                    if not item_id:
                        continue

                    match cmd:
                        case "v":
                            sp.Popen(
                                [OPEN_COMMAND, self.items[item_id].given_url],
                                stdout=sp.DEVNULL,
                                stderr=sp.DEVNULL,
                            )
                        case "d":
                            self.pocket.request_delete(item_id)
                            del self.items[item_id]
                            self.display()
                        case "vd":
                            sp.Popen(
                                [OPEN_COMMAND, self.items[item_id].given_url],
                                stdout=sp.DEVNULL,
                                stderr=sp.DEVNULL,
                            )
                            self.pocket.request_delete(item_id)
                            del self.items[item_id]
                            self.display()

    def update_tags(self):
        for item_id in self.items.keys():
            self.pocket.request_tags_clear(item_id)

        for item_id, item in self.items.items():
            self.pocket.request_tags_add(
                item_id, f"{item.get_grouped_time_to_read()}-min"
            )

        self.pocket.send_batched_requests()
