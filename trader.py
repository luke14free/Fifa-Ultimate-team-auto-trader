import fut14
import time
import os

i=-1
successful_bids = []
fut = None
backoff = 5
bought_something = False

while not fut:
    try:
        fut = fut14.Core('luke14free@sharklasers.com', 'Londra14', 'corletto', platform='ps3', debug=True)
    except:
        print "Failed connecting, retrying in %d.." % backoff
        backoff += 5
        time.sleep(backoff)

print "Connected.."

def balance():
    tp = fut.tradepile()
    wl = fut.watchlist()
    t = filter(lambda i: i['resourceId'] == 1615613739, tp)
    w = filter(lambda i: i['bidState'] == "highest" and i['resourceId'] == 1615613739, wl)
    credits = fut.credits
    #os.system("clear")
    print "CREDITS: %d - current est. balance: %d (Trading: %d items (%d) - Won: %d (%d))" % (credits, len(t)*250+len(w)*250+credits, len(t),len(tp), len(w),len(wl))


def emptyTradePile():
    """
    print "Handshake"
    fut.keepalive()
    print "Success"
    print "Emptying tradepile"
    tp = fut.tradepile()
    print "TP size:", len(tp)
    for item in tp:
        if item['tradeState'] == "closed":
            try:
                deleted = fut.tradepileDelete(item['tradeId'])
                print "Deleted: ", item['tradeId'], " - ", deleted
                time.sleep(3)
            except:
                print "Could not delete from TL: ", item
                time.sleep(3)
    """
    try:
        fut.relist(clean=True)
    except:
        pass
    tp_size = len(fut.tradepile())
    #print "Tradepile size:", tp_size,"/ 30"
    return tp_size

def emptyWatchList():
    #print "Handshake"
    fut.keepalive()
    #print "Success"
    #print "Emptying watchlist"
    wl = fut.watchlist()
    #print "WL size:", len(wl)
    for item in wl:
        if item['currentBid'] > 150 and item['itemType'] == 'contract':
            deleted = fut.watchlistDelete(item['tradeId'])
            #print "Deleted: ", item['tradeId'], " - ", deleted
            time.sleep(3)
            #except:
            #print "Could not delete from WL: ", item
            time.sleep(3)
    #print "WL size:", wl_size,"/ 100"
    return wl_size

def sellAllContracts():
    tp_size = emptyTradePile()
    successful_bids = fut.watchlist()
    wl_size = emptyWatchList()
    #print "Handshake"
    fut.keepalive()
    #print "Success"
    print "DEBUG: Selling phase"
    while successful_bids and tp_size < 30:
        item = successful_bids.pop()
        if item['currentBid'] == 150 and item['itemType'] == 'contract' and item['expires'] == -1 and item['bidState'] == 'highest': #then we were the last bidders and we can sell!
            try:
                moved = fut.sendToTradepile(item['tradeId'], item['id'])
                if moved:
                    1
                    #print "Item moved to tradepile"
                fut.sell(item['id'], 200, buy_now=250, duration=3600)
                time.sleep(3)
                print "DEBUG: Successfully put on the mkt!"
                tp_size += 1
            except:
                #print "Failed selling:", item
                time.sleep(3)
                pass #fail silently..
        else:
            1
            #print "Trade state not good or not won: ", item['tradeState'] == "closed", "price:", item['currentBid'], "type:", item['itemType']

    print "DEBUG: Done selling! Tp size: ", tp_size


while 1:
    try:
        emptyWatchList()
	emtpyTradePile()
    except:
	pass
    balance()

    if (bought_something or len(fut.watchlist()) > 5) and len(fut.tradepile()) < 30: #wait for at least 3 spots to open
        sellAllContracts()
        bought_something = False

    while fut.credits < 150 or (len(fut.watchlist()) >= 96 and len(fut.tradepile()) >= 28):
        #Nothing to do.. Wait for a minute or so and check again
        balance()
        print "Waiting 120 secs.."
        fut.keepalive()
        i = -1
        time.sleep(120)
        try:
            fut.relist(clean=True)
        except:
            pass
    i+=1

    print "DEBUG: Iteration n.", i
    if i % 5 == 0:
        #print "Handshake"
        fut.keepalive()
        #print "Success"

    if i >= 10:
        i = 0 #go back to newest bids

    print
    try:
        players = fut.searchAuctions('development', category='contract', start=i*16, level='gold', max_price = 150)
    except:
        fut.keepalive()
        players = fut.searchAuctions('development', category='contract', start=i*16, level='gold', max_price = 150)

    if not players:
        #print "Nothing found"
        time.sleep(5)
        continue
    for player in players:
        #bid_price = max([(player['currentBid'] + 50), (player['startingBid'])])
        #if player['discardValue'] > 310 or max([(player['currentBid'] + 50), (player['startingBid'])]) > 250: continue
        bid_price = 150
        #bid_price = 600 if player['discardValue'] >= 640 else max([(player['currentBid'] + 50), (player['startingBid'])])

        if player['expires'] < 15:  break

        if player['resourceId'] == 1615613739 and max([(player['currentBid'] + 50), (player['startingBid'])]) <= 150: # (player['discardValue'] - bid_price) > 0: #extra security check
            #print "Bidding for", player['discardValue'], "at", bid_price, "expires in:", player['expires']
            try:
                bid = fut.bid(player['tradeId'], bid_price)
            except:
                #print "Weird error, (timed out? Moving to next batch)"
                bid = False
                break

            if bid:
                print "DEBUG: Successful bid!"
                #print "Waiting 3 seconds.."
                bought_something = True
                time.sleep(3)
            else:
                #print "Unsuccessful"
                #print player
                #print "Waiting 3 seconds.."
                time.sleep(3)

            continue #Too late to bid for others
        else:
            1
            #print "Not bidding for", player['discardValue'], "at", bid_price, "exp", player['expires'], "RID:", player['resourceId'], "type: ", 'allenatore' if player['resourceId'] != 1615613739 else 'giocatore'
    #print "Waiting 3 seconds.."
    time.sleep(3)
