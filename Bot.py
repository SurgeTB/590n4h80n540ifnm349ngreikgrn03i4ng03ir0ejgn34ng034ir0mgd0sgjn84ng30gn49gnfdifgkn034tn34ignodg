token = "Mzk3OTIyMjc1NzkxMzM5NTIw.DS3BlA.MW-21dK35PTbv7FtAXGHyqVYLq8"

import discord
import asyncio
import http.client
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="-help"))



@client.event
async def on_message(message):
####################################################################################################################################################################################
    if message.content.startswith("-lastpost"):
        print(message.content)
        await client.send_message(message.channel, ":arrows_counterclockwise: **Accessing forums...**")
        await client.send_typing(message.channel) #indicate bot is typing, until a message is sent
        #access site
        session_requests = requests.session()
        url = "http://forum.toribash.com/vaispy.php?do=xml" #specify url to access
        result = session_requests.get(url,headers = dict(referer = url))
        #access html
        tree = html.fromstring(result.content)
        titles=[]
        for found in tree.xpath("//title"): #search for <title>
            titles.append(found.text_content()) #add all results to list
        posters=[]
        for found in tree.xpath("//poster"): #search for <title>
            posters.append(found.text_content()) #add all results to list
        times=[]
        for found in tree.xpath("//when"): #search for <title>
            times.append(found.text_content()) #add all results to list
        post_id=[]
        for found in tree.xpath("//id"): #search for <title>
            post_id.append(found.text_content()) #add all results to list
        await client.send_message(message.channel, ":white_check_mark: Last post was in the thread **"+titles[0]+
                                  "**, posted by **"+posters[0]+
                                  "**, "+times[0]+
                                  ". **Link: **"+"http://forum.toribash.com/showthread.php?p="+post_id[0]+"#post"+post_id[0]) #print out everything (1st result = most recent [0])
####################################################################################################################################################################################
    if message.content.startswith("-deac"):
        await client.send_message(message.channel, ":white_check_mark: I'll send you a DM when I've gathered all the info!")
        print(message.content)
        content_a = []
        for x in range(0,len(message.content)):
            content_a.append(message.content[x])
        for o in range(0,6):
            content_a.remove(content_a[0])
        user_final = ""
        for i in range(0,len(content_a)):
            user_final += content_a[i]

        url = "http://forum.toribash.com/tori_inventory.php?username="+user_final
        
        # Start a session so we can have persistant cookies
        session_requests = requests.session()

        # This is the form data that the page sends when logging in
        login_data = {
            'username': "AdvntrBank",
            'password': "Luxray12345",
            'submit': 'submit',
        }

        # Authenticate
        r = session_requests.post(url, data=login_data)

        # Try accessing a page that requires you to be logged in
        r = session_requests.get("http://forum.toribash.com/tori_inventory.php?username="+user_final)
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree = html.fromstring(result.content)
        deactive=[]
        for found in tree.xpath("//span[@class='inv_item_info_name']"): #search for <title>
            deactive.append(found.text_content()) #add all results to list
        items_final = ""
        print(deactive)
        for x in range(0,len(deactive)):
            if not deactive[x] == "Set (EMPTY)":
                items_final += deactive[x]+"\n"
        await client.send_message(message.author, ":white_check_mark: Here's what **"+user_final+"** has in their deactivated inventory:\n```"+items_final+
                                      " ```\n**Nothing here?** either they have an empty inventory or there's too much stuff for Discord to put in 1 message.\nhttp://forum.toribash.com/tori_inventory.php?username="+user_final)
####################################################################################################################################################################################
    if message.content.startswith("-price"):            
        await client.send_message(message.channel, ":arrows_counterclockwise: Checking prices...")
        content_price = []
        for x in range(0,len(message.content)):
            content_price.append(message.content[x])
        for o in range(0,7):
            content_price.remove(content_price[0])
        item_final = ""
        for z in range(0,len(content_price)):
            item_final += content_price[z]
        print(item_final)
        ###
        url = "http://forum.toribash.com/tori_market.php"
        
        # Start a session so we can have persistant cookies
        session_requests = requests.session()

        # This is the form data that the page sends when logging in
        login_data = {
            'username': "AdvntrBank",
            'password': "Luxray12345",
            'submit': 'submit',
        }

        # Authenticate
        r = session_requests.post(url, data=login_data)
        time.sleep(2)
        url = "http://forum.toribash.com/tori_market.php?action=search&item="+item_final+"&username=&max=0&maxQi=0"
        # Try accessing a page that requires you to be logged in
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree2 = html.fromstring(result.content)
        final_items = []
        found_items = []
        for found_item in tree2.xpath("//td[@class='market_item_name']/a"): #search for <title>
            found_items.append(found_item.text_content()) #add all results to list
        if len(found_items) != 0:        
            final_items.append(found_items[0])
            found_items = []
            for found_item in tree2.xpath("//tr[@class]/td"): #search for <title>
                found_items.append(found_item.text_content()) #add all results to list
            try:
                final_items.append(found_items[3])
                await client.send_message(message.channel, ":moneybag: The cheapest result for '"+item_final+"' is being sold for **"+final_items[1]+" TC**.")
            except:
                await client.send_message(message.channel, ":no_entry_sign: No results found")
        else:
            await client.send_message(message.channel, ":no_entry_sign: No results found")
    #http://forum.toribash.com/tori_inventory.php?username=heat
