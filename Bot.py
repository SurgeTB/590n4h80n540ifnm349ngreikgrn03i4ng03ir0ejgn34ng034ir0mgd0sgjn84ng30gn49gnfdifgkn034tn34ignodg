token = "redacted" ##
#
import discord
import asyncio
import http.client
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import sys
import csv
import ast

client = discord.Client()
#server = discord.Server(redacted)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="-help"))


login_data = {
            'username': "",
            'password': "",
            'submit': 'submit',
            }


@client.event
async def on_message(message):
####################################################################################################################################################################################
    if message.content.startswith("-lastpost"):
        
        print(message.content)
        ###
        user_id = message.author.id
        user_name = message.author

        ###
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
        await client.send_typing(message.channel) #indicate bot is typing, until a message is sent
        #access site
        session_requests = requests.session()
        url = "http://forum.toribash.com/vaispy.php?do=xml" 
        result = session_requests.get(url,headers = dict(referer = url))
        #access html
        tree = html.fromstring(result.content)
        titles=[]
        for found in tree.xpath("//title"): 
            titles.append(found.text_content())
        posters=[]
        for found in tree.xpath("//poster"): 
            posters.append(found.text_content()) 
        times=[]
        for found in tree.xpath("//when"): 
            times.append(found.text_content()) 
        post_id=[]
        for found in tree.xpath("//id"): 
            post_id.append(found.text_content()) 
        await client.send_message(message.channel, ":white_check_mark: Last post was in the thread **"+titles[0]+
                                  "**, posted by **"+posters[0]+
                                  "**, "+times[0]+
                                  ". **Link: **"+"http://forum.toribash.com/showthread.php?p="+post_id[0]+"#post"+post_id[0]) #print out everything (1st result = most recent [0])
####################################################################################################################################################################################
    if message.content.startswith("-deac"):
        global login_data
        ###
        user_id = message.author.id
        user_name = message.author

        ###
        await client.add_reaction(message, '\U0001F4E8') #:incoming_envelope:
        
        content_a = []
        for x in range(0,len(message.content)):
            content_a.append(message.content[x])
        print(content_a)
        x = 0
        pagenumber = []
        while 1:
            x+=1
            if content_a[len(content_a)-x].isdigit():
                print("Last item is a digit")
                
                
                print(content_a)
                pagenumber.insert(0, content_a[len(content_a)-x])
                
            else:
                for x in range(0,len(pagenumber)):
                    content_a.remove(content_a[len(content_a)-1])
                break
        pagenumber = "".join(pagenumber)
        print("page number " + str(pagenumber))
        for o in range(0,6):
            try:
                content_a.remove(content_a[0])
            except:
                break
        user_final = ""
        for i in range(0,len(content_a)):
            user_final += content_a[i]
        print(user_final)
        url = "http://forum.toribash.com/tori_inventory.php?username="+user_final
        
        session_requests = requests.session()

         


        r = session_requests.post(url, data=login_data)

        r = session_requests.get("http://forum.toribash.com/tori_inventory.php?username="+user_final)
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree = html.fromstring(result.content)
        deactive=[]
        sets =[]
        link_a = []
        link_a_1 = []
        link_a_2 = []
        wasnumber = 0
        for found in tree.xpath("//span[@class='inv_item_info_name']"): 
            deactive.append(found.text_content()) 
        for found1 in tree.xpath("//span[@class='inv_item_info_name']/a/@href"): 
            for x in range(24,35):
                if not found1[:x][-1].isdigit():
                    found1 = found1[:x]

            for r in range(0,len(found1)):
                link_a.append(found1[r])
            for b in range(0,len(link_a)):
                if link_a[b].isdigit():                    
                    link_a_2.append(link_a[b])
            link_a_1.append("".join(link_a_2))
            link_a_2 = []
            link_a = []
        print(link_a_1)
                
        items_final = ""
        
        page = 1
        emptysets = 0
        msglen = 0
        sent = 0
        above2000 = 0
        setsused = 0
        
        for x in range(0,len(deactive)):

            if "Set" in deactive[x][:3]:
                toadd = " [ Use -openset "+user_final+" "+str(link_a_1[setsused]+" ]")


                deactive[x] += str(toadd)
                setsused += 1
            if msglen < 1800:
                if not "(EMPTY)" in deactive[x]:
                    if x != len(deactive):
                        msglen += len(deactive[x]+"\n")
                        items_final += deactive[x]+"\n"
                    else:
                        msglen += len(deactive[x])
                        items_final += deactive[x]
                else:
                    emptysets += 1
            else:
                if len(items_final) > 0:
                    print(items_final)
                    if sent == 0:
                        await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s inventory:\n```ini\n"+items_final+"```")
                    else:
                        await client.send_message(message.author, "Page "+str(page)+":\n```ini"+items_final+"```")
                    sent += 1
                    above2000 = 1
                    items_final = ""
                    page+=1
                    msglen = 0
        if above2000 == 0:
            print(items_final)
            await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s inventory:\n```ini\n"+items_final+"```")
            sent += 1
        else:
            await client.send_message(message.author, "Page "+str(page)+":\n```ini\n"+items_final+"```")
            sent +=1
        

