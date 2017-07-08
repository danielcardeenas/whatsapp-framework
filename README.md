# mac (Whatsapp framework) 
![Version](https://img.shields.io/badge/version-0.0.7-brightgreen.svg?style=flat-square)
![Version](https://img.shields.io/badge/release-alpha-yellow.svg?style=flat-square)

Mac is a whatsapp bot/framework I made as a weekend project. The project itself has all you need to make your own custom functions easily.

## Setup:
1. Clone this repository (with submodules)
```sh
> git clone --recursive https://github.com/danielcardeenas/whatsapp-framework.git
```
2. Install submodules
```sh
> cd libs/python-axolotl
> python3.5 setup.py install
> cd ../yowsup
> python3.5 setup.py install
```

3. Register your phone and get a password with yowsup-cli: [_Documentation_](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0)


4. Open **config.py** and add set credentials

5. Ready to go! (Now you can add your own whatsapp modules)
```sh
> ./start
```

## Modules examples:
![alt text](http://i.imgur.com/ZRlk5Uj.png)
![alt text](http://i.imgur.com/JmPbPXB.png)
![alt text](http://i.imgur.com/L4ebZql.png)
![alt text](http://i.imgur.com/B2igFQd.png)

##### Current modules:
+ **`!hi`**: Says hi to sender
+ **`!yt`**: Activates youtube detection
+ **`!siono`**: Random yes or no function. Returns gif and answer from [**yesno.wtf/api**](https://yesno.wtf/api/)
+ **`!poll <title>, <identifier (optional)>`**: Make polls (taking chat as input)
+ **`!poll2 <title>, <cantidates>...`**: Make polls (taking chat as input)
+ **`!<message>`**: If command is not recognized uses IA from ~~Cleverbot~~ Wolframalpha to answer
+ **`!elo <game>`**: Retrieves rankings of the game
+ **`!match <game>, <results>`**: Records a match to the specified game

## Contributing
Adding your own funcitons to Mac is very easy. Check the [**wiki**](https://github.com/danielcardeenas/MacBot/wiki) for more info.
