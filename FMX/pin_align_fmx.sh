#!/bin/bash
#  Auto Config
#  pin_align.sh -- ccmparison 0 and 90 degree images
#                       H. J. Bernstein, 3 Jan 2019
#
#  Version 2.0 - 15 Jun 2020
full_path="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
export PIN_ALIGN_ROOT=`dirname "$full_path" | sed 's/\/bin$//'`
#echo full_path=\"$full_path\"
# if [ -d /home/samuel/Desktop/Projects/FMX/pin_align-master ]; then
#    export PIN_ALIGN_ROOT=/home/samuel/Desktop/Projects/FMX/pin_align-master
# fi
. $PIN_ALIGN_ROOT/pin_align_config_fmx.sh
if [ "xx${PIN_ALIGN_DEBUG}" != "xx" ]; then
    echo PIN_ALIGN_ROOT=\"$PIN_ALIGN_ROOT\"
    echo "argument 0: ${0}" 1>&2
    echo "argument 1: ${1}" 1>&2
    echo "argument 2: ${2}" 1>&2
fi

if [ "${1}xx" == "--helpxx" ]; then
    echo "pin_align.sh image_0 image_90 image_out image_base_out image_sub_base_out [tilt_limit]"
    echo "        compare 0 and 90 degree images"
    echo "        writing the resulting pin tip image to image_out"
    echo "        writing the resulting pin base image to image_base_out"
    echo "        writing the resulting pin base cap image to image_sub_base_out"
    echo "        assuming  1280x1024 images"
    echo "        imagemagick convert called as convert"
    echo "        imagemagick compare called as compare"
    echo "        assuming a center at 515 460"
    echo "        assuming 325x400+${BIG_BOX_X1}+${BIG_BOX_Y1} ROI"
    echo "        and $PIN_ALIGN_ROOT containing pin_align_prep.sh, etc"
    echo "        tilt_limit is a limit on the image height in pixels"
    echo "        default 50 "
    echo " "
    echo "        export Y_POS=1; if Y motor axis is up"
    echo "        export PIN_ALIGN_Z_UP=1; if Z motor axis is up"
    echo " "
    exit
fi

