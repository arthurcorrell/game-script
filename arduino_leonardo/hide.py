import os

# path to USB firmware configuration file
# TODO: search for path
usb_core_path = r"C:\Users\arthu\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino\USBCore.cpp"
alternate_path = r"C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino\USBCore.cpp"

# make a backup for un-spoofing
backup_path = usb_core_path + '.bak'

if not os.path.exists(backup_path):
    os.rename(usb_core_path, backup_path)
    print(f'Created backup at {backup_path}')
else:
    print(f'Backup already exists: {backup_path}')

# device descriptors
serial_number = 'CH12128210102684'

VID = 0x258A
PID = 0x2023

# TODO: format from user input
product = 'Glorious Model D'
manufacturer = 'PixArt'

# prevent arduino enumerating as both HID and serial devices. Remove USB serial from descriptor


# replacement settings
replacements = {
    '#define USB_VID': f'#define USB_VID {VID}', 
    '#define USB_PID': f'#define USB_PID {PID}',  
    'const u8 STRING_PRODUCT[]': "const u8 STRING_PRODUCT[] = {USB_STRING_DESCRIPTOR_HEADER(16), 'G', 'l', 'o', 'r', 'i', 'o', 'u', 's', ' ', 'M', 'o', 'd', 'e', 'l', ' ', 'D'};",
    'const u8 STRING_MANUFACTURER[]': "const u8 STRING_MANUFACTURER[] = {USB_STRING_DESCRIPTOR_HEADER(6), 'P', 'i', 'x', 'A', 'r', 't'};",
}

"""
usb_class = 0x03
usb_subclass = 0x01

Locate the Device Descriptor Section
Find the line that defines the Device Descriptor.
Modify the bDeviceClass, bDeviceSubClass, and bDeviceProtocol fields.
Here’s what to change:

#define USB_DEVICE_CLASS        0x00  // Set to 0x00 to indicate that the class is defined in the interface descriptor
#define USB_DEVICE_SUBCLASS     0x00  // No subclass at the device level
#define USB_DEVICE_PROTOCOL     0x00  // No specific protocol at the device level

Locate the Configuration Descriptor Section
Next, find the Configuration Descriptor section. Look for a line defining the interface descriptor for the HID interface, and set the Class and Subclass.

Replace the current values with the following:

#define HID_INTERFACE_CLASS     0x03  // HID
#define HID_INTERFACE_SUBCLASS  0x01  // Boot Interface
#define HID_INTERFACE_PROTOCOL  0x02  // Mouse
"""

# navigate and modify USBCore.cpp
with open(backup_path, 'r') as file:
    lines = file.readlines()

with open(usb_core_path, 'w') as file:
    for line in lines:
        for key, replacement in replacements.items():
            if key in line:
                line = replacement + "\n"
                print(f"Replaced: {key} -> {replacement}")
        file.write(line)

print("USBCore.cpp has been modified with custom descriptors.")




# --> check device descriptors with device manager