Previous posts:
* [2020-05-23 - My Factorio Logistic Train Evolution](/factorio/2020/05/23/logistic-train-evolution.md)
* [2020-05-28 - Logistic Circuits Part 2 - Automatic indexes, trash trains, faster unloaders](2020/05/28/logistic-circuits-part-2.md)
* [2020-05-30 - Logistic Circuits Part 3 - Max filter loader, fixed point reached?](2020/05/30/max-filter-fast-exact-loader.md)
* [2020-06-01 - Logistic Circuits Part 4 - Outpost refinements, self-contained modules](2020/06/01/self-contained-modules.md)
* [2022-06-06 - Logistic Circuits Part 5 - Upgrades for Factorio v1.1](2022/06/06/upgrades-for-factorio-1-1.md)

# Logistic Trains Without Logistic Bots

Hello again! It's been another long while since my last post and I've played a
few more [Space Exploration](https://mods.factorio.com/mod/space-exploration)
games since then.

A problem I keep encountering is the massive gap between unlocking basic bots
and unlocking logistic bots in SE making the logistic train circuits in the
prior posts useless. Because I've already "solved" the end-game logistic train
circuits I kept trying to push through this gap without using midgame logistic
trains/circuits with little success.

It's difficult to go back to the pre-logistic train solution with all the
assocated problems, limitations and annoyances. After a lot of experimentation
I've adapted the end-game logistic train circuits to work without logistic bots.
I find it works very well for me though the throughput is limited compared to
logistic bots and requestor chests. When I unlock logistic bots I'll be using
requestor chests again.

Here's a preview of the finished depot with the loading stations for each
logistic train type:

![loader-birds-eye.jpg](loader-birds-eye.jpg)

And the unloading station that supports up to 3 logistic train modules:

![unloader-birds-eye.jpg](unloader-birds-eye.jpg)

They can also be upgraded to their end-game forms independently, the modules and
trains are common between mid-game and end-game circuits.

## The Loading Stations

![module.jpg](module.jpg)

The "SEED MODULE" top-left is a train station and combinators for the seed train
logistic module. The module is shared (copied) between the loader and unloader.
There is a red and green side. Two constant combinators per side allows up to 40
unique items per wagon matching the 40 slots per wagon. The red and green
manifest signals are put on the lower substation red and green wires which
signal the buffer chest circuits and the loader circuits.

The lower loader circuits are detailed in the prior posts and do exact insertion
with a hand-size signal as well as item set-filters signal to the inserters.

The above buffer chest circuit inserts the target items into the buffer chests
if found on the belts near the buffer chests.

The target level in the buffer chests is a small multiple of the manifest
signals (x4) to ensure a few trains can be loaded in quick succession before the
slower fill-up from the shared depot storage catches up which is limited to the
throughput of 1-belt and the time to switch between item types.

Missing items in the buffer circuit set the green signal on the depot storage to
request the ring-belt around the storage warehouses is filled with that/those
target items. A pair of whitelist inserters and pair of blacklist inserters on
each storage warehouse add and remove wanted and unwanted items from the shared
ring belt one item type at a time until the buffer for that item is filled.

![interface.jpg](interface.jpg)

This shows the storage to station interface in more detail. The top two
arithmetic combinators act as a diode to prevent station signals being mixed
from the aggregate depot signals. The third puts the missing items (requested)
items on the green storage wire.

The depot signal is used to set the target item level in the shared storage
warehouses. Missing items are made-to-order in the mall above via the red
signal (shown elsewhere).

![delay.jpg](delay.jpg)

This belt from the storage to the buffer wagons is also very important as it
helps reduce the number of item switches on the storage warehouse ring belt. It
takes 10 seconds or so for the requested item to appear then saturate the
storage ring belt for each item type requested. If requesting 80 item types, it
would take a minimum of 800 seconds to refill buffers. However if you do more
work per item switch you'll need to switch less. In the seed train there is a
diverse set of common items configured (inserters, chests, power, bots, etc) and
the ~30 belts of delay between putting an item into the station circuit and
putting that item in the buffer chest allows up to 240 additional items to be
buffered during that context switch which for some items and trains may mean
re-loading every 4th or 5th train.

![worm.jpg](worm.jpg)

The minimum work per item switch can be increased by increasing the length of
the belt and delay between the storage and buffer chests, assuming you have
enough buffer chest storage slots left.

![trash.jpg](trash.jpg)

The trash station is shared between all logistic trains to reset them back to a
good known state (empty). Some select items (wood, coal) are converted to fuel
to power the logistic trains and others (barrels) are re-filled with oil for the
wall flamethrowers.

The "RED MISSING ITEMS" shows the simple difference circuit that requests new
items from the mall.

![mall.jpg](mall.jpg)

This is my mall that creates the missing/requested items for the logistic depot.

![4-stations.jpg](4-stations.jpg)

The depot supports multiple logistic train types. In this playthrough I have a
"seed" train with generic common items, "outpost" with mining and factory items,
"wall" which contains wall items and "raid" items for taking out nests.

The module and loader station are customized and configured per train, the rest
is common.

## The Unloader Stations

![unloader.jpg](unloader.jpg)

This is the unloader station with room for 3 modules (or train types). Items are
unloaded directly into the storage chests and trash items loaded back into
trains from the storage.

Because my trains are unidirectional I can't guarantee the arrival orientation
of the trains, so construction and logistic bots are moved from the lower to
upper storage chest to bootstrap the bot network.

![seed-arrives.jpg](seed-arrives.jpg)

This is showing the seed module was placed, it detected the storage is missing
seed items, the seed train was dispatched and seed train is currently unloading.

Compared to the prior stations in prior posts the thresholds have been updated
to (1) request a train if item count below 100% target (2) unload items up to
200% target (3) items above 300% or unknown items request a trash train to
return items to the depot.

Previously I've requested trains at <100% and >200% but found that it's too
sensitive a common case where I've only used a few items (chests, wire, jetpack
fuel) and a full train is dispatched to replenish 5-10% of a few items.

Now I'm re-filling at least one full item type per train dispatch.

## Save File

If you want to play with it in action I've uploaded my current save game. You'll
see I've massively overbuilt on Nauvis and not even launched my first rocket at
120 hours in. I've had a lot of fun working on logistic trains instead.

- [2024-02-04-mason-se.zip](2024-02-04-mason-se.zip)

Go to one of the wall stations and start building some stuff, or adding and
removing modules from the station to see the depot and trains do their dance.

No blueprints for now as it should be simple to copy what you want/need from the
above save game. My rail blueprints can be found in prior posts.

## Bugs & Feedback

Please raise an issue [here](http://github.com/mason-larobina/factorio) or email
mason.larobina@pm.me for any corrections or improvements.

## Discussion

TODO: /r/factorio link

Enjoy! 😁
