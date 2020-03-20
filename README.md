# nMigen FPGA test

This is a simple application to test running an nMigen design on actual FPGA hardware.

It's just a 'blinking LED' program that increments a 3-bit counter and toggles each color of an RGB LED based on each bit in the counter.

The `ice40up5k_bb.py` file contains a description of Lattice's `iCE40UP5K-SG48` breakout board:

https://www.digikey.com/short/z8ddhq

And the `upduino.py` file contains a description of Gnarly Grey's more affordable 'Upduino' board which uses the same `iCE40UP5K-SG48` chip:

http://www.gnarlygrey.com/

There's not much to see here; I just wanted to learn how to build an nMigen design and program an FPGA with it.

# Prerequisites

To run this example, you'll need to install `nmigen` and the main components of the `icestorm` toolchain:

https://github.com/nmigen/nmigen

https://github.com/nmigen/nmigen-boards

https://github.com/YosysHQ/yosys

https://github.com/cliffordwolf/icestorm

https://github.com/YosysHQ/nextpnr

Once everything is installed, you should be able to build and flash the program by running the `blink.py` file with the type of board you are using:

    python3 blink.py up5k_bb
    python3 blink.py upduino
