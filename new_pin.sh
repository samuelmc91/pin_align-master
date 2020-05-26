#!/bin/sh
IMAGE_ROOT=/home/student/Desktop/Images
if [ -e "/Users/samuel/Desktop/BNL/pin_align-master" ]; then
  export PIN_ALIGN_ROOT=/Users/samuel/Desktop/BNL/pin_align-master
  $PIN_ALIGN_ROOT/pin_align.sh Catalase01_6_8_9_PA_0_001.jpg Catalase01_6_8_9_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Ferritin01_6_11_12_PA_0_001.jpg Ferritin01_6_11_12_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Lys01_6_0_330_PA_0_001.jpg Lys01_6_0_330_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Lys02_6_1_58_PA_0_001.jpg Lys02_6_1_58_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Lys03_6_2_27_PA_0_001.jpg Lys03_6_2_27_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh LysSerial01_6_6_11_PA_0_001.jpg LysSerial01_6_6_11_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh LysSerial02_6_7_11_PA_0_001.jpg LysSerial02_6_7_11_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh LysSingle01_6_3_11_PA_0_001.jpg LysSingle01_6_3_11_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh LysSingle02_6_4_10_PA_0_001.jpg LysSingle02_6_4_10_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh LysSingle03_6_5_11_PA_0_001.jpg LysSingle03_6_5_11_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Thermolysin01_6_10_9_PA_0_001.jpg Thermolysin01_6_10_9_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
  $PIN_ALIGN_ROOT/pin_align.sh Trypsin01_6_9_9_PA_0_001.jpg Trypsin01_6_9_9_PA_90_001.jpg pin.pgm mid.pgm cap.pgm
fi
