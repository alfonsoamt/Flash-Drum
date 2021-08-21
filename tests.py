from flash import *
from stream import Stream

if __name__ == '__main__':
    flash = FlashDrum()
    C1 = 'chlorobenzene'
    C2 = 'styrene'
    C3 = 'p-xylene'
    z = {C1: 0.3, C2: 0.5, C3 : 0.2}

    c = parameters([C1, C2, C3])

    Tf = 435
    Pf = 200
    feedStream = Stream('Feed', Tf, Pf, 1000000, z)
    flash.setFeedStream(feedStream)
    T = 460
    P = 200

    flash.isothermal(T, P, c, True)
    print(flash.Streams(True))
    # feedStream = Stream('Feed', Tf, Pf, 100, z)
    # flash.setFeedStream(feedStream)
    # flash.adiabatic(P, c)
    # flash.Streams()