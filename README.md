# Hedgehog
### A Mate Indicator for Hamster
This is an indicator for the Hamster GNOME Timetracker. (https://github.com/projecthamster/hamster)
Hamster brings its Gnome Shell Extension which shows whether your time is actually tracked for a project and how long you have been working 
at ths project.
Unfortunately no Applet or Indicator for the Mate Desktop (https://mate-desktop.org/) existed. 

Hedgehog is exactly this: A Mate Indicator for the Hamster Timetracker. It is tested for Ubuntu Mate but shout work with other Distributions too.

If running it shows what you are doing in the Panel.

## Prereqisites
A Linux distribution with the Mate desktop (for instance Ubuntu Mate)
Hamster Timetracker is installed

## Installation
    git clone ...
    cd hedgehog-reduced
    cp config.py.dist config.py

In config.py change the db_path and hamster_path according to your system.
It should work out of the box with Ubuntu Mate.

Start it:

    ./hedgehog-indicator.py

It makes sense to put this into the autostart configuration.
