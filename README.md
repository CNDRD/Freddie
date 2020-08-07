### Commands  
*For shits and giggles let's say the prefix is [ , ] (comma)*  

| Command            | What does it do                                         | Alias |
|--------------------|---------------------------------------------------------|:-----:|
|`,link [username]`  | Links your osu! account with your Discord account       | `l`   |
|`,recent <username>`| Shows your (or <username>s) most recent play statistics | `r`   |

#### Argument rules
| Brackets | Required? |
|:--------:|:---------:|
|**[ ]**   | ✔️       |
|**< >**   | ❌       |

#### Tree structure  
```
📦 Frederick
    📂 cogs
        📜 recent.py
    📂 chromedriver
        📜 chromedriver(.exe)
    📜 config.yml  
    📜 fred.py  
    📜 linked_accounts.json  
```
#### config.yml
```yaml
chromedriver_path: absolute path to your chromedriver file
token: bots token, won't work without it
linked_accs_location: path to the linked_accs.json file
admin_user_ids:
  213243546576879809
  699887766554433221
  ...
prefix: whatever you want it to be
```
#### linked_accounts.json
```
{}
```
Make sure that `linked_accounts.json` looks exactly like this before you link the first account.

Download [chrome driver](https://chromedriver.chromium.org/) (same version as your chrome browser) and place it where it belongs according to the tree structure.  

Made with ❤️ by CNDRD
