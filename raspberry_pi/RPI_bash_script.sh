

cd /sys/kernel/config/usb_gadget/
mkdir -p pi_hid
cd pi_hid

echo 0x258A > idVendor 
echo 0x2023 > idProduct 

echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB


mkdir -p strings/0x409
echo "CH12128210102684" > strings/0x409/serialnumber 
echo "PixArt" > strings/0x409/manufacturer
echo "HID-compliant mouse" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Config 1: HID Mouse" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

echo -ne '\\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x05\\x15\\x00\\x25\\x01\\x95\\x05\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x03\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x03\\x81\\x06\\xC0\\xC0' > functions/hid.usb0/report_desc




ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC


