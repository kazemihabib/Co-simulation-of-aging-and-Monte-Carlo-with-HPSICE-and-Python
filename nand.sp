*SIMPLE NMOS INVERTER
.include '32nm_LP.pm'
* This line includes the model file
* .PROBE DC vth0

** Sources ***********
VD VDD 0 DC 0.9V
.param vdd=0.9
.param c=GAUSS(1,0.2,3)
.param d=GAUSS(1,0.2,3)
* .global vdd
*VIN IN 0 DC 0v
.option measform=3
*3 yani exerl  0 mt0 mirizieh
.option random_generator=srs
************PWL customise
* vin in gnd PWL
* + 0n 0v
* +3990p 0v
* + 4n 0.9v
* +14.9n 0.9v
* +15n 0.9v
* +18999p 0.9v
* +19n 0v
* +22n 0v
* +34.9n 0v
* +35n 0.9v
**************pulse 
vin in1 0 pulse 0 0.9 1ns 5ps 5ps 1.5n 3n
vin1 in2 0 pulse 0 0.9 1ns 5ps 5ps 2.5n 5n

** Inverter Netlist *****
M1 out in1 x 0  nmos L=32n*c  W=32n*d
M2 x in2 0 0  nmos L=32n*c  W=32n*d
M3 OUT IN1 vdd vdd pmos L=32n*c  W=64n*d
M4 OUT IN2 vdd vdd pmos L=32n*c  W=64n*d
c1  out 0 2ff  // tarif khazzan be in shekl hast ke ba C shoro mishe v baad bein 2 greh hast v dar akhar megdaresh ke alan 2 fento farad hast
c2  in 0 2ff   // in khazan haro gozashtim chon nemodar kheili smooth tar mishe dar vorodi v khurogi


.measure tran tlh trig v(in1) val = 'vdd/2'  rise=1 targ v(out) val = 'vdd/2'  fall=1
.measure tran  thl trig v(in1) val = 'vdd/2' fall = 1 targ v(out) val = 'vdd/2' rise =1
.measure tran tpd param='(tlh+thl/2)'
.option post
.tran 10p 40n sweep monte=1000
.temp 70

.measure tran AvgPower Avg Power from = 10ps to = 40ns

*<---BeginAging--->

.mosra reltotaltime='10*365*24*60*60' 
*bala yani vaghti aging hesab mikonim ta 6 saal hesab kon 
+relstep=6.3e+7
*alan dafaat hesab kardan hast masalan mige 6.3e+7 bar chek kon ta be 6sal beresi
+agingstart=10p agingstop=40n
*in yani aging ke baad dakhel nemodar mikhay neshon bedi az 10p shoro mishe ta 40n

.model NCH_RA mosra level=1 tit0=5e-7 titfd=7.5e-10 tittd=1.45e-20 tn=0.23 tk=0.25 totde=1 
*in parameter haye bala donestanesh kheili mohem nist v ye seri chiz hayeh sabet hastand v agar khastim meghdari dar nahayat avaz beshe kafie ina ro kam kam taghir bedim ta dar nahayat be on megdrat moredeh nazar beresim
*alan tn faghat mohemeh bedonim chi hast ke darsad dar stress gozashtan tranzistor hast masalan mige be andazeh 0.23 in gate tranzistor to dar stress bezar
+relmode=2 HciThreshold=0 SimMode=1
* relmode ham ba addadi ke behesh entesab midim migim ke az kodom ravesh aging mikhaim estefadeh konim .
.appendmodel NCH_RA mosra nmos nmos
.appendmodel NCH_RA mosra pmos pmos
* alan aging haee ham ke tarif kardim be tamam nmos haye madar taasir mideh

* agar khastim be yek seri khas az tranzistor haye khas aging asar bedim bayad library hashon ro avaz konim

 .option appendall
 .option mosrasort=delvth0

*<---EndAging--->
.END
* AZ subckt barayeh moshakhas kardan madule v seda zadan estefadeh mishe k kheili baad hast v man natonestam bahash kar konam.
*.subsckt not in out
*.ends
