import requests
import threading
import json
from termcolor import *
import colorama
from datetime import *
from discord_webhook import DiscordWebhook, DiscordEmbed


colorama.init()

keywords = ['jordan 1','jordan 3','jordan 4','jordan 6','jordan 11','nocta','dunk']

class Monitor:
	def __init__(self,menu):
		self.menu = menu

		self.products = []
		self.first_run = True
		self.start_monitor()
		

	def LOG(self,text,color):
		print(colored(f'[{datetime.now()}][{self.menu}] {text}',color))


	def sendWebhook(self,sku,title,url,price,image,sizes):
		desc = ''
		for i in sizes:
			desc = desc + i['Key'] + '\n'

		if desc == '':
			desc = 'undefined'

		if any(keyword in title.lower() for keyword in keywords):
			webhook_url = 'https://discord.com/api/webhooks/848184548432150549/jUduFy6KKdeRS2FJG8nvvyKsNBzbTW8PXne9QLY_UU0C1QpFBbF1tEFGGUNSWbrqYCAx'
		else:
			webhook_url = 'https://discord.com/api/webhooks/948935640781824010/DWN8o8FO7aDndUGaUBH_TJYz9pRbZwE91cCQocO9hFyQIpWWhN0NBUdEEHQP3glNt9vi'
				

			
		webhook = DiscordWebhook(url=webhook_url)

		embed = DiscordEmbed(title=title, color=15158332,url='https://www.sneakerboy.com'+url)
		
		embed.set_author(name='https://www.sneakerboy.com/',icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=936&height=936')
		
		embed.set_thumbnail(url=image)
		
		embed.set_footer(text='Powered By Genesis | Sneakerboy V1.0', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=936&height=936')
		
		embed.set_timestamp()
		
		embed.add_embed_field(name='PRICE', value=price,inline=True)
		embed.add_embed_field(name='SKU', value=sku,inline=True)
		embed.add_embed_field(name='SIZES',value=desc,inline=False)
		embed.add_embed_field(name='LINKS',value='[Login](https://www.sneakerboy.com/myaccount.php) | [Cart](https://www.sneakerboy.com/cart)',inline=False)
			
		# add embed object to webhook
		webhook.add_embed(embed)
		
		response = webhook.execute()

			
	def start_monitor(self):
		cycle = 0
		while True:
			cycle += 1

			if(cycle == 1 or cycle == 2 or cycle % 500 == 0):
				self.LOG("Checking",'yellow')
			try:
				response = requests.get('https://www.sneakerboy.com/includes/data_product.php?menu='+self.menu)
			except:
				self.LOG('Request Error','red')
				continue


			if response.status_code == 200:
				response = response.json()
				for i in response['data']:
					if(i['Id'] not in self.products):
						self.products.append(i['Id'])
						if(not self.first_run):
							self.LOG(" [NEW PRODUCT] :: "+i['Title'],'green')
							self.sendWebhook(i['Id'],i['Title'],i['RelativeUrl'],i['Price'],i['Thumbnail'],i['sizes'])
							
					

			elif response.status_code == 403:
				self.LOG("Unauthorized Access",'red')
				continue
			else:
				self.LOG("Bad Response Status "+str(response.status_code),'red')
				continue

			self.first_run = False
					






options = ['clothing','sneakers']
for i in options:
	threading.Thread(target=Monitor,args=(i,)).start()
	