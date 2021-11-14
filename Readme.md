#Hspice toolchain

# Requirements

    windows or linux
    python3
    hspice

# What is hspice toolchain

hspice can not simulate process variation and aging together, this toolchain simualtes process variation and aging together.

# How to it works

Step1:

1. Parses the spice file and reads the distribution and monte parameters
2. Removes the distribution and monte parameters
3. For example if monte parameter was 10, it creates 10 versions of the given spice file
   but with width and length values changed according to the distributions we parsed previously
4. Runs our generated spice files
5. Parses the csv results and calculates the mean and sigma of delays

Step2:

1. Adds the aging section to step1 spice files
2. Runs the generated spice files
3. parses the csv results and calculates the mean and sigma of delays

# How to use

## Preparation the environment

    Add the installation directory to your path variable so the script can run the hspice.
    (e.g. windows: Add "C:\synopsys\Hspice_L-2016.06-SP1\BIN" to your path variable in environment variables)

## Install the python dependencies

    pip install -r requirements.txt

## how to write spice script

    Toolchain reads all the parameters from the source so you don't need to pass
    any extra parameter to the toolchain.
    toolchain reads the distribution parameters. e.g. .param c=GAUSS(1,0.2,2.1)
    toolchain reads the monte parameter. e.g. .tran 10p 40n sweep monte=2

    Add *<---BeginAging---> before aging section and *<---EndAging---> after aging section
    with the help of these annotations toolchain removes the aging section in the step1 and
    adds it again in the step2.

## run

    python .\toolchain.py -i yourspicefilepath
