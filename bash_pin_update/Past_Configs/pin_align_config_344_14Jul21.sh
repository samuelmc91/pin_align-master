#/bin/bash

###########################################################

DEFAULT_PIXELS_PER_MM=$((20))

export X_POS=1
export Y_POS
export Z_POS=1

X_CENTER=$((409))

Y_CENTER=$((487))

#########################################################

BIG_BOX_X1=$((369))
BIG_BOX_X2=$((664))

BIG_BOX_Y1=$((362))
BIG_BOX_Y2=$((612))

PIN_ALIGN_ROI_WIDTH=$(((${BIG_BOX_X2}-${BIG_BOX_X1}) / 3))
PIN_ALIGN_ROI_HEIGHT=$((${BIG_BOX_Y2}-${BIG_BOX_Y1}))

########################## pin,body,base ##########################

DEFAULT_ROI_Y1=$((362))

PIN_TIP_X1=$((369))

PIN_TIP="${PIN_ALIGN_ROI_WIDTH}x${PIN_ALIGN_ROI_HEIGHT}+${PIN_TIP_X1}+${DEFAULT_ROI_Y1}"

PIN_BODY_X1=$((467))

PIN_BODY="${PIN_ALIGN_ROI_WIDTH}x${PIN_ALIGN_ROI_HEIGHT}+${PIN_BODY_X1}+${DEFAULT_ROI_Y1}"

PIN_BASE_X1=$((565))

PIN_BASE="${PIN_ALIGN_ROI_WIDTH}x${PIN_ALIGN_ROI_HEIGHT}+${PIN_BASE_X1}+${DEFAULT_ROI_Y1}"

########################## Tilt check  parameters ##########################

TILT_CHECK_X1=$((614))
TILT_CHECK_X2=$((664))

TILT_CHECK_ROI_WIDTH=$((${TILT_CHECK_X2}-${TILT_CHECK_X1}))

# Tilt check top
TILT_CHECK_TOP_Y1=$((382))
TILT_CHECK_TOP_Y2=$((452))

TILT_CHECK_TOP_HEIGHT=$((${TILT_CHECK_TOP_Y2}-${TILT_CHECK_TOP_Y1}))

TILT_CHECK_TOP="${TILT_CHECK_ROI_WIDTH}x${TILT_CHECK_TOP_HEIGHT}+${TILT_CHECK_X1}+${TILT_CHECK_TOP_Y1}"

# Tilt check bottom
TILT_CHECK_BOTTOM_Y1=$((522))
TILT_CHECK_BOTTOM_Y2=$((592))

TILT_CHECK_BOTTOM_HEIGHT=$((${TILT_CHECK_BOTTOM_Y2}-${TILT_CHECK_BOTTOM_Y1}))

TILT_CHECK_BOTTOM="${TILT_CHECK_ROI_WIDTH}x${TILT_CHECK_TOP_HEIGHT}+${TILT_CHECK_X1}+${TILT_CHECK_BOTTOM_Y1}"

########################## Pin check parameters ##########################

PIN_CHECK_ROI_WIDTH=${PIN_ALIGN_ROI_WIDTH}

PIN_CHECK_X1=${PIN_BODY_X1}

PIN_CHECK_TOP_Y1=$((362))
PIN_CHECK_TOP_Y2=$((452))

PIN_CHECK_TOP_HEIGHT=$((${PIN_CHECK_TOP_Y2}-${PIN_CHECK_TOP_Y1}))

PIN_CHECK_TOP="${PIN_CHECK_ROI_WIDTH}x${PIN_CHECK_TOP_HEIGHT}+${PIN_CHECK_X1}+${PIN_CHECK_TOP_Y1}"

PIN_CHECK_BOTTOM_Y1=$((522))
PIN_CHECK_BOTTOM_Y2=$((612))

PIN_CHECK_BOTTOM_HEIGHT=$((${PIN_CHECK_BOTTOM_Y2}-${PIN_CHECK_BOTTOM_Y1}))

PIN_CHECK_BOTTOM="${PIN_CHECK_ROI_WIDTH}x${PIN_CHECK_TOP_HEIGHT}+${PIN_CHECK_X1}+${PIN_CHECK_BOTTOM_Y1}"

########################## X,Y,Z check parameters ##########################
MIN_X=$((-2))
MAX_X=$((2))

MIN_Y=$((-2))
MAX_Y=$((2))

MIN_Z=$((-2))
MAX_Z=$((2))

##############################################################
#  *** UNCOMMENT THE FOLLOWING LINE TO ENABLE DEBUG MODE ***
# export PIN_ALIGN_DEBUG="yes"
##############################################################

# if [ "xx${PIN_ALIGN_DEBUG}" != "xx" ]; then
#     echo "PIN_ALIGN: DEBUG enabled" 1>&2
# fi
# if [ "xx${PIN_ALIGN_DEBUG}" == "xx" ]; then
#     echo "PIN_ALIGN: DEBUG disabled" 1>&2
# fi

# if [ "xx${PIN_ALIGN_DEBUG}" != "xx" ]; then
#     if [ "xx${PIN_ALIGN_ROI_WIDTH}" != "xx" ]; then
#         echo "PIN_ALIGN_ROI_WIDTH: $PIN_ALIGN_ROI_WIDTH" 1>&2
#     fi
#     if [ "xx${PIN_ALIGN_ROI_HEIGHT}" != "xx" ]; then
#         echo "PIN_ALIGN_ROI_HEIGHT: $PIN_ALIGN_ROI_HEIGHT" 1>&2
#     fi
#     if [ "xx${X_CENTER}" == "xx" ]; then
#         echo "X_CENTER: $X_CENTER" 1>&2
#     fi
#     if [ "xx${Y_CENTER}" == "xx" ]; then
#         echo "Y_CENTER: $Y_CENTER" 1>&2
#     fi
# fi