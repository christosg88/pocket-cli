#!/usr/bin/env python3

from pocket_comm import Pocket
from pocket_prompt import PocketPrompt

if __name__ == "__main__":
    pocket = Pocket()
    pocket.authenticate()
    prompt = PocketPrompt(pocket)
    prompt.prompt()