####################################################################################################################################################################################
    if message.content.startswith("-tc"):
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
        ###
        user_id = message.author.id
        user_name = message.author

        ###
        
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
    if message.content.startswith("-price"):
        
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
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
            
        session_requests = requests.session()

         

        r = session_requests.post(url, data=login_data)
        time.sleep(2)
        url = "http://forum.toribash.com/tori_market.php?action=search&item="+item_final+"&username=&max=0&maxQi=0"
            
        result = session_requests.get(url,headers = dict(referer = url))
        tree2 = html.fromstring(result.content)
        final_items = []
        found_items = []
        for found_item in tree2.xpath("//td[@class='market_item_name']/a"): 
            if len(found_items) < 5:
                if not found_item.text_content().startswith("["):
                    found_items.append(found_item.text_content()) 
        len_orig = len(found_items)
        final_items.append(found_items[0])
        found_items_2 = []
        for found_item in tree2.xpath("//tr[@class]/td"): 
            found_items_2.append(found_item.text_content()) 
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
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        newline = "\n"
        await client.add_reaction(message, '\U0001F4E8') #:incoming_envelope:
        await client.send_message(message.author, ":question: Current commands:"
                                  +newline+"```-deac <user> - View the contents of user's inventory"
                                  +newline+"-active <user> - View the contents of a user's active inventory"
                                  +newline+"-price <item> - View the 5 cheapest prices of an item on the market"
                                  +newline+"-help - Access a list of commands"
                                  +newline+"-lastpost - View the last post on the forum"
                                  +newline+"-tc <user> - View the amount of TC a user has"
                                  +newline+"-stats <user> - Shows stats about the user"
                                  +newline+"-clan <clanname> - View the members of a clan"
                                  +newline+"-join <roomname> - Create a steamlink for a TB room```")
####################################################################################################################################################################################
    if message.content.startswith("-join"):
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        message_a = []
        for x in range(0,len(message.content)):
            message_a.append(message.content[x])
        for x in range(0,6):
            message_a.remove(message_a[0])
        room_join = ""
        for x in range(0,len(message_a)):
            room_join += message_a[x]
        await client.send_message(message.channel, ":arrow_forward: steam://run/248570//+connect%20join%20"+room_join)
####################################################################################################################################################################################            
    if message.content.startswith("-stats"):
        
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        message_a = []
        for x in range(0,len(message.content)):
            message_a.append(message.content[x])
        for x in range(0,7):
            message_a.remove(message_a[0])
        embed_user = ""
        for x in range(0,len(message_a)):
            embed_user += message_a[x]
        ###

        url = "http://forum.toribash.com/tori_stats.php?format=json&username="+str(embed_user)
        
        session_requests = requests.session()
        
        result = session_requests.get(url,headers = dict(referer = url))
        
        tree4 = html.fromstring(result.content)
        found_text = ""
        for found_dt in tree4.xpath("//html/body/*"):
            found_text += found_dt.text_content()
        text_n = found_text.replace("null", '"null"')


        dict_s = eval(text_n)


        

        url = "http://forum.toribash.com/member.php?username="+str(embed_user)

        result = session_requests.get(url,headers = dict(referer = url))
        tree4 = html.fromstring(result.content)

        found_img_a = []            
        for found_img in tree4.xpath("//td/img/@src"):
            found_img_a.append(found_img)
            print(found_img)

        ###

        real_names = ["Username", "User ID", "QI", "Join Date", "Posts", "Last Forum Activity", "Last Fight", "achiev_progress",
                      "Belt", "beltrank", "Custom Belt Title", "Clan Name", "Clan Tag", "ELO", "Win Rate", "TC", "room"]

        remove = ["Username", "beltrank", "room", "achiev_progress"]
        #print(dict_s["belttitle"])

        if dict_s["belttitle"] == " Belt":
            remove.append("Custom Belt Title")

        dict_s["joindate"] = time.strftime("%d %b %Y", time.localtime(int(dict_s["joindate"])))
        dict_s["lastactivity"] = time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(dict_s["lastactivity"])))
        dict_s["lastingame"] = time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(dict_s["lastingame"])))
        dict_s["winratio"] += "%"

        a = dict_s["posts"]
        del dict_s["posts"]

        temp_dict = {}

        do = 0

        for key, val in dict_s.items():
            if do == 1:
                temp_dict["posts"] = a
            if key == "joindate":
                do = 1
                
            temp_dict[key] = val

        dict_s = temp_dict

        
        #x = 0
        
        for key, value in dict_s.items():
            username = value
            break
            
            
            #print(key, real_names[x])
            #x += 1
            
        embed = discord.Embed(title=str(username), color=0xff0000)
        
        if len(found_img_a) > 0:
            embed.set_thumbnail(url=found_img_a[0])
            
        x = 0
        
        for key, value in dict_s.items():
            if not real_names[x] in remove and str(value) != "":
                embed.add_field(name=real_names[x], value=str(value), inline=True)
            x += 1

        #embed.add_field(name="Field2", value="test2", inline=True)
        
        await client.send_message(message.channel, url, embed=embed)
