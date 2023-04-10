from collections import defaultdict
from datetime import datetime, timedelta
from pocket_comm import PocketItem, Pocket
from tabulate import tabulate
import readline
import subprocess as sp


class PocketPrompt:
    valid_commands = {
        "v": "[v]iew <index>",
        "d": "[d]elete <index>",
        "vd": "[vd] <index>",
        "u": "[u]pdate",
        "f": "[f]ilter",
        "q": "[q]uit",
    }

    def __init__(self, pocket: Pocket):
        self.pocket: Pocket = pocket
        self.items: dict[str, PocketItem] = None

    def update(self):
        new_items = self.pocket.retrieve()
        if new_items is not None:
            self.items = new_items

    def display(self):
        idx = 1
        for k, v in sorted(self.items.items()):
            v.sort_idx = idx
            idx += 1

        to_print = tabulate(
            (
                (
                    item.sort_idx,
                    item.domain_name,
                    item.given_title,
                    item.given_url,
                    datetime.fromtimestamp(item.time_added),
                    item.time_to_read,
                    item.word_count,
                )
                for item in sorted(
                    self.items.values(), key=lambda item: item.sort_idx, reverse=True
                )
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
            maxcolwidths=40,
        )
        lines = to_print.split("\n")
        print(to_print)
        print(lines[1])
        print(lines[0])
        print()

    def prompt_filter(self):
        # show possible groups of 5 minutes increment
        groups: set[int] = set()
        for item in self.items.values():
            groups.add(item.time_to_read // 5)

        groups = list(sorted(groups))
        for idx, group in enumerate(groups, 1):
            print(f"{idx}: {group * 5}–{(group + 1)*5}")
        group_idx = int(input("> "))

        min_time_to_read = groups[group_idx - 1] * 5
        max_time_to_read = (groups[group_idx - 1] + 1) * 5

        self.items = dict(
            filter(
                lambda pair: min_time_to_read
                <= pair[1].time_to_read
                <= max_time_to_read,
                self.items.items(),
            )
        )

    def get_cmd_and_idx(self):
        while True:
            tokens = input(
                "  |  ".join(PocketPrompt.valid_commands.values()) + " > "
            ).split()

            if not tokens:
                continue
            if tokens[0] not in PocketPrompt.valid_commands.keys():
                continue
            if tokens[0] in ("u", "q", "s", "f") and len(tokens) != 1:
                continue
            if tokens[0] in ("v", "d", "vd") and len(tokens) != 2:
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
                case "f":
                    self.update()
                    self.prompt_filter()
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
                                ["xdg-open", self.items[item_id].given_url],
                                stdout=sp.DEVNULL,
                                stderr=sp.DEVNULL,
                            )
                        case "d":
                            self.pocket.request_delete(item_id)
                            del self.items[item_id]
                            self.display()
                        case "vd":
                            sp.Popen(
                                ["xdg-open", self.items[item_id].given_url],
                                stdout=sp.DEVNULL,
                                stderr=sp.DEVNULL,
                            )
                            self.pocket.request_delete(item_id)
                            del self.items[item_id]
                            self.display()
