** Layout Netlist, pegasus precompare
** 

.subckt sram_6t BL BLB Q QB VDD VSS WL 
MX66/M0 Q QB VDD VDD P1SVT L=1.8e-08 nf=1 nfin=2 m=1 
MX67/M0 QB Q VDD VDD P1SVT L=1.8e-08 nf=1 nfin=2 m=1 
MX68/M0 Q WL BL VSS N1SVT L=1.8e-08 nf=1 nfin=2 m=1 
MX69/M0 BLB WL QB VSS N1SVT L=1.8e-08 nf=1 nfin=2 m=1 
MX70/M0 QB Q VSS VSS N1SVT L=1.8e-08 nf=1 nfin=4 m=1 
MX73/M0 Q QB VSS VSS N1SVT L=1.8e-08 nf=1 nfin=4 m=1 
.ends


