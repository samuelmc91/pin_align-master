#!/bin/sh
IMAGE_ROOT=/home/student/Desktop/Images
if [ -e "/Users/samuel/Desktop/BNL/pin_align-master" ]; then
  export PIN_ALIGN_ROOT=/Users/samuel/Desktop/BNL/pin_align-master
  $PIN_ALIGN_ROOT/pin_align.sh AntR18_8_0_7_0_PA_0_001.jpg AntR18_8_0_7_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh AntR18_9_0_8_0_PA_0_001.jpg AntR18_9_0_8_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh AntR7_8_10_7_0_PA_0_001.jpg AntR7_8_10_7_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Cav1_4_2_3_0_PA_0_001.jpg Cav1_4_2_3_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Horse-Syn_1_2_4_0_PA_0_001.jpg Horse-Syn_1_2_4_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Horse-Syn_4_2_7_0_PA_0_001.jpg Horse-Syn_4_2_7_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Izumo1_1_4_11_0_PA_0_001.jpg Izumo1_1_4_11_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Izumo1_2_4_12_0_PA_0_001.jpg Izumo1_2_4_12_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Mab1_6_2_13_0_PA_0_001.jpg Mab1_6_2_13_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Mab1_7_2_14_0_PA_0_001.jpg Mab1_7_2_14_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Pig-Syn_8_4_14_0_PA_0_001.jpg Pig-Syn_8_4_14_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Pig-Syn_9_4_15_0_PA_0_001.jpg Pig-Syn_9_4_15_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh T74D_6_1_5_0_PA_0_001.jpg T74D_6_1_5_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh T74D_7_1_6_0_PA_0_001.jpg T74D_7_1_6_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh T74D_8_1_7_0_PA_0_001.jpg T74D_8_1_7_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh T74D_9_1_8_0_PA_0_001.jpg T74D_9_1_8_0_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh oemga0_tilted_AMX_005.jpg oemga90_tilted_AMX_005.jpg pin.pgm mid.pgm cap.pgm
fi
