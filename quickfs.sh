#!/bin/bash

MOUNT_POINT="$HOME/quickfs"
SIZE="8G"

print_usage() {
  echo "Usage: $0 --size [size] --mount-point [mount_point]"
    echo "Options:"
    echo "  --size [size]        Size of the tmpfs (e.g., 8G for 8 GiB)"
    echo "  --mount-point [path] Path to mount the tmpfs (default: $HOME/quickfs)"
    echo "  -h, --help          Show this help message"
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --size)
      SIZE="$2"
      shift 2
      ;;
    --mount-point)
      MOUNT_POINT="$2"
      shift 2
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown parameter passed: $1"
      print_usage
      exit 1
     ;;
  esac
done

# Check if the size is valid
if ! [[ $SIZE =~ ^[0-9]+[KMG]$ ]]; then
  echo "Invalid size format. Please use a valid size (e.g., 8G for 8 GiB)."
  exit 1
fi

# Check if the mount point already exists
if [ ! -d "$MOUNT_POINT" ]; then
  echo "Creating directory $MOUNT_POINT..."
  mkdir -p "$MOUNT_POINT"
fi

# Mount the tmpfs
if mountpoint -q "$MOUNT_POINT"; then
  echo "$MOUNT_POINT is already mounted."
else
  echo "Mounting tmpfs to $MOUNT_POINT with size $SIZE..."
  sudo mount -t tmpfs -o size=$SIZE tmpfs "$MOUNT_POINT"
  echo "tmpfs mounted successfully."
fi

echo "To unmount, use: sudo umount $MOUNT_POINT"
echo "To remove the directory after unmounting, use: rmdir $MOUNT_POINT"
