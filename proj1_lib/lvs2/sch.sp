** Schematic Netlist, pegasus precompare
** 

.subckt sram_6t BL BLB Q QB VDD VSS WL 
MMPM1 QB Q VDD VDD P1SVT m=1 l=1.8e-08 nfin=2 nf=1 
MMPM0 Q QB VDD VDD P1SVT m=1 l=1.8e-08 nfin=2 nf=1 
MMNM3 Q WL BL VSS N1SVT m=1 l=1.8e-08 nfin=2 nf=1 
MMNM2 BLB WL QB VSS N1SVT m=1 l=1.8e-08 nfin=2 nf=1 
MMNM1 QB Q VSS VSS N1SVT m=1 l=1.8e-08 nfin=4 nf=1 
MMNM0 Q QB VSS VSS N1SVT m=1 l=1.8e-08 nfin=4 nf=1 
.ends


