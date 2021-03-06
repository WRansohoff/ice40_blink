from nmigen import *
from nmigen.back.pysim import *
from ice40up5k_bb import *
from upduino import *

import sys

# LED blinker to test that nMigen runs on an FPGA board.
class Blinker( Elaboratable ):
  def __init__( self ):
    self.counter = Signal( 32, reset = 0x00000000 )
    self.which_led = Signal( 3, reset = 0b000 )

  def elaborate( self, platform ):
    m = Module()

    rled = platform.request( 'led_r', 0 )
    gled = platform.request( 'led_g', 0 )
    bled = platform.request( 'led_b', 0 )

    with m.If( self.counter >= 12000000 ):
      m.d.sync += [
        self.counter.eq( 0 ),
        self.which_led.eq( self.which_led + 1 )
      ]
    with m.Else():
      m.d.sync += self.counter.eq( self.counter + 1 )

    m.d.comb += [
      rled.o.eq( self.which_led & 0b001 ),
      gled.o.eq( ( self.which_led & 0b010 ) >> 1 ),
      bled.o.eq( ( self.which_led & 0b100 ) >> 2 )
    ]

    return m

if __name__ == "__main__":
  if len( sys.argv ) != 2:
    print( 'Usage: python3 blink.py <board>\r\n'
           'Accepted boards:\r\n'
           '  "up5k_bb" (Lattice iCE40UP5K-SG48 breakout board)\r\n'
           '  "upduino" (Gnarly Grey Upduino board)' )
  elif sys.argv[ 1 ].lower() == 'up5k_bb':
    UP5KBBPlatform().build( Blinker(), do_program = True )
  elif sys.argv[ 1 ].lower() == 'upduino':
    UpduinoPlatform().build( Blinker(), do_program = True )
  else:
    print( 'Unrecognized board: %s\r\n'
           'Accepted boards:\r\n'
           '  "up5k_bb" (Lattice iCE40UP5K-SG48 breakout board)\r\n'
           '  "upduino" (Gnarly Grey Upduino board)'
           %( sys.argv[ 1 ] ) )
