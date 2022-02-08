#!/bin/bash
#
#  pin_check_run.sh -- ccmparison 0 degree image after sample testing
#                       Samuel Clark, 20 November 2020
#
#  Version 1.0 - 20 Nov 2020
full_path="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
if [ -d /GPFS/CENTRAL/xf17id1/skinnerProjectsBackup/pinAlign/pin_align-master ]; then
    export PIN_ALIGN_ROOT=/GPFS/CENTRAL/xf17id1/skinnerProjectsBackup/pinAlign/pin_align-master
fi

fname=$1
fname=${fname##*/}
fbase=${fname%%.*}

. $PIN_ALIGN_ROOT/pin_align_config_fmx.sh
#TODO
#When integrated into LSDC the image_in should be taken when unmounting
# the sample when the rotation = 90 degrees
tmp_dir=$PWD/${USER}_pin_align_$$
mkdir $tmp_dir

convert $1 -contrast  -contrast ${tmp_dir}/$1
convert ${tmp_dir}/$1 -crop $PIN_ALIGN_SECONDARY_PIN_TIP_WINDOW -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 ${tmp_dir}/${fbase}_body.pgm

convert ${tmp_dir}/${fbase}_body.pgm -crop ${TOP_PIN_CROP_WINDOW} ${tmp_dir}/${fbase}_pin_check_top.pgm
convert ${tmp_dir}/${fbase}_body.pgm  -crop ${BOTTOM_PIN_CROP_WINDOW} ${tmp_dir}/${fbase}_pin_check_bottom.pgm

pin_top_compare=$(identify -format %k ${tmp_dir}/${fbase}_pin_check_top.pgm)
pin_bottom_compare=$(identify -format %k ${tmp_dir}/${fbase}_pin_check_bottom.pgm)

if [ $pin_top_compare == 1 ]; then
    pin_check_one=true
fi

if [ $pin_bottom_compare == 1 ]; then
    pin_check_two=true
fi

if [[ "$pin_check_one" = true && "$pin_check_two" = true ]]; then
    echo "PIN PRESENT"
else
    echo "PIN MISSING"
fi

