########################## Base Parameters ##########################

DEFAULT_PIXELS_PER_MM = 20
PIN_X1_OFFSET = 25

X_POS = True
Y_POS = True
Z_POS = False

X_CENTER = 402
Y_CENTER = 484

########################## pin,body,base ##########################
# slice(offset, offset)
# offset = Y + height
DEFAULT_ROI_Y1 = 372
DEFAULT_ROI_Y2 = 596

DEFAULT_HEIGHT = 225

# Pin tip
# offset = X + width
PIN_TIP_X1 = 377
PIN_TIP_X2 = 475

PIN_TIP = slice(PIN_TIP_X1, PIN_TIP_X2)

# Pin body
PIN_BODY_X1 = 475
PIN_BODY_X2 = 573

PIN_BODY = slice(PIN_BODY_X1, PIN_BODY_X2)

# Pin base
PIN_BASE_X1 = 573
PIN_BASE_X2 = 671

PIN_BASE = slice(PIN_BASE_X1, PIN_BASE_X2)

########################## Tilt check  parameters ##########################
# Setting the width = -10 the width of the image
TILT_CHECK_X1 = 621
TILT_CHECK_X2 = 671

TILT_CHECK_ROI_WIDTH = slice(TILT_CHECK_X1, TILT_CHECK_X2)

# Top crop
TILT_CHECK_TOP_Y1 = 387
TILT_CHECK_TOP_Y2 = 434

TILT_CHECK_TOP = slice(TILT_CHECK_TOP_Y1, TILT_CHECK_TOP_Y2)

# Bottom crop
TILT_CHECK_BOTTOM_Y1 = 534
TILT_CHECK_BOTTOM_Y2 = 581

TILT_CHECK_BOTTOM = slice(TILT_CHECK_BOTTOM_Y1, TILT_CHECK_BOTTOM_Y2)

########################## Pin check parameters ##########################

# Top crop
PIN_CHECK_TOP_Y1 = 372
PIN_CHECK_TOP_Y2 = 434

PIN_CHECK_TOP = slice(PIN_CHECK_TOP_Y1, PIN_CHECK_TOP_Y2)

# Bottom crop
PIN_CHECK_BOTTOM_Y1 = 534
PIN_CHECK_BOTTOM_Y2 = 596

PIN_CHECK_BOTTOM = slice(PIN_CHECK_BOTTOM_Y1, PIN_CHECK_BOTTOM_Y2)

DEFAULT_WIDTH = 294

########################## X,Y,Z check parameters ##########################
MIN_X = -2
MAX_X = 2

MIN_Y = -2
MAX_Y = 2

MIN_Z = -2
MAX_Z = 2

########################## Small & Big Box parameters ##########################
BOX_X_IN = 402
BOX_Y_IN = 484

SMALL_BOX_X1 = BOX_X_IN + (MIN_Z * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_X2 = BOX_X_IN + (MAX_Z * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_WIDTH = slice(SMALL_BOX_X1, SMALL_BOX_X2)

SMALL_BOX_Y1 = BOX_Y_IN + (MIN_Y * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_Y2 = BOX_Y_IN + (MAX_Y * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_HEIGHT = slice(SMALL_BOX_Y1, SMALL_BOX_Y2)

BIG_BOX_X1 = 377
BIG_BOX_X2 = 671

BIG_BOX_WIDTH = slice(BIG_BOX_X1, BIG_BOX_X2)

BIG_BOX_Y1 = 372
BIG_BOX_Y2 = 596

BIG_BOX_HEIGHT = slice(BIG_BOX_Y1, BIG_BOX_Y2)

########################## ROI W/H parameters ##########################
INPUT_ROI_WIDTH = 466
INPUT_ROI_HEIGHT = 256
