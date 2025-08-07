> **Note:** This post describes complex workarounds for challenges that have been addressed by quality of life features in Factorio. For a detailed look at these improvements, see my new post: [A Thank You to the Factorio Devs: An End to Complex Workarounds](/factorio/2025/08/07/factorio-qol-improvements.html).

# Logistic Train Upgrades For Factorio v1.1

It's been a while, folks! I can't believe it's been two years since my [last posts](https://mason-larobina.github.io/factorio/). Thank you for sharing the links and for all the comments. I hope I've inspired you to dig deeper into circuits for factory automation and logistics.

At long last (and by popular request), I'm doing a writeup on my logistic train upgrades for Factorio v1.1, which added two massive quality-of-life features:

- **Train limits:** removing the need for a global circuit network.
- **The `Anything` signal:** greatly simplifying the train loader circuit.

## Mods

Since my prior blog posts, I've been playing a mixture of Krastorio 2 and Space Exploration, which add extreme depth and complexity to the game (to my delight and occasional frustration).

As a result, the screenshots, blueprints, and sandbox save-file below require the [AAI Containers](https://mods.factorio.com/mod/aai-containers) mod.

At one point, I had a completely vanilla (and less compact) version of the Factorio v1.1 circuits, which you should be able to find in the revision history of [this gist](https://gist.github.com/mason-larobina/68389bbf2fa9ee4d764ae58c4a443f8a).

## Overview

The logistic depot consists of four main pieces:

- **Depot storage:** located close to both the trash unloader and the loading stations to minimize the [bandwidth-delay product](https://en.wikipedia.org/wiki/Bandwidth-delay_product).
- **Trash unloader:** resets all trains to a known-good state (empty) to avoid the item fragmentation problems I've discussed in prior posts.
- **Logistic modules, loading stations, and trains:** one for each train type (e.g., seed train, defense train, nuclear train, mining train, etc.).
- **A stacker with dummy stations:** enqueues all pending incoming and outgoing logistic trains, allowing multiple trains per station and avoiding deadlocks over the shared stations.

![depot and stacker](depot_and_stacker.jpg)

Thanks to the AAI Containers mod and Factorio v1.1, the logistic outpost is more compact and contains many features (some are the same, some are new, and some are improved):

- Bootstraps logistic bots automatically from either of the seed train's wagons.
- Refills lost or low bots up to the configured set-points for each.
- Three module slots for three logistic train types (manifests) per outpost.
- A dedicated trash train station to return unwanted or overstocked items to the logistic depot.
- The trash loaders overlap with most of the module stations, minimizing unnecessary trash train call-outs.
- Unloads and loads 96 items per swing (stack size permitting, of course).
- Station train limits prevent a thundering herd of trains of the same type from descending on each outpost.
- No global circuit network needed.

![outpost](outpost.jpg)

## Logistic Loading Stations

![depot](depot.jpg)

The stations are greatly simplified, thanks to the `Anything` signal added in Factorio v1.1. This feature removes the need for an index- or max-signal-based item filter for exact insertion. I detailed the problem and prior solutions in the previous four blog posts.

Now, the circuit is a simple difference calculation, followed by an `Anything` output to perform exact insertion on one item type and count at a time.

The two constant combinators in the logistic modules map to two independent loading circuits in the logistic station, connected and separated by the green and red wires.

Another trick here is to use both requester and buffer chests. If stock levels run low, the system reshuffles items into the requester chests so that trains aren't stalled waiting for the low-stock items to be returned or produced.

I keep stacking stations for each logistic train type.

## Shared Trash And Storage

![trash](trash.jpg)

This station is common to all trains and resets their wagons to a known-good state to prevent item fragmentation.

Factorio signals cannot differentiate between a single stack of items (e.g., `{ rails: 100 }`) and several fragmented, partial stacks of items that total the same amount.

## Logistic Outpost

![outpost](outpost.jpg)

The outpost may appear complex, but it's composed of several smaller, simpler, independent circuits that work together to provide the features I've described. I'll break them down layer by layer for analysis.

### The Circuit Bus & Module Interface

![circuit_bus](circuit_bus.jpg)

This is the connection interface between the modules and the station. It has four pairs of lamps connected by green and red wires. The station connects to the leftmost pair of lamps, and the three modules connect to the remaining pairs.

### Unloader Circuit

![unloader circuit](unloader_circuit.jpg)

The unloader circuit subtracts the logistic module's request signal from the station's storage. The logistic modules are not pictured here, but you can see them in the sections above and in my prior posts. The modules put a negative request signal onto the bus, which is used by the unloader circuit.

Items with a negative quantity are turned into an item mask with `each < 0` and an output of `each: 1`.

The train's contents are turned into a mask with `each > 0` and an output of `each: 1`.

When you combine these masks, you can perform a set union by checking for `each = 2` and outputting `each: 1`.

The result sets the filter inserters' items.

### Trash Circuit

![trash circuit](trash_circuit.jpg)

This circuit doubles the negative module request signal and subtracts it from the station's storage.

The positive results are then requested by the left buffer chest for each wagon.

The right buffer chests count the number of trashed items. When the count reaches a certain threshold (e.g., `T >= 200`), the station calls the trash train.

Remember, you can't set requests and count items in a chest at the same time.

To double the loading throughput, the inserters between the buffer chests are on their own smaller circuits with an `each < 100` condition.

### Bot Bootstrap

![bot bootstrap](bot_bootstrap.jpg)

This circuit bootstraps the initial logistic bots from either wagon of the seed train.

### Bot Loader

![bot loader](bot_loader.jpg)

A simple difference circuit reads from a combinator with the bot set-points (e.g., `{ logistic: 100, construction: 100 }`) and subtracts the current bot counts.

The result sets the requests on the requester chest.

### Combined Again And Close Up

![outpost zoom](outpost_zoom.jpg)

## Blueprints

You can download the logistic train blueprint book [here](blueprint.txt).

And a simple rail blueprint book [here](rails.txt).

## Sandbox Download

The screenshots from this post are from a sandbox world I used to demonstrate and explain the updated logistic train circuits.

You can download it [here](sandbox.zip) and play with it yourself.

## Bugs & Feedback

Please raise an issue [here](http://github.com/mason-larobina/factorio) for any corrections or improvements.

## Update: Vanilla Blueprints & Sandbox

Vanilla blueprints can be found [here](vanilla-blueprint.txt) and the sandbox [here](vanilla-sandbox.zip).

## Discussion

In [/r/factorio](https://www.reddit.com/r/factorio/comments/v5weot/logistic_train_upgrades_for_factorio_v11_part_5/) and [/r/technicalfactorio](https://www.reddit.com/r/technicalfactorio/comments/v5yc5w/logistic_train_upgrades_for_factorio_v11_part_5/).

Enjoy! 😁
