# A Pocket CLI (Command Line Interface) to view and modify your Pocket list from the terminal

`pocket-cli` uses Python 3 `requests` to communicate with Pocket's API, to retrieve your list of saved-for-later items,
and displays them on the terminal.

The first time you run `pocket-cli`, it will authenticate you by making a request to your Pocket account. A browser
window will open (if you're not signed into Pocket it will ask you to sign-iin first), and you will be asked if you want
to allow `pocket-cli` to access your Pocket list.

After you have authorized `pocket-cli` to access your list, it will store your access token into `~/.pocket` for future
use.

Through `pocket-cli`'s prompt, you can `[v]iew` an item, `[d]elete` an item or `[vd]` (view and delete) an item at the
same time.

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
     25  Ars Technica   Won’t somebody please think of the        https://arstechnica.com/?p=1913921        2023-02-05 09:51:08               2           482
                        insects?!
     24  Ars Technica   New data illustrates time’s effect on     https://arstechnica.com/?p=1914056        2023-02-05 09:51:21               2           470
                        hard drive failure rates
     23  Ars Technica   Musk locks his Twitter account to         https://arstechnica.com/?p=1914026        2023-02-05 09:52:18               4           815
                        personally test reported malfunction
     22  Ars Technica   Apple’s focus on secrecy violated         https://arstechnica.com/?p=1913818        2023-02-05 10:02:18               2           496
                        employee rights, US regulators find
     21  Ars Technica   US still has the worst, most expensive    https://arstechnica.com/?p=1913812        2023-02-05 10:02:33               4           839
                        health care of any high-income count
     20  Ars Technica   How to tell if your cats are playing or   https://arstechnica.com/?p=1913275        2023-02-05 10:02:42               4           922
                        fighting—and whether it’s a problem
     19  Ars Technica   GitHub says hackers cloned code-signing   https://arstechnica.com/?p=1913534        2023-01-31 13:37:45               2           447
                        certificates in breached repository
     18  Ars Technica   MusicLM: Google AI generates music in     https://arstechnica.com/?p=1913289        2023-01-31 13:37:39               3           634
                        various genres at 24 kHz
     17  Ars Technica   Man wanted for attempted murder is using  https://arstechnica.com/?p=1913479        2023-01-31 13:37:04               3           747
                        dating apps while on the run, cops
     16  Ars Technica   Charter settles with family of murder     https://arstechnica.com/?p=1913433        2023-01-31 13:36:58               3           700
                        victim, says insurance will cover it
     15  Ars Technica   COVID is still a global health            https://arstechnica.com/?p=1913458        2023-01-31 13:36:55               3           620
                        emergency, but end may be near, WHO says
     14  Ars Technica   Massive Yandex code leak reveals Russian  https://arstechnica.com/?p=1913325        2023-01-31 13:36:36               3           553
                        search engine’s ranking factors
     13  Ars Technica   Renault and Nissan hammer out historic    https://arstechnica.com/?p=1913381        2023-01-31 13:36:18               4           788
                        deal to salvage alliance
     12  France 24      Raising retirement age to 64 'is now      https://www.france24.com/en/europe/20230  2023-01-31 13:39:06               2           470
                        non-negotiable' says French PM Borne a    129-france-s-legal-retirement-age-is-
                                                                  now-non-negotiable-says-pm-borne-as-
                                                                  strikes-loom
     11  Ars Technica   DirecTV dumps Newsmax instead of paying   https://arstechnica.com/?p=1912543        2023-01-26 16:05:17               4           829
                        new fee, drawing Republican outrage
     10  Ars Technica   RNC sued Google for filtering spam but    https://arstechnica.com/?p=1912471        2023-01-26 16:04:48               3           574
                        never used Gmail tool that bypasses
      9  Ars Technica   Manchin writes bill to stop temporary     https://arstechnica.com/?p=1912422        2023-01-26 16:04:01               3           591
                        electric vehicle tax credits
      8  briankrebs     Administrator of RSOCKS Proxy Botnet      https://krebsonsecurity.com/2023/01/admi  2023-01-25 12:22:22               3           696
                        Pleads Guilty                             nistrator-of-rsocks-proxy-botnet-pleads-
                                                                  guilty/
      7  Ars Technica   For Facebook addicts, clicking is more    https://arstechnica.com/?p=1911786        2023-01-24 10:08:38               4           895
                        important than facts or ideology
      6  Ars Technica   Archaeologists discovered a new papyrus   https://arstechnica.com/?p=1911466        2023-01-22 10:49:22               3           735
                        of Egyptian Book of the Dead
      5  Ars Technica   Twitter retroactively changes developer   https://arstechnica.com/?p=1911442        2023-01-21 19:34:20               2           455
                        agreement to ban third-party client
      4  Ars Technica   Musk oversaw staged Tesla self-driving    https://arstechnica.com/?p=1911445        2023-01-21 19:34:25               3           645
                        video, emails show
      3  briankrebs     New T-Mobile Breach Affects 37 Million    https://krebsonsecurity.com/2023/01/new-  2023-01-24 10:13:18               4           944
                        Accounts                                  t-mobile-breach-affects-37-million-
                                                                  accounts/
      2  Ars Technica   Microsoft to lay off 10,000 workers,      https://arstechnica.com/?p=1910849        2023-01-20 09:47:15               3           630
                        blames decelerated customer spending
      1  Ars Technica   Trump tries to get back on Facebook,      https://arstechnica.com/?p=1910774        2023-01-20 09:47:29               4           785
                        claims ban is electoral “interference”
-------  -------------  ----------------------------------------  ----------------------------------------  -------------------  --------------  ------------
  Index  Domain Name    Title                                     URL                                       Added                  Time to Read    Word Count

[v]iew <index>  |  [d]elete <index>  |  [vd] <index>  |  [u]pdate  |  [f]ilter  |  [q]uit >
```

# Ideas/Bugs

Any ideas for improvement or bugs found are welcome. Please open a GitHub Issue.
