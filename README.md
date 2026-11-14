# t2b-yte
Turns any type or data in python into a series of bytes that can be converted back.

The result can be extremely long so it's recommended to losslessly compress before saving.
As a shortcut for saving the bytes can be turned into a string or int before using.

Note for int saving:
Most computers only support up to about 10^308 for an int but this integer well overpasses that limit.
