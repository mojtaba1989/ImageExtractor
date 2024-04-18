#!/bin/sh

NC='\033[0m'       # Text Reset
R='\033[0;31m'          # Red
G='\033[0;32m'        # Green
Y='\033[0;33m'       # Yellow
B='\033[0;34m'         # Blue
P='\033[0;35m'       # Purple
C='\033[0;36m'         # Cyan
W='\033[0;37m'        # White

INFO() {
   # Display Help
   echo "APSRC Image Extracting Tool: MOJTABA BAHRAMGIRI, APSRC - Jan 2024"
   echo "---------------------------------------------------------------"
   echo "Description:"
   echo "  This tool extracts images from selected topics in a ROSBAG file."
   echo ""
   echo "Source Code Compatibility:"
   echo "  - ROS Melodic"
   echo "  - Python 2.7"
   echo ""
   echo "Requirements:"
   echo "  - No additional package installation is required."
   echo ""
   echo "Open Source:"
   echo "  - The source code is open access and can be used in whole or in part."
   echo "---------------------------------------------------------------"
}

SHORTCUT() {
   shortcut="/home/$USER/Desktop/ImageExtractor.desktop"
   echo "[Desktop Entry]" > $shortcut
   echo Name=Rosbag Image Extract Tool >> $shortcut
   echo Exec=$PWD/installed/image_extractor_app.dist/image_extractor_app.bin >> $shortcut
   echo Terminal=true >> $shortcut
   echo Type=Application >> $shortcut
   echo Icon=$PWD/icon.png >> $shortcut
   sudo chmod +x /home/$USER/Desktop/ImageExtractor.desktop
   echo "${G}[OK] Shortcut added to desktop${NC}"
}

INFO

target_dir="./installed"
log_file=".log"
exec 3<> $log_file
runfile="ImageExtractor.desktop"

if [ -d $target_dir ]; then
   while true; do
      read -p "[Warning] Old installation found! Wish to reinstall?(y/n)" yn
      case $yn in
         [Yy]* ) sudo rm -r $target_dir; break ;;
         [Nn]* ) return 1;;
         * ) return 1;;
      esac
   done
else
   mkdir ./installed
   echo "${G}[OK] Directories Created${NC}"
fi

echo "${Y}[Info] Unpacking source files${NC}"
unzip ./image_extractor_app..zip -d $target_dir 1>/dev/null 2>&3
if [ $? -ne 0 ]; then echo "${R}[Error] Zip file corrupted!${NC}"; return 1; fi
echo "${G}[Ok] Zip file unpacked!${NC}"

echo "[Desktop Entry]" > $runfile
echo Name=Rosbag Image Extract Tool >> $runfile
echo Exec=$PWD/installed/image_extractor_app.dist/image_extractor_app.bin >> $runfile
echo Terminal=true >> $runfile
echo Type=Application >> $runfile
echo Icon=$PWD/icon.png >> $runfile
sudo chmod +x $runfile

echo "${G}[Ok] Run file added!${NC}"
while true; do
   read -p "Add shortcut to desktop?(y/n)" yn
   case $yn in
      [Yy]* ) SHORTCUT; break;;
      [Nn]* ) break;;
      * ) break;;
   esac
done

echo "${G}[OK] Installation Completed${NC}"
unset INFO
unset SHORTCUT






