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
* `[d]elete [a]ll` items
* `[.] domains` filtering
* `[vd]` (view and delete) an item at the same time
* `[l]ength` show only items in a length group
* `[f]ilter` the items by keyword
* `[s]ort` the items based on reading time or time added
* `[t]ag` the items with the needed time to read

Viewing an item will open the link to your default browser.

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
     20  Ars Technica   The future exists now: Bringing William Gibson’s The Peripheral to televisi  https://arstechnica.com/?p=1891572  2022-11-12 10:21:51              11          2306
     19  Ars Technica   Biotechnology is creating ethical worries—and we’ve been here before         https://arstechnica.com/?p=1893728  2022-10-30 09:33:43              10          2247
     18  Ars Technica   Coinbase users scammed out of $21M in crypto sue company for negligence      https://arstechnica.com/?p=1890656  2022-10-18 13:58:31              10          2116
     17  Ars Technica   No fix in sight for mile-wide loophole plaguing a key Windows defense for y  https://arstechnica.com/?p=1887240  2022-10-06 14:20:55              10          2043
     16  Ars Technica   Meta disrupted China-based propaganda machine before it reached many Americ  https://arstechnica.com/?p=1885001  2022-09-28 09:00:04              12          2640
     15  Ars Technica   How electric cars could rescue the US power grid                             https://arstechnica.com/?p=1882783  2022-09-21 09:25:56              10          2067
     14  Ars Technica   The Big Bang should have made cracks in spacetime—why haven’t we found them  https://arstechnica.com/?p=1871473  2022-09-21 09:25:02              15          3117
     13  Ars Technica   Why are hard drive companies investing in DNA data storage?                  https://arstechnica.com/?p=1881626  2022-09-19 14:18:21              10          2081
     12  Ars Technica   Punishment, puppies, and science: Bringing dog training to heel              https://arstechnica.com/?p=1881676  2022-09-19 14:12:19              15          3138
     11  Ars Technica   Cloudflare explains why Kiwi Farms was its most dangerous customer ever      https://arstechnica.com/?p=1879770  2022-09-09 09:57:52              12          2587
     10  Ars Technica   Cheap, high capacity, and fast: New aluminum battery tech promises it all    https://arstechnica.com/?p=1875891  2022-08-27 20:02:36              10          2177
      9  Ars Technica   Should we be trying to create a circular urine economy?                      https://arstechnica.com/?p=1874923  2022-08-21 13:59:28              11          2259
      8  Ars Technica   Solving the rock-hard problem of nuclear waste disposal                      https://arstechnica.com/?p=1872652  2022-08-18 08:54:00              18          3926
      7  Ars Technica   De-extinction company sets its next (first?) target: The thylacine           https://arstechnica.com/?p=1873897  2022-08-17 07:39:48              12          2472
      6  Ars Technica   Man who built ISP instead of paying Comcast $50K expands to hundreds of hom  https://arstechnica.com/?p=1872522  2022-08-10 23:37:25              10          2230
      5  Ars Technica   Locked-in syndrome and the misplaced presumption of misery                   https://arstechnica.com/?p=1872126  2022-08-09 21:52:04              15          3217
      4  Ars Technica   How Tor is fighting—and beating—Russian censorship                           https://arstechnica.com/?p=1870005  2022-07-30 01:08:15              10          2105
      3  Ars Technica   Discovery of new UEFI rootkit exposes an ugly truth: The attacks are invisi  https://arstechnica.com/?p=1869307  2022-07-26 23:07:56              12          2571
      2  Ars Technica   Nuclear power plants are struggling to stay cool                             https://arstechnica.com/?p=1868886  2022-07-23 10:04:19              10          2195
      1  Ars Technica   Electric cars are doomed if fast charger reliability doesn’t get better      https://arstechnica.com/?p=1866587  2022-07-14 16:09:25              10          2101
-------  -------------  ---------------------------------------------------------------------------  ----------------------------------  -------------------  --------------  ------------
  Index  Domain Name    Title                                                                        URL                                 Added                  Time to Read    Word Count

[v]iew <index>  |  [d]elete <index>  |  [d]elete [a]ll  |  [.] domains  |  [vd] <index>  |  [u]pdate  |  by [l]ength  |  [f]ilter <keyword>  |  [s]ort  |  [t]ag  |  [q]uit >
```

# Ideas/Bugs

Any ideas for improvement or bugs found are welcome. Please open a GitHub Issue.
