## CSGO Case Data Analysis (Currently without knives/gloves)

Works out average profit per case (Currently only uses gun skin prices), the code only currently accurately works for GBP but can easily be changed in the main.py file (So without changes the code will crash or be inaccurate unless you live in UK).
The code takes a while to run as Steam has a limit on requests, so it compiles data from CSGOStash as well as SteamMarket, but only uses steam market prices.
The code should have no need to be changed when a new case gets released, unless they do something odd.

## How It Calculates Values

Gets average price of each skin of each rarity and stat-track of each case according to the rarity of each, then calculates cost of opening each case. Gets average cost and minus's average outcome of each case.

## Instructions

- Install python 3
- Install requests module - `pip install requests`
- It can take about 27 mins to compile all the data it needs
- Run main.py
- Program outputs the result in the results.txt file located in /current

## Help

	If you have issues, 
	Message on the github page
	
	But the code should work fine


## Example Results (10/05/2022):
```
CS:GO Weapon Case 3 ~ -0.49065092733333415
Shadow Case ~ -0.5353895642857143
Operation Wildfire Case ~ -0.7451264979999995
Falchion Case ~ -0.8690617335555553
Horizon Case ~ -0.9773799866666665
Revolver Case ~ -1.0868887199999997
Prisma Case ~ -1.1622260504126984
Operation Vanguard Weapon Case ~ -1.1663884526666666
Prisma 2 Case ~ -1.2546098422857141
CS20 Case ~ -1.3001250133333335
Danger Zone Case ~ -1.3088801385714286
Snakebite Case ~ -1.333511416
Fracture Case ~ -1.3559560880000001
Shattered Web Case ~ -1.3802351561904762
Operation Phoenix Weapon Case ~ -1.5493879913888886
Operation Broken Fang Case ~ -1.6023493226666667
Chroma 2 Case ~ -1.6476826024999998
Dreams &amp; Nightmares Case ~ -1.7349554659047621
Spectrum Case ~ -1.761462312857143
Chroma 3 Case ~ -1.8120143757142855
Clutch Case ~ -1.8141858224761904
Chroma Case ~ -1.834853867333333
Spectrum 2 Case ~ -1.8980511855238096
Gamma Case ~ -1.9623437694285712
eSports 2014 Summer Case ~ -1.966613270666666
Operation Riptide Case ~ -2.1354644559047617
Gamma 2 Case ~ -2.1760050912380953
Winter Offensive Weapon Case ~ -2.2364220816666665
eSports 2013 Winter Case ~ -2.262996812222222
CS:GO Weapon Case 2 ~ -2.3633042296666655
Huntsman Weapon Case ~ -2.810259526666666
Glove Case ~ -3.650142872
Operation Breakout Weapon Case ~ -3.915997794722222
Operation Hydra Case ~ -8.945994573523809
Operation Bravo Case ~ -19.98586110333333
eSports 2013 Case ~ -20.09925230222222
CS:GO Weapon Case ~ -20.73005133333333
```