####################################################################################################################################################################################
    if message.content.startswith("-tc"):
        tc_a = []
        for a in range(0,len(message.content)):
            tc_a.append(message.content[a])
        for b in range(0,4):
            tc_a.remove(tc_a[0])
        tc_user_final = ""
        for c in range(0,len(tc_a)):
            tc_user_final += tc_a[c]

        ####
        
        url = "http://forum.toribash.com/member.php?username="+tc_user_final
        # Try accessing a page that requires you to be logged in
        session_requests = requests.session()
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree3 = html.fromstring(result.content)
        found_dd_a = []
        for found_dd in tree3.xpath("//dl/dd"):
            found_dd_a.append(found_dd.text_content())
        for i in range(0,len(found_dd_a)-1):
            found_dd_a.remove(found_dd_a[0])
        await client.send_message(message.channel, ":white_check_mark: **"+tc_user_final+"** has **"+found_dd_a[0]+" TC**.")
####################################################################################################################################################################################
    if message.content.startswith("-5price"):            
        await client.send_message(message.channel, ":arrows_counterclockwise: Checking prices...")
        content_price = []
        for x in range(0,len(message.content)):
            content_price.append(message.content[x])
        for o in range(0,8):
            content_price.remove(content_price[0])
        item_final = ""
        for z in range(0,len(content_price)):
            item_final += content_price[z]
        print(item_final)
        ###
        url = "http://forum.toribash.com/tori_market.php"
            
        # Start a session so we can have persistant cookies
        session_requests = requests.session()

        # This is the form data that the page sends when logging in
        login_data = {
            'username': "AdvntrBank",
            'password': "Luxray12345",
            'submit': 'submit',
        }

        # Authenticate
        r = session_requests.post(url, data=login_data)
        time.sleep(2)
        url = "http://forum.toribash.com/tori_market.php?action=search&item="+item_final+"&username=&max=0&maxQi=0"
        # Try accessing a page that requires you to be logged in
            
        result = session_requests.get(url,headers = dict(referer = url))
        tree2 = html.fromstring(result.content)
        final_items = []
        found_items = []
        for found_item in tree2.xpath("//td[@class='market_item_name']/a"): #search for <title>
            if len(found_items) < 5:
                found_items.append(found_item.text_content()) #add all results to list
        len_orig = len(found_items)
        final_items.append(found_items[0])
        found_items_2 = []
        for found_item in tree2.xpath("//tr[@class]/td"): #search for <title>
            found_items_2.append(found_item.text_content()) #add all results to list
        for x in range(0,5):
            try:
                for x in range(0,3):
                    found_items_2.remove(found_items_2[0])
                found_items.append(found_items_2[0])
                found_items_2.remove(found_items_2[0])
            except:
                pass
        string_to_send = ":moneybag: Cheapest item results:\n```"
        #for x in range(0,len(found_items)/2):
        failed = 0
        print(found_items)
        half_len = int(len(found_items)/2)
        print(half_len)
        for x in range(0,5):
            y = x+1
            try:
                string_to_send += str(y)+". "+found_items[x]+" selling for "+found_items[x+half_len]+" TC\n"
            except:
                pass
        string_to_send += "```"
        await client.send_message(message.channel, string_to_send)
####################################################################################################################################################################################
    if message.content.startswith("-help"):
        newline = "\n"
        await client.send_message(message.channel, ":incoming_envelope: Sending you a DM!")
        await client.send_message(message.author, ":question: Current commands:"
                                  +newline+"```-deac <user> - View the contents of user's inventory"
                                  +newline+"-price <item> - View the cheapest price of an item on the market"
                                  +newline+"-5price <item> - View the 5 cheapest prices of an item on the market"
                                  +newline+"-help - Access a list of commands"
                                  +newline+"-lastpost - View the last post on the forum"
                                  +newline+"-tc <user> - View the amount of TC a user has```")
####################################################################################################################################################################################
    if message.content.startswith("-join"):
        message_a = []
        for x in range(0,len(message.content)):
            message_a.append(message.content[x])
        for x in range(0,6):
            message_a.remove(message_a[0])
        room_join = ""
        for x in range(0,len(message_a)):
            room_join += message_a[x]
        await client.send_message(message.channel, ":arrow_forward: steam://run/248570//+connect%20join%20"+room_join)
            
            
                                  
                
                
        
        
        
        


def setup():
    client.run("Mzk3OTIyMjc1NzkxMzM5NTIw.DS3BlA.MW-21dK35PTbv7FtAXGHyqVYLq8")
setup()




