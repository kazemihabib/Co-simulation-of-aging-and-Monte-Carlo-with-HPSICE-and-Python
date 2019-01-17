.include '32nm_LP.pm'

.param vdd_me = 0.9
 
.global vdd
VDD VDD 0 DC 0.9V

.param c=GAUSS(1,0.20,1)
.param d=GAUSS(1,0.20,1)

.option  measform = 3
vin ina 0 pulse 0 0.9 2ns 5ps 5ps 1.5n 3n 

vin1 inb 0 pulse 0 0.9 1ns 5ps 5ps 1.5n 3n

M1  ss ina 0 0  nmos L=32n*c W=64n*d
M2  OUT inb ss 0 nmos L=32n*c W=64n*d
M3  OUT INa vdd vdd pmos L=32n*c W=64n*d
M4  OUT INb vdd vdd pmos L=32n*c W=64n*d


.option post
.tran 10p 40n sweep monte=10
.measure tran AvgPower Avg Power from = 10ps to = 40ns
.measure  tran  DELAY_fall_a  trig  V(ina)  val='vdd_me/2'  rise=1  targ V(out) val='vdd_me/2'  fall=1
.measure  tran  DELAY_fall_b  trig  V(inb)  val='vdd_me/2'  rise=1  targ V(out) val='vdd_me/2'  fall=1
.measure  tran  DELAY_rise_a  trig  V(ina)  val='vdd_me/2'  fall=1  targ V(out) val='vdd_me/2'  rise=2
.measure  tran  DELAY_rise_b  trig  V(inb)  val='vdd_me/2'  fall=1  targ V(out) val='vdd_me/2'  rise=1

.mosra reltotaltime='3*365*24*60*60'

.model NC mosra level=1 tit0=5e-7 tit7td=7.5e-10 tittd=1.45e-20 tn=0.23 tk=0.23 totde=1 +relmode=2 HciThreshold=0 SimMode=1
.appendmodel NC mosra nmos nmos
.appendmodel NC mosra pmos pmos

.end