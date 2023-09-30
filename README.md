# A Pocket CLI (Command Line Interface) to view and modify your Pocket list from the terminal

`pocket-cli` uses Python 3 `requests` to communicate with Pocket's API, to retrieve your list of saved-for-later items,
and displays them on the terminal.

The first time you run `pocket-cli`, it will authenticate you by making a request to your Pocket account. A browser
window will open (if you're not signed into Pocket it will ask you to sign-iin first), and you will be asked if you want
to allow `pocket-cli` to access your Pocket list.

After you have authorized `pocket-cli` to access your list, it will store your access token into `~/.pocket` for future
use.

Through `pocket-cli`'s prompt, you can:

* `[v]iew` an item
* `[d]elete` an item
* `[vd]` (view and delete) an item at the same time
* `[f]ilter` the items based on reading time or time added
* `[s]ort` the items based on reading time or time added
* `[t]ag` the items with the needed time to read

Viewing an item will open the link to your default browser through `xdg-open`.

Deleting an item will synchronize the change to your Pocket list.

# How to run

After you clone the repo, you can either run `pocket-cli.py` directly, or recreate it like so:

```python3
#!/usr/bin/env python3

from pocket_comm import Pocket
from pocket_prompt import PocketPrompt

if __name__ == "__main__":
    pocket = Pocket()
    pocket.authenticate()
    prompt = PocketPrompt(pocket)
    prompt.prompt()
```

The `authenticate()` function will make all the necessary steps to authenticate you to pocket, asking for access the
first time, or using the stored access token for subsequent runs.

The `prompt()` function will display a tabulated list of your items. The prompt line will ask you which operation you'd
like to perform.

Here's a truncated example using my list:

```
     20  Ars Technica    US government slams Musk in court filing  https://arstechnica.com/?p=1967364        2023-09-12 21:44:10              11          2404
                         describing “chaotic environment” a
     19  Ars Technica    For the first time, research reveals      https://arstechnica.com/?p=1967439        2023-09-13 22:56:04               8          1775
                         crows use statistical logic
     18  Ars Technica    What would it take to build a self-       https://arstechnica.com/?p=1967156        2023-09-13 22:56:34              18          3810
                         sustaining astronaut ecosystem on Mars?
     17  Ars Technica    Google quietly corrects previously        https://arstechnica.com/?p=1971345        2023-09-27 08:26:27               2           465
                         submitted disclosure for critical webp 0
     16  Ars Technica    GPUs from all major suppliers are         https://arstechnica.com/?p=1971213        2023-09-27 08:28:09              11          2282
                         vulnerable to new pixel-stealing attack
     15  Ars Technica    Can you melt eggs? Quora’s AI says        https://arstechnica.com/?p=1971106        2023-09-27 08:28:32               3           729
                         “yes,” and Google is sharing the result
     14  Ars Technica    Musk’s X spreads more disinformation      https://arstechnica.com/?p=1971598        2023-09-27 23:27:26               7          1449
                         than rival social networks, EU says
     13  Ars Technica    Backdoored firmware lets China state      https://arstechnica.com/?p=1971587        2023-09-27 23:27:58               7          1459
                         hackers control routers with “magic pa
     12  Ars Technica    Einstein right again: Antimatter falls    https://arstechnica.com/?p=1971331        2023-09-27 23:28:52               7          1580
                         “down” due to gravity like ordinary
     11  Ars Technica    How climate change could make fungal      https://arstechnica.com/?p=1971382        2023-09-27 23:29:04              13          2748
                         diseases worse
     10  Ars Technica    We try out the first legal level 3        https://arstechnica.com/?p=1971280        2023-09-27 23:29:12               7          1530
                         automated driving system in the US
      9  Ars Technica    “Yeah, they’re gone”: Musk confirms cuts  https://arstechnica.com/?p=1971902        2023-09-28 20:54:16               3           742
                         to X’s election integrity team
      8  Ars Technica    Reddit blocks opting out of personalized  https://arstechnica.com/?p=1971837        2023-09-28 20:54:21               4           792
                         ads, starts paying users
      7  Ars Technica    AI is getting better at hurricane         https://arstechnica.com/?p=1971778        2023-09-28 20:55:24               8          1752
                         forecasting
      6  Ars Technica    Our 10-point scale will help you rate     https://arstechnica.com/?p=1970465        2023-09-28 20:55:33              13          2835
                         the biggest misinformation purveyors
      5  France 24       French government launches battle plan    https://www.france24.com/en/france/20230  2023-09-29 13:57:54               1           282
                         against bedbug invasion                   929-french-government-launches-battle-
                                                                   plan-against-bedbug-invasion
      4  Ars Technica    US agency sues Tesla as Black workers     https://arstechnica.com/?p=1972215        2023-09-30 11:57:17               7          1577
                         report “swastikas, threats, and noose
      3  Ars Technica    SCOTUS to decide if Florida and Texas     https://arstechnica.com/?p=1972299        2023-09-30 11:58:17               7          1551
                         social media laws violate 1st Amendme
      2  Ars Technica    “No choice at all”: Pharma companies      https://arstechnica.com/?p=1972343        2023-09-30 11:58:29               3           694
                         begrudgingly agree to negotiate prices
      1  Ars Technica    DOJ finally posted that “embarrassing”    https://arstechnica.com/?p=1972364        2023-09-30 11:58:37               3           538
                         court doc Google wanted to hide
-------  --------------  ----------------------------------------  ----------------------------------------  -------------------  --------------  ------------
  Index  Domain Name     Title                                     URL                                       Added                  Time to Read    Word Count

[v]iew <index>  |  [d]elete <index>  |  [vd] <index>  |  [u]pdate  |  [f]ilter  |  [s]ort  |  [t]ag  |  [q]uit >
```

# Ideas/Bugs

Any ideas for improvement or bugs found are welcome. Please open a GitHub Issue.
