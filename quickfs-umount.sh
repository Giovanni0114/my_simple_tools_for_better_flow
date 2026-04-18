#!/bin/bash

MOUNT_POINT="$HOME/quickfs"

print_usage() {
    echo "Usage: $0 --mount-point [mount_point]"
    echo "Options:"
    echo "  --mount-point [path] Path of the tmpfs to be unmounted (default: $HOME/quickfs)"
    echo "  -h, --help          Show this help message"
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
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

# umount the tmpfs
if mountpoint -q "$MOUNT_POINT"; then
    echo "Unmounting tmpfs on $MOUNT_POINT"
    sudo umount "$MOUNT_POINT"
    rm -rf "$MOUNT_POINT"
    echo "Unmounted and removed $MOUNT_POINT"
    exit 0
fi

echo "$MOUNT_POINT is not mounted."
if [ -d "$MOUNT_POINT" ]; then
    rm -rf "$MOUNT_POINT"
    echo "$MOUNT_POINT removed."
fi
