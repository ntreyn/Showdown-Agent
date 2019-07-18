# Showdown-Agent

# TODO

Test stale element fix in battle.get_opposing_team()

Turn Updates:

1. Update sets each turn
    * Detected: items, abilities, nicknames **DONE**
    * Must Detect: form changes, moveset **DONE**
        * Moveset requires change to moveset dict instead of list
        * Requires eventual movedex and move class
    * Add knock off condition to items **DONE**
    * Create nickname to species dict **DONE**
    * Z move case
2. Update lasting attributes
    * HP / PP / Fainted **DONE**
    * Status Conditions **DONE**
3. Update temp attributes
    * Confusion, perish, leech, ingrain, etc **DONE**
    * Stat changes (boosts, drops) **DONE**
    * Remove attributes on switch **DONE**
    * Add substitute
4. Differentiate between friendly and opposing pokemon **DONE**
5. Tweak for friendly updates too **DONE**
6. Add move and status effects
7. Tox next damage edge case


Field Conditions and Hazards:

1. Implement hazards **DONE**
    * Requires side attribute
2. Finish weather
    * Add starter **DONE**
        * Requires nickname dict and friendly vs. opposing differentiation
    * Add turn logic for updating item (heat rock, light clay)
    * Add side attribute for screens **DONE**
    * Add heavy sun, heavy rain, strong winds **DONE**
    * Add tailwind, lucky chant, safeguard, mist **DONE**
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
    

