# Logistic Circuits Part 4 - Outpost refinements, self-contained modules

A major annoyance remains after the improvements in [parts 1, 2 & 3](../../../).

Changing or upgrading each of the logistic modules requires updating three
separate locations:

1. The station-wide buffer/request circuit (I run all the logistic stations as
   an isolated bot network so that science packs don't eat my rails and
   furnaces).
1. The loader circuit for the first wagon.
1. The loader circuit for the second wagon.

![Paste 3](2020-06-01-paste3.jpg)

Ideally I would plonk down the new module and have all three signals update
automatically. I can't do this due to a poor choice I made when creating the
first module. Let's explode one and see:

![Exploded module](2020-06-01-joined.jpg)

See both the constant combinators are joined on both the red 1 and the green
`CHECK 50%` circuit? Back at the station there is no way to process each
constant combinator separately for each wagon.

The first step to fixing this is feeding both of the constant combinators into
another combinator via separate red and green connections:

![Separate](2020-06-01-separate.jpg)

But adding more components to the module increases the width of the outpost
station to 13 blocks:

![Wide](2020-06-01-wide.jpg)

I briefly considered moving some of the components into the unused part above
the lights:

![Over under](2020-06-01-over-under.jpg)

Which has its own annoyances too: no longer able to deconstruct a module with a
single drag (`Alt+D`).

What if it is possible to reduce the size of the modules instead? There are
common elements to each of the modules:

* Requesting the train
* The 50% check
* Diode
* Constant combinators

![Common](2020-06-01-common.jpg)

Another way of doing the 50% stock check is to double the outpost contents
signal on the circuit interface. From `have - (want/2) < 0` to `(2*have) - want
< 0`.

Keeping `[*each] / -2` from the prior circuit would have persisted a bug where
`car: 1, fuel: 1` are rounded down to 0's. The `want * -1` is subtracted from
the `2*have`. Any negative values enable the train request.

![New module](2020-06-01-new-module.jpg)

Here's the refactored outpost with the circuit interface changes:

![New outpost](2020-06-01-new-outpost.jpg)
> [blueprint.txt](2020-06-01-new-outpost.txt)

The `have*2` doubles the logistic chest contents. The `-want*2` up top is the
200% threshold changes for the trash circuit. The default outpost thresholds are
restock if `<50%` and trash if `>200%` for each item.

And on the topic of the trash circuit, I added another two combinators to handle
the rounding problems for `<4` items (`EXACT TRASH`).

The right-most trash chest takes the full raw trash signal. The two additional
combinators take that signal and:

* `[*each] / 4` to spread the load across all 4 chests (rounds down for `<4`).
* Then `[*each] * -3` (equivalent to -75%) to correct the signal on the
  right-most chest.

Anything that is `<4` will correctly land in the right-most chest. Anything `>4`
will be evenly spread across the 4 chests.

Another change on the bottom-left adds a 5th unloader. This is so that there is
overlap with both wagons on the trash train. While the change from requester
chests to buffer chests made the trash items available to the logistic network
-- they wouldn't be moved back into storage. Without any unloader overlap with
both trash wagons, those items would have to round-trip through the logistic
trains. One unloader is slow -- but it's also a rare edge case, increase it if
needed.

The final change is the public green diode moved from the end of the station
(offscreen to the left) to near the circuit interface. I embed the outpost
station into many other contraptions and sometimes the entrance is curved.
Easier to adjust the system if the components are densely packed into a smaller
footprint.

## Loader improvements

With the module improvements, I now have a trivial way to connect the two module
constant combinators to the two wagon loading circuits with red and green wires:

![New loader](2020-06-01-new-loader.jpg)

The combined request signal (that is negative) goes into the station buffer
system.

Now the upgrade flow is:

1. Make adjustments in the field.
1. Copy-paste onto the station module (and remember that the flush circuit
   will reset the buffer chests when changes are detected).

The dream of self-contained, multi-purpose modules that can be used the same way
at the outpost and station is finally reality!

## Depot improvements

I've been messing with some new designs for the stations, I think I prefer this
over the previous iteration but may still move the trash train to the left with
the train stacker:

![Depot stations](2020-06-01-depot-stations.jpg)
![Depot stacker](2020-06-01-depot-stacker.jpg)

This allows me to add new station types on the right and add room for more
trains on the left without the two colliding.

I'm also experimenting with that loop junction and some two-way track which
forces all logistic trains to loop through (and wait in) the stacker on the way
to the loading stations.

The tiny circuit bottom right is the buffer circuit which will request items
from the main logistic network (request if `<10x`, trash if `>20x`).

## Blueprints

Contains latest outpost, depot, module & train blueprints:

[blueprint-book.txt](2020-06-01-blueprint-book.txt)

Should work out of the box (but you need a ~global green rail circuit network)!

## Contact

Would love you hear your feedback, corrections, contributions & fixes!

Email: mason.larobina@gmail.com or raise an issue on the [GitHub
repo](http://github.com/mason-larobina/factorio).

For updates, star the repo or follow:

https://github.com/mason-larobina/factorio/commits/master.atom
