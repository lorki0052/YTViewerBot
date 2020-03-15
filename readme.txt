1)install tor-browser
2)find "torrc" file in : tor-browser-folder -> data -> tor -> torrc
3)replace content on :

# This provides a port for our script to talk with. If you set this then be
# sure to also set either CookieAuthentication *or* HashedControlPassword!
#
# You could also use ControlSocket instead of ControlPort, which provides a
# file based socket. You don't need to have authentication if you use
# ControlSocket. For this example however we'll use a port.

ControlPort 9051

# Setting this will make Tor write an authentication cookie. Anything with
# permission to read this file can connect to Tor. If you're going to run
# your script with the same user or permission group as Tor then this is the
# easiest method of authentication to use.

CookieAuthentication 1

# Alternatively we can authenticate with a password. To set a password first
# get its hash...
#
# % tor --hash-password "my_password"
# 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF
#
# ... and use that for the HashedControlPassword in your torrc.

HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF

SocksPort 9052
SocksPort 9053
SocksPort 9054
SocksPort 9055

4)launch from "launcher.ps1" (but u need edit him with correct path to project)