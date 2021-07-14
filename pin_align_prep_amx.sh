#!/bin/bash
#
#  pin_align_prep.sh -- prepare a pin alignment image for
#                       comparison between 0 and 90 degree images
#                       H. J. Bernstein, 3 Jan 2019
#                       rev 16 Jan 2019
#
#  Version 2.0 - 15 Jun 2020

if [ "${1}xx" == "--help" ]; then
    echo "pin_align_prep.sh image_in image_out [base_image_out [sub_base_image_out]]"
    echo "        prepare a pin alignment image, image_in, for"
    echo "        comparison between 0 and 90 degree images"
    echo "        writing the resulting image to image_out"
    echo "        assuming a 1280x1024 image and imgagemagick convert"
    echo "        in the PATH"
    echo "	 $2 pin tip, $3 is base, $4 is sub_base"
    exit
fi
. $PIN_ALIGN_ROOT/pin_align_config_amx.sh

# Windows     width x height (px) + horizontal offset + vertical offset from top left corner
convert ${tmp_dir}/$1 -crop $PIN_TIP -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 $2
if [ "${3}xx" != "xx" ]; then
    convert ${tmp_dir}/$1 -crop $PIN_BODY -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 $3
    if [ "${4}xx" != "xx" ]; then
        convert ${tmp_dir}/$1 -crop $PIN_BASE -canny 2x1 -negate -colorspace Gray -morphology Erode Octagon:1 -morphology Dilate Octagon:1 $4
    fi
fi

