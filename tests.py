from flash import *
from stream import Stream

if __name__ == '__main__':
    flash = FlashDrum()
    C1 = 'benzene'
    C2 = 'toluene'
    z = {C1: 0.5, C2: 0.5}

    c = parameters([C1, C2])

    Tf = 380
    Pf = 300
    feedStream = Stream('Feed', Tf, Pf, 100, z)
    flash.setFeedStream(feedStream)
    T = 405
    P = 250

    flash.isothermal(T, P, c, True)
    print(flash.Streams(True))
    # feedStream = Stream('Feed', Tf, Pf, 100, z)
    # flash.setFeedStream(feedStream)
    # flash.adiabatic(P, c)
    # flash.Streams()