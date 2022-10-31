#!/usr/bin/env python3

from pocket import Pocket

if __name__ == "__main__":
    pocket = Pocket()
    pocket.authenticate()
    pocket.prompt()
