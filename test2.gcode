; Set bed temperature to 100°C and wait until it's reached
M190 S50

; Set tool (hotend) temperature to 260°C and wait until it's reached
M109 S50



@CHAMBERWAIT 29  ; Custom command to wait for chamber to reach  desired temp in °C


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