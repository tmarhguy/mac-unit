##############################################################################################################
#####  
#####                                       Pegasus LVS COMPARISON
#####  
#####  Version                       :   23.20-p013
#####  NVN Run Start                 :   Sun Oct 18 19:14:42 2026
#####  ERC Summary File              :   sram_6t.sum
#####  Extraction Report File        :   sram_6t.rep
#####  Comparison Report File        :   sram_6t.rep.cls
#####  Top Cell                      :   sram_6t  <vs>  sram_6t
#####  
#####  Run Result                    :   MATCH
#####  
#####  Run Summary                   :   [INFO]  ERC Results: Empty
#####                                :   [INFO]  Extraction Clean
#####  
#####  Layout Design                 :   proj1_lib sram_6t layout
#####  Schematic File                :   /vast/projects/radway/ese-5700-fall/tmarhguy/project_1/proj1_lib/lvs2/sram_6t.cdl (cdl)
#####  Rules File                    :   /vast/projects/radway/ese-5700-fall/tmarhguy/project_1/pvs/pvlLVS.rul
#####  Pin Swap File                 :   sram_6t.rep.cps
#####  
#####  Extraction CPU Time           :   0h 0m 1s - (1s)
#####  Extraction Exec Time          :   0h 0m 3s - (3s)
#####  Extraction Peak Memory Usage  :   26.00MB
#####  NVN CPU Time                  :   0h 0m 0s - (0s)                 
#####  NVN Exec Time                 :   0h 0m 2s - (2s)                 
#####  NVN Peak Memory Usage         :   244.99MB
#####  LVS Total CPU Time            :   0h 0m 1s - (1s)                 
#####  LVS Total Exec Time           :   0h 0m 5s - (5s)                 
#####  LVS Total Peak Memory Usage   :   244.99MB
#####  
##############################################################################################################


##############################################################################################################
#
#                                            CELL MATCH STATISTICS                                            
#
##############################################################################################################

Cell Statistic Descriptions                  | Count
---------------------------------------------+----------
Cells matched                                |         1
Cells expanded                               |         0
Cells not run                                |         0
Cells which mismatch                         |         0
---------------------------------------------+----------
Total                                        |         1


Cell Statistic Detail                        | Count
---------------------------------------------+----------
Cells with parameter mismatches              |         0
Cells with mismatched instance subtypes      |         0
Cells that have been blackboxed              |         0


##############################################################################################################
#
#                                             CELL MATCH SUMMARY                                              
#
##############################################################################################################

            |     Initial Pins     |     Compare Pins     |            | 
Cell        |   lay    :    sch    |   lay    :    sch    | Status     | Detail
------------+----------+-----------+----------+-----------+------------+-----------
sram_6t     |        7 :         7 |        7 :         7 | match      | 


##############################################################################################################
#
#                                                  LVS RULES                                                  
#
##############################################################################################################

Command Line LVS Rule Values
----------------------------

    layout_primary                          sram_6t {-top_cell sram_6t}
    schematic_primary                       sram_6t {-source_top_cell sram_6t}

