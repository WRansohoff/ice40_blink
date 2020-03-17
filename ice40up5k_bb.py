import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from nmigen_boards.resources import *

#######################################
# Board definition file for Lattice's #
# iCE40UP5K-SG48 breakout board.      #
#######################################
# TODO: I'm not sure what 'IOStandard' does, but...CMOS sounds good?

__all__ = [ 'UP5KBBPlatform' ]

class UP5KBBPlatform( LatticeICE40Platform ):
  device      = 'iCE40UP5K'
  package     = 'SG48'
  default_clk = 'clk12'
  resources   = [
    # 12MHz oscillator is the only clock input (J51 must be connected)
    Resource( 'clk12', 0, Pins( '35', dir = 'i' ), Clock( 12e6 ),
              Attrs( GLOBAL = True, IO_STANDARD = 'SB_LVCMOS' ) ),

    # LEDs; one R, one G, one B. Classic.
    *LEDResources( pins = '39 40 41', invert = True,
                   attrs = Attrs( IO_STANDARD = 'SB_LVCMOS' ) ),
    Resource( 'led_b', 0, PinsN( '39', dir = 'o' ),
              Attrs( IO_STANDARD = 'SB_LVCMOS' ) ),
    Resource( 'led_g', 0, PinsN( '40', dir = 'o' ),
              Attrs( IO_STANDARD = 'SB_LVCMOS' ) ),
    Resource( 'led_r', 0, PinsN( '41', dir = 'o' ),
              Attrs( IO_STANDARD = 'SB_LVCMOS' ) ),

    # There are 4 DIP switches on the board, but their pull-ups
    # are not populated by default, so I'm not defining them here.
    # I think they're on pins 23, 25, 34, 43 though.

    # SPI Flash connection.
    *SPIFlashResources( 0, cs = '16', clk = '15',
                        miso = '17', mosi = '14',
                        attrs = Attrs( IO_STANDARD = "SB_LVCMOS" ) )
  ]
  connectors  = [
    # Aardvark connector.
    Connector( 'aardvark', 0, '- - - - 14 - 15 17 16 -' ),
    # PMOD connector.
    Connector( 'pmod', 0, '16 14 17 15 - - 27 26 32 31 - -' ),
    # Header 'A'.
    # (Let's call it J0, even though it's marked J52 on the board...)
    Connector( 'j', 0, '- - 39 14 40 17 - 15 41 16 - -' ),
    # Header 'B'. (J1)
    Connector( 'j', 1, '- - 23 - 25 - 26 36 27 42 '
                       '32 38 31 28 37 15 34 - 43 -' ),
    # Header 'C'. (J2)
    Connector( 'j', 2, '- 12 4 21 3 13 48 20 45 19 '
                       '47 18 44 11 46 10 2 9 - 6' )
  ]

  def toolchain_program( self, products, name ):
    iceprog = os.environ.get( 'ICEPROG', 'iceprog' )
    with products.extract( '{}.bin'.format( name ) ) as bitstream_fn:
      subprocess.check_call( [ iceprog, bitstream_fn ] )
