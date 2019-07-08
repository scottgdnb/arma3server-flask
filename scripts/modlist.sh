#!/bin/bash

MODPATH="mods/"
MODLIST="/home/steam/arma3/mods.cfg"

getArray() {
    array=() # Create array
    while IFS= read -r line # Read a line
    do
        array+=("$line") # Append line to the array
    done < "$1"
}


getArray "${MODLIST}"

echo ${array[*]}