LVS Rules Given in the Rules File
---------------------------------

    lvs_abort                               -softchk                               no  
    lvs_abort                               -supply_error                          no  
    layout_path                             /vast/projects/radway/ese-5700-fall/tmarhguy/project_1/proj1_lib/lvs2/sram_6t.gds.gz
    layout_format                           gdsii
    schematic_path                          /vast/projects/radway/ese-5700-fall/tmarhguy/project_1/proj1_lib/lvs2/sram_6t.cdl
    schematic_format                        cdl
    lvs_write_netlist                       -layout lvs.sp
    lvs_write_netlist                       -source sch.sp
                                             
    lvs_ignore_ports                        no  
    lvs_compare_port_names                  yes 
    lvs_find_shorts                         no  
    lvs_break_ambig_max                     32
    lvs_reduce_split_gates                  yes ...
    lvs_reduce                              yes -parallel_mos ...
    lvs_reduce_device                       C ( cmim ) -series PLUS MINUS no 
    lvs_reduce_device                       C ( cmim ) -parallel yes ...
    lvs_expand_cell_on_error                no  
    lvs_check_property                      R r r -tolerance 0
    lvs_check_property                      R l l -tolerance 0 -absolute
    lvs_check_property                      R w w -tolerance 0 -absolute
    lvs_check_property                      C ( cmim ) w w -absolute -tolerance 0
    lvs_check_property                      C ( cmim ) l l -absolute -tolerance 0
    lvs_check_property                      C ( cmim ) c c -tolerance 0
    lvs_check_property                      Q ( npn ) A A -absolute -tolerance 0
    lvs_check_property                      D A A -tolerance 0 -absolute
    lvs_check_property                      D P P -tolerance 0 -absolute
    lvs_check_property                      MN l l -absolute -tolerance 0
    lvs_check_property                      MN nf nf -absolute -tolerance 0
    lvs_check_property                      MN nfin nfin -absolute -tolerance 0
    lvs_check_property                      MP l l -absolute -tolerance 0
    lvs_check_property                      MP nf nf -absolute -tolerance 0
    lvs_check_property                      MP nfin nfin -absolute -tolerance 0
    lvs_report_file                         sram_6t.rep
    lvs_report_max                          50 -mismatched_net_limit 100 
    unit                                    -length u
    input_scale                             2000
    virtual_connect                         no  -colon
    virtual_connect                         yes -semicolon_as_colon
    virtual_connect                         no  -report
    virtual_connect                         -depth primary
    text_depth                              -primary

Default LVS Rule Values
-----------------------

    lvs_abort                               -check_device_for_property_rule no
    lvs_abort                               -missing_hcell no
    lvs_abort                               -erc_error yes
    lvs_abort                               -inconsistent_reduction yes
    layout_case_sensitive                   no
    // layout_cpf_file                       
    // schematic_cpf_file                    
    schematic_case_sensitive                no
    // hcell_file                            
    // hcell                                 
    // lvs_exclude_hcell                     
    // lvs_delete_cell                       
    lvs_push_devices                        yes
    lvs_push_devices_properties             no
    lvs_netlist                             yes -substrate_comment
    lvs_netlist                             yes -box_contents
    lvs_netlist                             yes -unnamed_box_pins
    lvs_netlist                             no -allow_inconsistent_model
    lvs_netlist                             yes -properties_comment
    // lvs_write_netlist_reduced             
    // lvs_delete_cell_pin                   
    // lvs_black_box                         
    // lvs_interposer                        
    lvs_spice                               yes -allow_floating_pins
    lvs_spice                               yes -allow_duplicate_subcircuit_names
    lvs_spice                               no  -conditional_ldd
    lvs_spice                               no  -prefer_pins
    lvs_spice                               no  -override_globals
    lvs_spice                               no  -redefine_param
    lvs_spice                               no  -replicate_devices
    lvs_spice                               no  -replicate_devices_enhanced
    lvs_spice                               yes -slash_is_space
    lvs_spice                               yes -keep_back_slash
    lvs_spice                               no  -allow_unquoted_strings
    lvs_spice                               no  -allow_inline_parameters
    lvs_spice                               no  -calculate_mos_area
    lvs_spice                               no  -strict_wl
    lvs_spice                               no  -cull_primitive_subcircuits
    lvs_spice                               no  -ignore_option_scale
    lvs_spice                               no  -show_neg_param_warning
    lvs_spice                               no  -scale_x_parameters
    lvs_spice                               yes -strict_subckts_order
    // lvs_spice_option                      
    lvs_reverse_wl                          no
    // lvs_spice_multiplier_name             
                                             
    lvs_compare_case                        no
    lvs_cname                               no  -cell
    lvs_cname                               yes -pin
    lvs_cname                               yes -net
    lvs_cname                               no  -instance
    lvs_non_user_name                       -port "^[0-9]+$"
    lvs_non_user_name                       -net  "^[0-9]+$"
    // lvs_non_user_name                    -instance 
    lvs_out_of_range_exclude_zero           no
    // lvs_group_models                      
    lvs_strict_subtypes                     no
    lvs_exact_subtypes                      no
    lvs_preserve_box_ports                  no
    // lvs_cpoint                            
    // lvs_power_name                        
    // lvs_ground_name                       
    // lvs_cell_list                         
    // lvs_device_type                       
    lvs_auto_pin_swap                       yes -swap_threshold 4000000
    lvs_swap_non_cpoint_pins                yes
    // lvs_swap_pins                         
    lvs_all_cap_pins_swappable              no
    lvs_builtin_device_pin_swap             yes
    // lvs_join_nets                         
    lvs_global_sigs_are_ports               yes
    lvs_discard_pins                        no
    lvs_filter                              no  -bipolar
    lvs_filter                              no  -capacitors
    lvs_filter                              no  -diodes
    lvs_filter                              no  -mos
    lvs_filter                              no  -resistors
    // lvs_filter_option                     
    // lvs_filter_device                     
    // lvs_filter_device_keep_net            
    lvs_reduction_priority                  -parallel
    lvs_derive_logic                        yes -sram
    lvs_derive_logic                        no  -dram
    lvs_derive_logic                        no  -rom
    lvs_recognize_gates                     -all  
    // lvs_recognize_gates_tolerance         
    lvs_reduce                              yes -parallel_bipolar
    lvs_reduce                              yes -parallel_caps
    lvs_reduce                              yes -series_caps
    lvs_reduce                              yes -parallel_diodes
    lvs_reduce                              no  -series_diodes
    lvs_reduce                              no  -series_mos
    lvs_reduce                              yes -parallel_resistors
    lvs_reduce                              yes -series_resistors
    // lvs_reduce_do_not_merge               
    lvs_expand_on_device_climbing           no
    lvs_expand_unbalanced_cells             yes
    // lvs_check_all_properties_by_name      
    // lvs_property_map                      
    // lvs_transfer_property                 
    lvs_warn_max                            50
    lvs_inconsistent_reduction_threshold    1000000
    // lvs_report_opt                        
    lvs_report_units                        yes
    lvs_keep_data                           no
    lvs_keep_source_cells                   no
    lvs_create_match_db                     no
    // lvs_map_device                        
    unit                                    -resistance ohm
    unit                                    -capacitance pf
    lvs_verilog_bus_map_by_position         no
    lvs_verilog_keep_backslash              no
    lvs_verilog_detect_buses                no
    lvs_do_not_normalize                    no
    // lvs_generic_device                    
    virtual_connect                         no  -colon
    virtual_connect                         yes -semicolon_as_colon
    // virtual_connect                      -name 
    virtual_connect                         no -report
    virtual_connect                         no -incremental
    lvs_preserve_parameterized_cells        no
    lvs_check_color                         no
    // lvs_schematic_color_path              
    // lvs_assign_conflict_layer             
    // lvs_conflict_layer_check             
    lvs_check_color_label                   no
    // lvs_preserve_cells                    
    port                                    -depth -primary
    lvs_high_shorts_max                     10000000

