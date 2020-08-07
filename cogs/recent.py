from humanfriendly import format_timespan
import discord, time, json, yaml
from discord.ext import commands
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep

################################# Config Load #################################
config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
linked_accs_location = str(config.get('linked_accs_location'))
chrome_driver_path = str(config.get('chromedriver_path'))

################################ Load Webdriver ###############################
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

################################## Functions ##################################
def get_mega_mind(link):
    mega_mind = {}
    driver.get(link)
    sleep(1)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    ui_segments = soup.find_all('div', {'class','ui segment'})
    smol = str(ui_segments[3])
    recents = BeautifulSoup(smol,'html.parser')
    latest_recent = recents.find_all('tr', {'class','score-row'})
    latest_recent_id = str(latest_recent[0])[:47]

    pfp_link = soup.find('img', {'class':'user avatar'})
    mega_mind['pfp_link'] = pfp_link['src']

    image = recents.find('img')
    mega_mind['rank'] = image['src'].replace('/static/ranking-icons/','').replace('.png','') + '_'

    driver.find_element_by_css_selector(f'tr[{latest_recent_id[22:46]}]').click()

    new_html = driver.page_source
    tatarka = BeautifulSoup(new_html,'html.parser')
    shit_table = tatarka.find('div',{'class':'content'})
    tds = shit_table.find_all('td')

    for i in range(0,len(tds),2):
        mega_mind[get_stuff(tds[i])] = get_stuff(tds[i+1])

    bm = mega_mind['Beatmap'].replace('</a>','').split('>',1)
    mega_mind['map_link_part'] = bm[0].replace('<a href=','').replace('"','')
    mega_mind['map_name'] = bm[1]
    mega_mind.pop('Beatmap')

    return mega_mind


def get_stuff(stuff):
    return str(stuff).replace('<td>','').replace('</td>','')

################################### Commands ##################################
class RecentPlay(commands.Cog):
    def __init__(self, client):
        """Shows users recent osu! play."""
        self.client = client

    @commands.command(aliases=['l'])
    async def link(self, ctx, user:str):
        with open(linked_accs_location, "r") as f:
            accs = json.load(f)

        accs[ctx.author.id] = user

        with open(linked_accs_location, "w") as f:
            accs = json.dump(f)


    @commands.command(aliases=['r'])
    async def recent(self, ctx, user=None):
        rank_emote = None
        if user is None:
            with open(linked_accs_location, "r") as f:
                accs = json.load(f)
            user = accs[str(ctx.author.id)]

        link = f"https://akatsuki.pw/u/{user}"
        data = get_mega_mind(link)

        rank_name = data['rank']
        for guild in self.client.guilds:
            emojis = guild.emojis
            for emote in emojis:
                if emote.name == rank_name:
                    rank_emote = emote
            if rank_emote is None:
                for emote in emojis:
                    if emote.name == 'osu':
                        rank_emote = emote

        if(pp := data['PP']) == '0':
            score = f"**{data['Points']} points**"
        else:
            score = f"**{pp}PP**"

        stars = round(float(data['Difficulty'].replace(' stars','')), 2)

        tim = data['Achieved']
        y_feeties = tim.replace('T',' ').replace('Z','')
        dt = datetime.strptime(y_feeties, '%Y-%m-%d %H:%M:%S')
        x_feeties = time.mktime(dt.timetuple())
        feeter = f"{format_timespan(int(time.time() - x_feeties))} ago"

        tristo = int(data['300s']) + int(data['Gekis'])
        jensto = int(data['100s']) + int(data['Katus'])

        el1 = f"• {rank_emote} • **{data['PP']}PP** • {data['Accuracy']} [{stars}★]"
        el2 = f"• {data['Points']} points • x{data['Max combo']} • [{tristo}/{jensto}/{data['50s']}/{data['Misses']}]"


        embed = discord.Embed(colour=discord.Colour(0xff66aa))

        embed.set_author(name=f"Latest osu! play from {user}", url=f"https://akatsuki.pw{data['map_link_part']}")
        embed.set_thumbnail(url=data['pfp_link'])
        embed.add_field(name=f"{data['map_name']}",
                        value=f"{el1}\n{el2}",
                        inline=False)
        embed.set_footer(text=feeter)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(RecentPlay(client))
