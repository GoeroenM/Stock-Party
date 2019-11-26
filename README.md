# Stock-Party
Script that helps run a 'stock party' where the amount a drink is consumed influences its price and the price of other drinks.

The concept is as follows: 

When people order more of a certain drink, the price will rise and the price of all the other drinks will drop.
The amount by which a price changes depends on the amount of drinks ordered in the time period, the current price and the base price of the drink.
Also, the way that price changes are calculated, all relative price changes will always be 0. As a simple example, assume only 2 drinks
are being sold. If one drink increases 20% in price, the other will drop 20%.

The usage of this script is already extensively explained in the script itself. It might seem like the amount of explanation is excessive,
but I wrote this originally to be used by people who have no idea how to use scripts or a command line, so I needed it to be redundant.

In order to properly run the script, you have to create a list of drinks called 'beer_list.txt' and store it in the script's directory.
In this, create two columns, the first one for the drinks and the second with base prices. Keep in mind that your file needs to have a header,
even though the column names don't matter, the order does. If you don't include headers, the first beer you enter will not be included.

I also built in a maximum and a minimum price for each drink. Right now, the script just takes 2x the original price as ceiling and 0.5x 
the original price as the floor. You can change this if you want, even turn it off completely (though I don't recommend this).
See the body of the script for an explanation of how to do this.

The way to use this script is to run it, after which a graph and a small UI window will appear. During a chosen time period (I recommend around 15 minutes),
keep note of how much of each drink is being drunk (it helps to prepare for this by making papers with each drink you sell beforehand and just draw lines).
After the time is up, enter the amount of drinks for each beer and hit the calculate button.

I also recommend not using this for more than about 8-10 different drinks, or you can group certain drinks such as IPA beers together. The reason for this
is twofold. First of all, if there's too many different drinks, it might have the effect that price fluctuations are too small to keep this concept interesting
because the drinks are all spread out. Secondly, it causes clutter on the graph.

There's also a market crash functionality which can be interesting. I've seen it happen that prices stagnate and refuse to budge, which can get boring.
The crash basically inverts the price relative to their base price. So if something is being sold at 1.8x its base price, it will now be sold at 1/1.8 = 0.55x
baseprice.