#!/usr/bin/env bash

if [ "$#" -lt 2 ] || [ ! -f "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo ""
    echo "Tool to create an updated image for the Raspberry Pi."
    echo ""
    echo "The scripts needs the zipfile of a previous release as input."
    echo "The image is extracted, updated and a new zipfile is created"
    echo "with the latest AirOne software"
    echo ""
    echo ""
	echo "usage: $(basename $0) /path/to/base-image.zip /destination/folder/ version"
    echo ""
    echo "e.g. $(basename $0) /my/base-img-v1.0.img.zip /save/here/ 2.0"
	echo ""
	exit 0
fi

ZIPFILE=$1
OUTPUT_DIR=$2
VERSION_NO=$3

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TMP_DIR="$DIR/.tmp_pi_img"
MOUNTPOINT="$TMP_DIR/mounted"



##
## Settings
##

# Absolute path to the repository IN THE RPI IMAGE!
REPO_DIR_IN_IMAGE="/home/pi/HumanInterface"

# Filename of generated image
IMAGE_NAME_PREFIX="airone_v"   



IMAGE_NAME="${IMAGE_NAME_PREFIX}${VERSION_NO}"
mkdir -p "$TMP_DIR"
mkdir -p "$MOUNTPOINT"

echo "Build image version '${VERSION_NO}'"
echo ""
echo "Creating temporary copy..."

unzip -q "$ZIPFILE" -d $TMP_DIR

echo ""
echo "Finding partitions in disk image..."
SRC_FILE="${TMP_DIR}/$(ls "$TMP_DIR" | grep "\.img$")"
IMG_FILE="${TMP_DIR}/${IMAGE_NAME}.img"
mv "$SRC_FILE" "$IMG_FILE" 2>/dev/null

SECTOR_SIZE="$(fdisk -l "$IMG_FILE" | grep "ector size" | sed -e 's/.*\s\([0-9]\+\).\s*bytes$/\1/g')"
SECTOR_OFFSET="$(fdisk -l "$IMG_FILE" | grep inux | awk '{ print $2 }')"
SECTOR_OFFSET_BYTES=$(( $SECTOR_SIZE * $SECTOR_OFFSET ))

is_number='^[0-9]+$'
if ! [[ $SECTOR_OFFSET_BYTES =~ $is_number ]] ; then
   echo "Error: Failed to detect linux partition in image!" >&2;
   exit -1
fi

echo "OK: Linux partition found at offset $SECTOR_OFFSET_BYTES ($SECTOR_OFFSET sectors of $SECTOR_SIZE bytes)"
echo "Mounting image..."
sudo mount "$IMG_FILE" -o loop,offset="$SECTOR_OFFSET_BYTES" "$MOUNTPOINT"

echo ""
echo "Updating image..."
echo "Pulling latest data from git..."
echo "$( cd "${MOUNTPOINT}/${REPO_DIR_IN_IMAGE}" >/dev/null 2>&1 && git pull )"
echo ""

sudo umount "$MOUNTPOINT"
rmdir "$MOUNTPOINT"

echo ""
echo "Image is complete, creating zip..."
NEW_IMG=${OUTPUT_DIR}/${IMAGE_NAME}.img.zip
zip -q -j "$NEW_IMG" "$IMG_FILE"

echo ""
echo "Cleaning up temp files..."
rm "$IMG_FILE"
rmdir "$TMP_DIR"
echo "DONE! New image saved to '$NEW_IMG'"