####################################################################################################################################################################################     
    if message.content.startswith("-clan"):
        
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        await client.add_reaction(message, '\U0001F4E8') #:incoming_envelope:
        clan_a = []
        for x in range(6,len(message.content)):
            clan_a.append(message.content[x].lower())
        print(clan_a)
        ###
        url = "http://forum.toribash.com/clan_list.php"

        session_requests = requests.session()

         

        r = session_requests.post(url, data=login_data)

        result = session_requests.get(url,headers = dict(referer = url))
        treeclan = html.fromstring(result.content)
        found_users = []
        count1 = 0
        found = 0
#        active_clans = []
#        active_clans_href = []
        clan_a = "".join(clan_a)

#       for found in treeclan.xpath("//*[@id='clan_list']/tr/td/div/a"):
#            count1 += 1
#            active_clans.append(found.text_content())
#            if found.text_content().lower() == clan_a:
#                break
#            
#        for found1 in treeclan.xpath("//*[@id='clan_list']/tr/td/div/a/@href"):
#            active_clans_href.append(found1)
#            if len(active_clans_href) > count1:
#                break
#
#        print(active_clans)
#        print(active_clans_href)        
#        
#        print(message.author, clan_a)
#        for x in range(0,len(active_clans)):
#            if active_clans[x].lower() == clan_a:
#                found = 1
#
#                count1 = x
#                break
        
        if found == 0:
            await client.send_message(message.author, ":x: I couldn't find that clan, maybe it's inactive or dead.")
        if found == 1:
            url = "http://forum.toribash.com/"+active_clans_href[x]
            session_requests = requests.session()

            r = session_requests.post(url, data=login_data)

            result = session_requests.get(url,headers = dict(referer = url))
            treeclan = html.fromstring(result.content)
            #################
            
            for found_user in treeclan.xpath("//a[@class='clan_member']"): 
                if not found_user.text_content() in found_users:
                    found_users.append(found_user.text_content())   
            msg_to_send = ":family: "+active_clans[count1]+ " member list:```\n"
            for x in range(0,len(found_users)):
                print(found_users[x])
                msg_to_send=str(msg_to_send)
                msg_to_send += str(found_users[x])+"\n"
            msg_to_send += "```"
            await client.send_message(message.author, msg_to_send)
#######################################################################################################################################################
    if message.content.startswith("-openset"):
        
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        
        await client.add_reaction(message, '\U0001F4E8') #:incoming_envelope:

        msg1 = message.content[9:]

        for x in range(0,len(msg1)):
            if msg1[x] == " ":
                user_final = msg1[:x]
                set_id = msg1[x+1:]
            else:
                pass
        
        print(user_final)
        print(set_id)
        print(user_final, set_id)

        url = "http://forum.toribash.com/tori_inventory.php?sid="+set_id+"&username="+user_final
        
        session_requests = requests.session()

         

        r = session_requests.post(url, data=login_data)

        r = session_requests.get("http://forum.toribash.com/tori_inventory.php?sid="+set_id+"&username="+user_final)
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree = html.fromstring(result.content)
        deactive=[]
        sets =[]
        link_a = []
        link_a_1 = []
        link_a_2 = []
        wasnumber = 0
        for found in tree.xpath("//span[@class='inv_item_info_name']"): 
            deactive.append(found.text_content()) 
                
        items_final = ""
        
        page = 1
        emptysets = 0
        msglen = 0
        sent = 0
        above2000 = 0
        setsused = 0
        
        for x in range(0,len(deactive)):
            if msglen < 1800:
                if x != len(deactive):
                    msglen += len(deactive[x]+"\n")
                    items_final += deactive[x]+"\n"
                else:
                    msglen += len(deactive[x])
                    items_final += deactive[x]
            else:
                if len(items_final) > 0:
                    print(items_final)
                    if sent == 0:
                        await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s set:\n```\n"+items_final+"```")
                    else:
                        await client.send_message(message.author, "Page "+str(page)+":\n```\n"+items_final+"```")
                    sent += 1
                    above2000 = 1
                    items_final = ""
                    page+=1
                    msglen = 0
        if above2000 == 0:
            print(items_final)
            await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s set:\n```\n"+items_final+"```")
            sent += 1
        else:
            await client.send_message(message.author, "Page "+str(page)+":\n```\n"+items_final+"```")
            sent +=1
