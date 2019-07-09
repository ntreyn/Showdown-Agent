# Showdown-Agent

# TODO

Turn Updates:

1. Update sets each turn
    * Detected: items, abilities, nicknames
    * Must Detect: form changes, moveset
        * Moveset requires change to moveset dict instead of list
        * Requires eventual movedex and move class
    * Add knock off condition to items
    * Create nickname to species dict
    * Z move case
2. Update lasting attributes
    * HP / PP / Fainted
    * Status Conditions
3. Update temp attributes
    * Sub, confusion, perish, leech, ingrain
    * Stat changes (boosts, drops)
4. Differentiate between friendly and opposing pokemon
5. Tweak for friendly updates too


Field Conditions and Hazards:

1. Implement hazards
    * Requires side attribute
2. Finish weather
    * Add starter
        * Requires nickname dict and friendly vs. opposing differentiation
    * Add turn logic for updating item (heat rock, light clay)
    * Add side attribute for screens
    * Add heavy sun, heavy rain, strong winds
    * Add tailwind, lucky chant
3. Future sight, doom desire?
    * Wait until move implementation


Action Function:

1. Implement execute action function
    * Requires a potential actions function
    * Requires an aciton code / dict


Turn Structure:

1. Implement execute turn
    * End of turn determination
    * Wait for animations and opponent's moves to avoid timeout exceptions
2. Implement lead and end game
    

