M140 S50 // set bed temperature to 50°C
M104 S50 // set hotend temperature to 50°C


@CHAMBERWAIT 22  ; Custom command to wait for chamber to reach  desired temp in °C


; End G-code for Prusa MK3S / Marlin
M104 S0            ; turn off hotend
M140 S0            ; turn off bed
M107               ; turn off fan
G91                ; relative positioning
G1 Z+10 F1000      ; lift Z by 10mm
G90                ; absolute positioning
G1 X0 Y200 F3000   ; move print head to the front
M84                ; disable motors
M117 Print complete