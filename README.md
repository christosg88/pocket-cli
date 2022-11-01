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

from pocket import Pocket

if __name__ == "__main__":
    pocket = Pocket()
    pocket.authenticate()
    pocket.prompt()
```

The `authenticate()` function will make all the necessary steps to authenticate you to pocket, asking for access the
first time, or using the stored access token for subsequent runs.

The `prompt()` function will display a tabulated list of your items, grouped by the required reading time in 5 minute
increments. The prompt line will ask you which operation you'd like to perform.

Here's a truncated example using my list:

```
===== 170–175 minutes =====
  Index  Domain Name    Title                                                    URL                                            Added         Time to Read    Word Count
-------  -------------  -------------------------------------------------------  ---------------------------------------------  ----------  --------------  ------------
    148  Wait But Why   Neuralink and the Brain's Magical Future — Wait But Why  https://waitbutwhy.com/2017/04/neuralink.html  2022-10-30             170         36307

===== 35–40 minutes =====
  Index  Domain Name    Title                                                          URL                                 Added         Time to Read    Word Count
-------  -------------  -------------------------------------------------------------  ----------------------------------  ----------  --------------  ------------
    147  Ars Technica   Human trafficking’s newest abuse: Forcing victims into cyb...  https://arstechnica.com/?p=1881183  2022-09-15              38          8218

===== 25–30 minutes =====
  Index  Domain Name    Title                                                URL                                 Added         Time to Read    Word Count
-------  -------------  ---------------------------------------------------  ----------------------------------  ----------  --------------  ------------
    146  Ars Technica   Rent going up? One company’s algorithm could be why  https://arstechnica.com/?p=1890378  2022-10-17              29          6128

===== 20–25 minutes =====
  Index  Domain Name    Title                                                          URL                                 Added         Time to Read    Word Count
-------  -------------  -------------------------------------------------------------  ----------------------------------  ----------  --------------  ------------
    145  Ars Technica   A scientist’s quest for an accessible, unhackable voting m...  https://arstechnica.com/?p=1893539  2022-10-30              20          4310
    144  Ars Technica   iOS 16 review: Customization unlocked                          https://arstechnica.com/?p=1884255  2022-09-24              23          4846
    143  Ars Technica   Here are the winners of the 2022 Ig Nobel Prizes               https://arstechnica.com/?p=1880190  2022-09-19              20          4358
    142  Ars Technica   What If? 2 is here with even more serious answers to your ...  https://arstechnica.com/?p=1880389  2022-09-14              20          4333
    141  Ars Technica   Some Macs are getting fewer updates than they used to. Her...  https://arstechnica.com/?p=1859979  2022-07-02              21          4458

===== 15–20 minutes =====
  Index  Domain Name     Title                                                          URL                                                            Added         Time to Read    Word Count
-------  --------------  -------------------------------------------------------------  -------------------------------------------------------------  ----------  --------------  ------------
<snip>
    123  briankrebs      Leaked Chats Show LAPSUS$ Stole T-Mobile Source Code           https://krebsonsecurity.com/2022/04/leaked-chats-show-laps...  2022-04-24              16          3328
    122  Ars Technica    OnePlus 10 Pro review: There’s not much left of the origin...  https://arstechnica.com/?p=1842798                             2022-04-16              17          3618
    121  Ars Technica    Rocket Report: NASA scrubs third SLS fueling test, Pythom ...  https://arstechnica.com/?p=1847143                             2022-04-16              15          3115
    120  Ars Technica    Exploring mind-bending questions about reality and virtual...  https://arstechnica.com/?p=1827805                             2022-01-29              19          3998
    119  Ars Technica    Planetary scientists are starting to get stirred up by Sta...  https://arstechnica.com/?p=1816671                             2021-12-02              18          3860

===== 10–15 minutes =====
  Index  Domain Name     Title                                                          URL                                                            Added         Time to Read    Word Count
-------  --------------  -------------------------------------------------------------  -------------------------------------------------------------  ----------  --------------  ------------
<snip>
     44  Opensource.com  Vanilla Vim is fun                                             https://opensource.com/article/21/12/vanilla-vim-config        2021-12-08              13          2783
     43  Ars Technica    Verizon overrides users’ opt-out preferences in push to co...  https://arstechnica.com/?p=1818669                             2021-12-08              10          2137
     42  Ars Technica    SolarWinds hackers have a whole bag of new tricks for mass...  https://arstechnica.com/?p=1818191                             2021-12-06              12          2654
     41  Ars Technica    The movement to hold AI accountable gains more steam           https://arstechnica.com/?p=1818000                             2021-12-05              13          2727
     40  Ars Technica    Here’s why Elon Musk asked his SpaceX employees to work Th...  https://arstechnica.com/?p=1817058                             2021-12-02              12          2634

===== 5–10 minutes =====
  Index  Domain Name     Title                                                          URL                                                            Added         Time to Read    Word Count
-------  --------------  -------------------------------------------------------------  -------------------------------------------------------------  ----------  --------------  ------------
<snip>
     10  Ars Technica    Experts debate the ethics of LinkedIn’s algorithm experime...  https://arstechnica.com/?p=1884675                             2022-09-28               9          1990
      9  Ars Technica    Set a calendar alert: NASA to broadcast first asteroid red...  https://arstechnica.com/?p=1883002                             2022-09-21               8          1646
      8  Ars Technica    Biden calls pandemic “over” despite pathetic booster rates...  https://arstechnica.com/?p=1882677                             2022-09-20               8          1767
      7  Ars Technica    Ukraine’s cyberwar chief sounds like he’s winning              https://arstechnica.com/?p=1881710                             2022-09-19               9          1938
      6  Ars Technica    How global warming and La Niña fueled a summer of climate ...  https://arstechnica.com/?p=1882033                             2022-09-19               7          1553
      5  Ars Technica    Record monsoon flooding in Pakistan due to a confluence of...  https://arstechnica.com/?p=1882062                             2022-09-19               6          1303
      4  Ars Technica    Kate Beaton on creating the best graphic novel of 2022         https://arstechnica.com/?p=1882099                             2022-09-19               7          1462
      3  Ars Technica    Lots of strange things about Saturn can be explained by a ...  https://arstechnica.com/?p=1882237                             2022-09-17               7          1528
      2  AnandTech       Arm Announces Neoverse V2 and E2: The Next Generation of A...  https://www.anandtech.com/show/17575/arm-announces-neovers...  2022-09-15               6          1333
      1  Ars Technica    Starlink appeals FCC rejection of $886M grant, calls rever...  https://arstechnica.com/?p=1880488                             2022-09-13               7          1555

[v]iew <index>  |  [d]elete <index>  |  [vd] <index>  |  [u]pdate  |  [s]tatistics  |  [q]uit >
```

# Ideas/Bugs

Any ideas for improvement or bugs found are welcome. Please open a GitHub Issue.