Effective LVS Rule Values
-------------------------

    lvs_swap_non_cpoint_pins                yes -unbound_pin_threshold 10000
    virtual_connect                         no  -report


##############################################################################################################
#
#                                               CELL COMPARISON                                               
#
##############################################################################################################

                              +------------------------------------------------+
                              |                                                |
                              |        ------->>>   MATCH   <<<-------         |
                              |                                                |
                              |             sram_6t  <vs>  sram_6t             |
                              |                                                |
                              |                                                |
                              +------------------------------------------------+

+===[sram_6t]=================================================================================================
|                                                 STATISTICS                                                  
+=============================================================================================================


                |     Original      |     Reduced      
Cell            |   lay   :   sch   |   lay   :  sch
----------------+---------+---------+---------+--------
MP [4 pins]     |         :         |         :        
 MP(P1SVT)      |       2 :       2 |       2 :       2
MN [4 pins]     |         :         |         :        
 MN(N1SVT)      |       4 :       4 |       4 :       4
----------------+---------+---------+---------+--------
Total           |       6 :       6 |       6 :       6
================+=========+=========+=========+========
Pins            |         :         |       7 :       7
Nets            |         :         |       0 :       0
================+=========+=========+=========+========

+===[sram_6t]=================================================================================================
|                                           INITIAL CORRESPONDENCES                                           
+=============================================================================================================

Type     | Name
---------+---------------------------
Pin      | BL BLB Q QB VDD VSS WL


##############################################################################################################
#
#                                                END OF REPORT                                                
#
##############################################################################################################