###############################################
    if message.content.startswith("-active"):
        
        ###
        user_id = message.author.id
        user_name = message.author
        ###
        
        await client.add_reaction(message, '\U0001F4E8') #:incoming_envelope:
        
        content_a = []
        for x in range(0,len(message.content)):
            content_a.append(message.content[x])
        print(content_a)
        x = 0
        for o in range(0,8):
            try:
                content_a.remove(content_a[0])
            except:
                break
        user_final = ""
        for i in range(0,len(content_a)):
            user_final += content_a[i]
        print(user_final)
        url = "http://forum.toribash.com/tori_inventory.php?sid=-1&username="+user_final
        
        session_requests = requests.session()

         

        r = session_requests.post(url, data=login_data)

        r = session_requests.get("http://forum.toribash.com/tori_inventory.php?sid=-1&username="+user_final)
        
        result = session_requests.get(url,headers = dict(referer = url))
        tree = html.fromstring(result.content)
        deactive=[]
        sets =[]
        link_a = []
        link_a_1 = []
        link_a_2 = []
        wasnumber = 0
        for found in tree.xpath("//span[@class='inv_item_info_name']"): 
            deactive.append(found.text_content()) 
        for found1 in tree.xpath("//span[@class='inv_item_info_name']/a/@href"): 
            for x in range(24,35):
                if not found1[:x][-1].isdigit():
                    found1 = found1[:x]

            for r in range(0,len(found1)):
                link_a.append(found1[r])
            for b in range(0,len(link_a)):
                if link_a[b].isdigit():                    
                    link_a_2.append(link_a[b])
            link_a_1.append("".join(link_a_2))
            link_a_2 = []
            link_a = []
        print(link_a_1)
                
        items_final = ""
        
        page = 1
        emptysets = 0
        msglen = 0
        sent = 0
        above2000 = 0
        setsused = 0
        
        for x in range(0,len(deactive)):

            if "Set" in deactive[x][:3]:
                toadd = " [ Use -openset "+user_final+" "+str(link_a_1[setsused]+" ]")


                deactive[x] += str(toadd)
                setsused += 1
            if msglen < 1800:
                if not "(EMPTY)" in deactive[x]:
                    if x != len(deactive):
                        msglen += len(deactive[x]+"\n")
                        items_final += deactive[x]+"\n"
                    else:
                        msglen += len(deactive[x])
                        items_final += deactive[x]
                else:
                    emptysets += 1
            else:
                if len(items_final) > 0:
                    print(items_final)
                    if sent == 0:
                        await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s inventory:\n```ini\n"+items_final+"```")
                    else:
                        await client.send_message(message.author, "Page "+str(page)+":\n```ini"+items_final+"```")
                    sent += 1
                    above2000 = 1
                    items_final = ""
                    page+=1
                    msglen = 0
        if above2000 == 0:
            print(items_final)
            await client.send_message(message.author, ":white_check_mark: Page "+str(page)+" of **"+user_final+"**'s inventory:\n```ini\n"+items_final+"```")
            sent += 1
        else:
            await client.send_message(message.author, "Page "+str(page)+":\n```ini\n"+items_final+"```")
            sent +=1
####################################################################################################
    if message.content.startswith("-games"):
        
        
        await client.add_reaction(message, '\U00002705') #:white_check_mark:
        
        content_a = []
        for x in range(0,len(message.content)):
            content_a.append(message.content[x])
        x = 0
        for o in range(0,7):
            try:
                content_a.remove(content_a[0])
            except:
                break
        user_final = ""
        for i in range(0,len(content_a)):
            user_final += content_a[i]

        url = "http://forum.toribash.com/tori_earnings.php?username=" + str(user_final)
        print(url)
        
        session_requests = requests.session()



        r = session_requests.post(url, data=login_data)

        
        result = session_requests.get(url,headers = dict(referer = url))
        tree = html.fromstring(result.content)
        
        member_activity = 0
        count = 0

        for found in tree.xpath("//td"): 
            count += 1
            print(found.text_content())
            if count == 7:
                member_activity += int(found.text_content())
                count -= 4

        await client.send_message(message.channel, "In the last 30 days that **"+user_final+"** played at least 1 game, they played **"+str(member_activity)+"** games.")


def setup():
    client.run("redacted")
setup()



