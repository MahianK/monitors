import random
import os
import requests
import time
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


class checkStock:
    

    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    stores = {
        "PS4" : 
        [
            "https://www.bestbuy.com/site/sony-playstation-4-1tb-console-black/5850905.p?skuId=5850905",
            ".add-to-cart-button",
            "Add to Cart",
            "Sony - PlayStation 4 1TB Console",
            "5850905",
            "$299.99",
        ],

        "PS5 DISC" : 
        [
            "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149",
            ".add-to-cart-button",
            "Add to Cart",
            "Sony - PlayStation 5 Console",
            "6426149",
            "$499.99",
        ],

        "PS5 DIGITAL" : 
        [
            "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161",
            ".add-to-cart-button",
            "Add to Cart",
            "Sony - PlayStation 5 Digital Edition",
            "6430161",
            "$399.99",
        ],

        "3070 Founders GPU" : 
        [
            "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
            ".add-to-cart-button",
            "Add to Cart",
            "NVIDIA GeForce RTX 3070 8GB GDDR6",
            "6429442",
            "$499.99",
        ],

        "Samsung - 55 Class Q80A " : 
        [
            "https://www.bestbuy.com/site/samsung-55-class-q80a-series-qled-4k-uhd-smart-tizen-tv/6451481.p?skuId=6451481",
            ".add-to-cart-button",
            "Add to Cart",
            "Samsung - 55 Class Q80A Series QLED 4K UHD Smart Tizen TV",
            "6451481",
            "$999.99",
        ],


    }

    #Get information from the atc button
    def getButton(self, url, selection):
        user_agent = random.choice(self.user_agent_list)
        headers = {"User-Agent" : user_agent}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        return soup.select(selection)

    def runCheck(self, interval):     
        for key in self.stores:
            myResult = self.getButton(self.stores[key][0], self.stores[key][1])
            if self.stores[key][2] in str(myResult):
                os.system("echo \033[32m" + f'[{datetime.now()}] :: {key}: {self.stores[key][3]}')
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/939686697359249468/g1bn6b9JGhsV93zCgk_W2i8j9m35hwnTnrWm3UaK1NhSBcbLlKdhDppzKVKxJ2iM_M0m', username="Best Buy")
                embed = DiscordEmbed(title= self.stores[key][3], description= "Available NOW", url=self.stores[key][0], color=242424)
                embed.set_author(name='https://www.bestbuy.com/ -- by Mahian', url='', icon_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.facebook.com%2Fbestbuy%2F&psig=AOvVaw1xgtOM3y03-F8pbfrLyGJR&ust=1644195619713000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIjm95Lw6fUCFQAAAAAdAAAAABAD')
                embed.set_footer(text='Embed Footer Text', url='')
                embed.set_timestamp()
                embed.add_embed_field(name='SKU', value= self.stores[key][4])
                embed.add_embed_field(name='Price', value= self.stores[key][5])
                embed.add_embed_field(name='', value='')
                embed.add_embed_field(name='Field 4', value='sadipscing elitr')
                webhook.add_embed(embed)
                response = webhook.execute()
            else:
                os.system("echo \033[31m "+ f'[{datetime.now()}] :: {key}: {self.stores[key][3]}')
            time.sleep(interval)
        self.runCheck(interval)
    

checkStock().runCheck(2)




