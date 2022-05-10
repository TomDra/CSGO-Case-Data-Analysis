## CSGO Case Data Analysis (Currently without knives/gloves)

Works out average profit per case (Currently only uses gun skin prices), the code only currently accuratly works for GBP but can easily changed in the main.py file (So without changes the code will crash or be unaccurate unless you live in UK).
The code takes a while to run as Steam has a limit on requests so it compiles data from CSGOStash as well as SteamMarket, but only uses steam market prices.
The code should have no need to be changed when a new case gets released, unless they do something odd.

## How It Calculates Values

Gets average price of each skin of each rarity and stattrack of each case according to the rarity of each, then calculates cost of opening each case. Gets average cost and minus's average outcome of each case.

## Instructions

- Install python 3
- Install requests module - `pip install requests`
- It can take about 17 mins to compile all the data it needs
- Run main.py
- Program outputs the result in the results.txt file located in /current

## Help

	If you have issues, 
	Message on the github page
	
	But the code should work fine


