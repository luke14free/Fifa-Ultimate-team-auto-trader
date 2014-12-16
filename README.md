FUT Auto Trade Concept
=======

The idea here is to try to implement a "arbitrage-like" mechanism to create money from zero in Fifa Ultimate team by leveraging market imperfections. It's fascinating to study how the FUT market is so similar to the finance one.

Included is a simple experiment trying to buy contracts at a very low price in the market by bidding on many of them and resell them for a slightly higher price. The script requires you to install https://github.com/oczkers/fut and it will require a config.py file structured this way:

```python
import fut14

def connect():
    return fut14.Core('yourPsn@Email', 'yourPassword', 'yourSecretAnswer', platform='ps3', debug=True)
```

UPDATE
====

From this year (Fifa 2015), EA esplicity forbids you to do this kind of stuff. 
http://www.easports.com/fifa/news/2014/fifa-ultimate-team-coin-selling-and-buying-bans

This is just a personal experiment done before the announcement (Fifa 14), I am leaving it for reference.
