########################## Base Parameters ##########################

DEFAULT_PIXELS_PER_MM = 20
PIN_X1_OFFSET = 5

X_POS = True
Y_POS = True
Z_POS = False

X_CENTER = 470
Y_CENTER = 432

########################## pin,body,base ##########################
# slice(offset, offset)
# offset = Y + height
DEFAULT_ROI_Y1 = 320
DEFAULT_ROI_Y2 = 544

DEFAULT_HEIGHT = 225

# Pin tip
# offset = X + width
PIN_TIP_X1 = 425
PIN_TIP_X2 = 534

PIN_TIP = slice(PIN_TIP_X1, PIN_TIP_X2)

# Pin body
PIN_BODY_X1 = 534
PIN_BODY_X2 = 643

PIN_BODY = slice(PIN_BODY_X1, PIN_BODY_X2)

# Pin base
PIN_BASE_X1 = 643
PIN_BASE_X2 = 752

PIN_BASE = slice(PIN_BASE_X1, PIN_BASE_X2)

########################## Tilt check  parameters ##########################
# Setting the width = -10 the width of the image
TILT_CHECK_X1 = 702
TILT_CHECK_X2 = 752

TILT_CHECK_ROI_WIDTH = slice(TILT_CHECK_X1, TILT_CHECK_X2)

# Top crop
TILT_CHECK_TOP_Y1 = 335
TILT_CHECK_TOP_Y2 = 382

TILT_CHECK_TOP = slice(TILT_CHECK_TOP_Y1, TILT_CHECK_TOP_Y2)

# Bottom crop
TILT_CHECK_BOTTOM_Y1 = 482
TILT_CHECK_BOTTOM_Y2 = 529

TILT_CHECK_BOTTOM = slice(TILT_CHECK_BOTTOM_Y1, TILT_CHECK_BOTTOM_Y2)

########################## Pin check parameters ##########################

# Top crop
PIN_CHECK_TOP_Y1 = 320
PIN_CHECK_TOP_Y2 = 382

PIN_CHECK_TOP = slice(PIN_CHECK_TOP_Y1, PIN_CHECK_TOP_Y2)

# Bottom crop
PIN_CHECK_BOTTOM_Y1 = 482
PIN_CHECK_BOTTOM_Y2 = 544

PIN_CHECK_BOTTOM = slice(PIN_CHECK_BOTTOM_Y1, PIN_CHECK_BOTTOM_Y2)

DEFAULT_WIDTH = 327

########################## X,Y,Z check parameters ##########################
MIN_X = -2
MAX_X = 2

MIN_Y = -2
MAX_Y = 2

MIN_Z = -2
MAX_Z = 2

########################## Small & Big Box parameters ##########################
BOX_X_IN = 470
BOX_Y_IN = 432

SMALL_BOX_X1 = BOX_X_IN + (MIN_Z * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_X2 = BOX_X_IN + (MAX_Z * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_WIDTH = slice(SMALL_BOX_X1, SMALL_BOX_X2)

SMALL_BOX_Y1 = BOX_Y_IN + (MIN_Y * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_Y2 = BOX_Y_IN + (MAX_Y * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_HEIGHT = slice(SMALL_BOX_Y1, SMALL_BOX_Y2)

BIG_BOX_X1 = 425
BIG_BOX_X2 = 752

BIG_BOX_WIDTH = slice(BIG_BOX_X1, BIG_BOX_X2)

BIG_BOX_Y1 = 320
BIG_BOX_Y2 = 544

BIG_BOX_HEIGHT = slice(BIG_BOX_Y1, BIG_BOX_Y2)

########################## ROI W/H parameters ##########################
INPUT_ROI_WIDTH = 466
INPUT_ROI_HEIGHT = 256
