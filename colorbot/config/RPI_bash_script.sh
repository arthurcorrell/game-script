

cd /sys/kernel/config/usb_gadget/
mkdir -p pi_hid
cd pi_hid


#HID\VID_258A&PID_2023&MI_00\7&18CB7810&0&0000

#VID, PID info
#MI: multiple interface
#last bit: device instance path - indicates port, hub or connection
# find these by chekcing mouse details on manufacturer website or lsusb tool
echo 0x258A > idVendor # VID vendorID for glorious PixArt
echo 0x2023 > idProduct # PID productID for model d wireless

# basic information
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB


# serial number manufacturer and product are product specific
# s/n CH12128210102684
mkdir -p strings/0x409
echo "CH12128210102684" > strings/0x409/serialnumber # use realistic serialnumber
echo "PixArt" > strings/0x409/manufacturer
echo "HID-compliant mouse" > strings/0x409/product

# Create configuration
mkdir -p configs/c.1/strings/0x409
echo "Config 1: HID Mouse" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

# modify the HID report descriptor to reflect the features of that device
# extract from device driver or tool like wireshark or technical documentation
# 5 button mouse report descriptor
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x05\\x15\\x00\\x25\\x01\\x95\\x05\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x03\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x03\\x81\\x06\\xc0\\xc0 > functions/hid.usb0/report_desc




ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC


#https://the-sz.com/products/usbid/index.php?v=0x258A

#use dmesg or lsusb on the laptop to ensure the Raspberry Pi is detected with the correct identifiers.
#and Control panel -> devices -> properties -> details

