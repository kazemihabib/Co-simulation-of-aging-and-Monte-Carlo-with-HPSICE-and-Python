# Co-simulation of aging and Monte Carlo with HPSICE and Python

# About

HSPICE can not perform Monte Carlo (MC) simulations while considering aging effects. I developed a python wrapper that automatically performs MC and aging simulations using HPSICE to save engineering hours.

# Requirements

    windows or linux
    python3
    hspice

# How does it work

Step1:

1. Parses the spice file and reads the distribution and monte parameters
2. Removes the distribution and monte parameters
3. For example if monte parameter was 10, it creates 10 versions of the given spice file
   but with width and length values changed according to the distributions it parsed previously
4. Runs the generated spice files
5. Parses the csv results and calculates the mean and sigma of delays

Step2:

1. Adds the aging section to step1 spice files
2. Runs the generated spice files
3. parses the csv results and calculates the mean and sigma of delays

# How to use

## Prepare the Environment

    Add the installation directory to your PATH variable, so the script can run the hspice.
    (For example in windows, Add "C:\synopsys\Hspice_L-2016.06-SP1\BIN" to your PATH variable)

## Install the python dependencies

    pip install -r requirements.txt

## How to write the spice script

    To use this wrapper, you do not need to know Python, just Add *<---BeginAging---> before the aging section and *<---EndAging---> after the aging section.
    With the help of these annotations, the wrapper will be able to remove the aging section in step1 and add it again in step2.

## How to Run

    python .\toolchain.py -i yourspicefilepath