fuzz="9% -threshold 50%"
fname=$1
fname=${fname##*/}
fbase=${fname%%.*}

roi_width=$(( $PIN_ALIGN_ROI_WIDTH ))
roi_height=$(( $PIN_ALIGN_ROI_HEIGHT ))
roi_width_offset=$(( $BIG_BOX_X1 ))
roi_height_offset=$(( $BIG_BOX_Y1 ))
image_center_width=$(( $X_CENTER - $roi_width_offset ))
image_center_height=$(( $Y_CENTER - $roi_height_offset ))

scaled_px_per_mm=`echo "scale=2;  5 * ${DEFAULT_PIXELS_PER_MM} "| bc -l`

tmp_dir=$PWD/${USER}_pin_align_$$
mkdir $tmp_dir
echo Processing pin images
echo "0 degree: " $1
echo "90 degrees; " $2
echo "Files in: " $tmp_dir

#  Assume images have the origin top left, with image_width increasing left to right
#  image_height increasing top to bottom
#  Assume 0 degree image has  motor-x horizontal increasing right to left
#                             i.e. opposite to image_width
#                             motor-z vertical increasing bottom to top
#                             i.e. opposite to image_height
#  Assume 90 degree image has motor-x horizontal increasing right to left
#                             i.e. opposite to image_width
#                             motor-y vertical increasing top to bottom
#                             i.e. with image_height
#                             unless environment variable Y_POS is not empty

convert $1 -contrast  -contrast ${tmp_dir}/$1
convert $2 -contrast  -contrast ${tmp_dir}/$2

XZ=${tmp_dir}/$1
XY=${tmp_dir}/$2

# Names ending in _1.pgm are 0 degrees, names ending in _2.pgm are 90 degrees and
# names ending in _3.pgm are combined 0 and 90 degrees
$PIN_ALIGN_ROOT/pin_align_prep_fmx.sh $XZ ${tmp_dir}/${fbase}_1_pin.pgm \
${tmp_dir}/${fbase}_1_body.pgm ${tmp_dir}/${fbase}_1_base.pgm> ${tmp_dir}/${fbase}_1.mvg
$PIN_ALIGN_ROOT/pin_align_prep_fmx.sh $XY ${tmp_dir}/${fbase}_2_pin.pgm \
${tmp_dir}/${fbase}_2_body.pgm ${tmp_dir}/${fbase}_2_base.pgm> ${tmp_dir}/${fbase}_2.mvg

#Combine both the top and bottom ROIs into one ROI
compare ${tmp_dir}/${fbase}_1_pin.pgm ${tmp_dir}/${fbase}_2_pin.pgm ${tmp_dir}/${fbase}_3_pin.pgm
compare ${tmp_dir}/${fbase}_1_body.pgm ${tmp_dir}/${fbase}_2_body.pgm ${tmp_dir}/${fbase}_3_body.pgm
compare ${tmp_dir}/${fbase}_1_base.pgm ${tmp_dir}/${fbase}_2_base.pgm ${tmp_dir}/${fbase}_3_base.pgm

#Crop the ROI down to two appropriate size ROIs --Sam
nooutput=0

convert ${tmp_dir}/${fbase}_3_base.pgm -crop ${TILT_CHECK_TOP} ${tmp_dir}/${fbase}_3_tilt_check_top.pgm
convert ${tmp_dir}/${fbase}_3_base.pgm -crop ${TILT_CHECK_BOTTOM} ${tmp_dir}/${fbase}_3_tilt_check_bottom.pgm


#Test to see if there is more than one color present in the ROI
#If the pin is not tilted the entire ROI should be white

top_compare=$(identify -format %k ${tmp_dir}/${fbase}_3_tilt_check_top.pgm)
bottom_compare=$(identify -format %k ${tmp_dir}/${fbase}_3_tilt_check_bottom.pgm)

if [ $top_compare == 1 ]; then
    check_one=true
fi

if [ $bottom_compare == 1 ]; then
    check_two=true
fi

if [[ "$check_one" = true && "$check_two" = true ]]; then
    echo "CAP CENTERED"
else
    echo "CAP TILTED"
    nooutput=1
fi

#The check to see if a pin is present or missing
convert ${tmp_dir}/${fbase}_3_body.pgm -crop ${PIN_CHECK_TOP} ${tmp_dir}/${fbase}_3_pin_check_top.pgm
convert ${tmp_dir}/${fbase}_3_body.pgm  -crop ${PIN_CHECK_BOTTOM} ${tmp_dir}/${fbase}_3_pin_check_bottom.pgm

pin_top_compare=$(identify -format %k ${tmp_dir}/${fbase}_3_pin_check_top.pgm)
pin_bottom_compare=$(identify -format %k ${tmp_dir}/${fbase}_3_pin_check_bottom.pgm)

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
    nooutput=1
fi
#End

########## fuzz factor #############
convert  ${tmp_dir}/${fbase}_1_pin.pgm -fuzz $fuzz -trim info:- > ${tmp_dir}/info_image_1
convert  ${tmp_dir}/${fbase}_2_pin.pgm -fuzz $fuzz -trim info:- > ${tmp_dir}/info_image_2
convert ${tmp_dir}/${fbase}_3_pin.pgm  -fuzz $fuzz -trim info:- > ${tmp_dir}/info_image_compare_3
convert ${tmp_dir}/${fbase}_3_base.pgm -fuzz $fuzz -trim info:- > ${tmp_dir}/info_image_compare_3_base

$PIN_ALIGN_ROOT/pin_align_split_info.sh ${tmp_dir}/info_image_1 > ${tmp_dir}/info_image_1.vars
. ${tmp_dir}/info_image_1.vars
image_half_height_z=$(( $info_active_image_height / 2 ))
image_pin_x1_orig=$(( $info_raw_image_width_offset + $roi_width_offset ))
image_pin_x1_offset_to_cent=$(( $image_center_width - $info_raw_image_width_offset ))
image_pin_x1_offset_to_cent=$(( $image_pin_x1_offset_to_cent * 5 ))
image_pin_x1_offset_to_cent=`echo "scale=2; -1* $image_pin_x1_offset_to_cent / ${scaled_px_per_mm}"| bc -l`
x1_clip=$(( ${info_raw_image_width_offset} + ${BIG_BOX_X1} ))

image_pin_z=$(( $info_raw_image_height_offset + $image_half_height_z ))
image_pin_z_orig=$(( $image_pin_z + $roi_height_offset ))
image_pin_z_offset_to_cent=$(( $image_center_height - $image_pin_z  ))
image_pin_z_offset_to_cent=$(( $image_pin_z_offset_to_cent * 5 ))
if [ "xx${Z_POS}" != "xx" ]; then
    image_pin_z_offset_to_cent=`echo "scale=2; $image_pin_z_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
else
    image_pin_z_offset_to_cent=`echo "scale=2; -1* $image_pin_z_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
fi


################### fuzz factor #################
convert $1 -crop "10x${PIN_ALIGN_ROI_HEIGHT}+${x1_clip}+${BIG_BOX_Y1}" -contrast -contrast -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 ${tmp_dir}/${fbase}_1_left.pgm
convert ${tmp_dir}/${fbase}_1_left.pgm -fuzz $fuzz -trim info:- > ${tmp_dir}/${fbase}_1_left.pgm.info

$PIN_ALIGN_ROOT/pin_align_split_info.sh ${tmp_dir}/${fbase}_1_left.pgm.info > ${tmp_dir}/info_image_1_left.vars
. ${tmp_dir}/info_image_1_left.vars


image_half_height_z2=$(( $info_active_image_height / 2 ))
image_pin_z2=$(( $info_raw_image_height_offset + $image_half_height_z2 ))
image_pin_z2_orig=$(( $image_pin_z2 + $roi_height_offset ))
image_pin_z2_offset_to_cent=$(( $image_center_height - $image_pin_z2  ))
image_pin_z2_offset_to_cent=$(( $image_pin_z2_offset_to_cent * 5 ))

if [ "xx${Z_POS}" != "xx" ]; then
    image_pin_z2_offset_to_cent=`echo "scale=2; $image_pin_z2_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
else
    image_pin_z2_offset_to_cent=`echo "scale=2; -1*  $image_pin_z2_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
fi

$PIN_ALIGN_ROOT/pin_align_split_info.sh ${tmp_dir}/info_image_2 > ${tmp_dir}/info_image_2.vars
. ${tmp_dir}/info_image_2.vars
image_half_height_y=$(( $info_active_image_height / 2 ))
image_pin_x2_orig=$(( $info_raw_image_width_offset + $roi_width_offset ))
image_pin_x2_offset_to_cent=$(( $image_center_width - $info_raw_image_width_offset ))
image_pin_x2_offset_to_cent=$(( $image_pin_x2_offset_to_cent * 5 ))
image_pin_x2_offset_to_cent=`echo "scale=2; -1* $image_pin_x2_offset_to_cent / ${scaled_px_per_mm}"| bc -l`
x2_clip=$(( ${info_raw_image_width_offset} + ${BIG_BOX_X1} ))

image_pin_y=$(( $info_raw_image_height_offset + $image_half_height_y ))
image_pin_y_orig=$(( $image_pin_y + $roi_height_offset ))
image_pin_y_offset_to_cent=$(( $image_center_height - $image_pin_y  ))
image_pin_y_offset_to_cent=$(( $image_pin_y_offset_to_cent * 5 ))
if [ "xx${Y_POS}" != "xx" ]; then
    image_pin_y_offset_to_cent=`echo "scale=2; $image_pin_y_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
else
    image_pin_y_offset_to_cent=`echo "scale=2; - $image_pin_y_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
fi


########################### fuzz factor ########################
convert $2 -crop "10x${PIN_ALIGN_ROI_HEIGHT}+${x2_clip}+${BIG_BOX_Y1}"  -contrast -contrast -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 ${tmp_dir}/${fbase}_2_left.pgm
convert ${tmp_dir}/${fbase}_2_left.pgm -fuzz $fuzz -trim info:- > ${tmp_dir}/${fbase}_2_left.pgm.info


$PIN_ALIGN_ROOT/pin_align_split_info.sh ${tmp_dir}/${fbase}_2_left.pgm.info > ${tmp_dir}/info_image_2_left.vars
. ${tmp_dir}/info_image_2_left.vars

image_half_height_y2=$(( $info_active_image_height / 2 ))
image_pin_y2=$(( $info_raw_image_height_offset + $image_half_height_y2 ))
image_pin_y2_orig=$(( $image_pin_y2 + $roi_height_offset ))
image_pin_y2_offset_to_cent=$(( $image_center_height - $image_pin_y2  ))
image_pin_y2_offset_to_cent=$(( $image_pin_y2_offset_to_cent * 5 ))
if [ "xx${Y_POS}" != "xx" ]; then
    image_pin_y2_offset_to_cent=`echo "scale=2; $image_pin_y2_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
else
    image_pin_y2_offset_to_cent=`echo "scale=2; - $image_pin_y2_offset_to_cent / ${scaled_px_per_mm}"|bc -l`
fi
$PIN_ALIGN_ROOT/pin_align_split_info.sh ${tmp_dir}/info_image_compare_3 > ${tmp_dir}/info_image_compare_3.vars
. ${tmp_dir}/info_image_compare_3.vars

if (( $(echo "${image_pin_x1_offset_to_cent} < $MAX_X" | bc -l)  )) && (( $(echo "${image_pin_x1_offset_to_cent} > $MIN_X" | bc -l)  )); then
    x1_check=true
fi

if (( $(echo "${image_pin_x2_offset_to_cent} < $MAX_X" | bc -l)  )) && (( $(echo "${image_pin_x2_offset_to_cent} > $MIN_X" | bc -l)  )); then
    x2_check=true
fi

if (( $(echo "${image_pin_y2_offset_to_cent} < $MAX_Y" | bc -l)  )) && (( $(echo "${image_pin_y2_offset_to_cent} > $MIN_Y" | bc -l)  )); then
    y_check=true
fi

if (( $(echo "${image_pin_z2_offset_to_cent} < $MAX_Z" | bc -l)  )) && (( $(echo "${image_pin_z2_offset_to_cent} > $MIN_Z" | bc -l)  )); then
    z_check=true
fi

if [[ "$x1_check" = true && "$x2_check" = true && "$y_check" = true && "$z_check" == true ]]; then
    echo "X, Y, Z WITHIN LIMITS"
else
    echo "PIN CANNOT BE CENTERED TRY MANUAL CENTERING"
    echo "X, Y, Z VIOLATION"
    nooutput=1
fi
#End


if [ "xx${nooutput}" == "xx0" ]; then
    if (( $(echo "${image_pin_x1_orig} < ${image_pin_x2_orig}" | bc -l)  )); then
        image_pin_x_orig=${image_pin_x1_orig}
        image_pin_x_offset_to_cent=${image_pin_x1_offset_to_cent}
    else
        image_pin_x_orig=${image_pin_x2_orig}
        image_pin_x_offset_to_cent=${image_pin_x2_offset_to_cent}
    fi
    echo "OMEGA 0  X,-,Z PIN POS IMAGE2 PX"  [${image_pin_x1_orig}, - , ${image_pin_z2_orig} ]; # adding omega values
    echo "OMEGA 90 X,Y,- PIN POS IMAGE1 PX"  [${image_pin_x2_orig}, ${image_pin_y2_orig}, - ];  # adding omega values
    echo "OVERALL  X,Y,Z PIN POS        PX"  [${image_pin_x_orig}, ${image_pin_y2_orig}, ${image_pin_z2_orig} ]; # move to better align
    
    echo "OMEGA 0  X,-,Z OFFSETS TO CENTER IMAGE2 mm"   [${image_pin_x1_offset_to_cent}, - , ${image_pin_z2_offset_to_cent} ]
    echo "OMEGA 90 X,Y,- OFFSETS TO CENTER IMAGE1 mm"   [${image_pin_x2_offset_to_cent}, ${image_pin_y2_offset_to_cent}, - ]; # change order to be below XZ plane for better visual
    echo "OVERALL X,Y,Z OFFSETS TO CENTER         mm"   [${image_pin_x_offset_to_cent}, ${image_pin_y2_offset_to_cent}, ${image_pin_z2_offset_to_cent} ]; # move to better align
    
fi
if [ "xx$PIN_ALIGN_DEBUG" != "xx" ]; then
    rm -rf ${tmp_dir}
fi
