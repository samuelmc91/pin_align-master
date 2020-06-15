#!/bin/bash
# pin_align_split_info
# convert an ImgMagick info string in $1 to a set of variable
# assignments in stdout
#     info_file_name=
#     info_file_type=
#     info_active_image_width=
#     info_active_image_height=
#     info_raw_image_width_offset=
#     info_raw_image_height_offset=
#echo $1
#
#  Version 2.0 - 15 Jun 2020

if [ -e "$1" ]; then
  info=`cat $1`
else
  info=$1;
fi
IFS=' '; read -r -a info_array <<< "$info"
#echo "${info_array[0]}" "${info_array[1]}" "${info_array[2]}" "${info_array[3]}" "${info_array[4]}" "${info_array[5]}"
if [ "${info_array[0]}xx" == "xx" ]; then
  echo info_file_name="unknown"
else
  echo info_file_name="${info_array[0]}"
fi
if [ "${info_array[1]}xx" == "xx" ]; then
  echo info_file_type="unknown"
else
  echo info_file_type="${info_array[1]}"
fi
IFS="0123456789"; read -r -a active_sep <<< "${info_array[2]}"; 
IFS=' '; read -r -a active_sep_sep <<< "${active_sep[@]}"; #echo raw_sep_sep="${raw_sep_sep[@]}"
IFS='x+- ';read -r -a active <<< "${info_array[2]}"; #echo active="${active[@]}"
if [ "${active[0]}xx" == "xx" ]; then
  echo info_active_image_width="-1"
else
  echo info_active_image_width="${active[0]}"
fi
if [ "${active[1]}xx" == "xx" ]; then
  echo info_active_image_height="-1"
else
  echo info_active_image_height="${active[1]}"
fi
IFS=' 0123456789'; read -r -a raw_sep <<< "${info_array[3]}";
IFS=' '; read -r -a raw_sep_sep <<< "${raw_sep[@]}"; #echo raw_sep_sep="${raw_sep_sep[@]}"
IFS='x+- '; read -r -a raw <<< "${info_array[3]}"; #echo "${raw[@]}"
if [ "${raw[0]}xx" == "xx" ]; then
  echo info_raw_image_width="-1"
else
  echo info_raw_image_width="${raw[0]}"
fi
if [ "${raw[1]}xx" == "xx" ]; then
  echo info_raw_image_height="-1"
else
  echo info_raw_image_height="${raw[1]}"
fi
if [ "${raw[2]}xx" == "xx" ]; then
  echo info_raw_image_width_offset="-1"
else
  echo info_raw_image_width_offset="${raw_sep_sep[1]}""${raw[2]}"
fi
if [ "${raw[3]}xx" == "xx" ]; then
  echo info_raw_image_height_offset="-1"
else
  echo info_raw_image_height_offset="${raw_sep_sep[2]}""${raw[3]}"
fi
