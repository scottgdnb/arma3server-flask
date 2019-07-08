#!/bin/sh  
var=$(/bin/systemctl show -p SubState --value arma3.service)
echo "$var"
