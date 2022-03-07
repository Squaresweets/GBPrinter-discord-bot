import usb.core
import usb.util
import signal
import sys
import time
import os

from PIL import Image, ImageOps
import numpy as np

INQU = bytearray(b'\x88\x33\x0F\x00\x00\x00\x0F\x00\x00')
INIT = bytearray(b'\x88\x33\x01\x00\x00\x00\x01\x00\x00\x00')
PRNT = bytearray(b'\x88\x33\x02\x00\x04\x00\x01\x00\xE4\x40\x2B\x01\x00\x00')
EMPT = bytearray(b'\x88\x33\x04\x00\x00\x00\x04\x00\x00\x00')
DATA_header = bytearray(b'\x88\x33\x04\x00\x80\x02')

def exit_gracefully():
    if dev is not None:
        usb.util.dispose_resources(dev)
        if reattach:
            dev.attach_kernel_driver(0)
    exit()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit_gracefully()


def send(data):
    print("SENDING: ", end="")
    for b in data:
        print("0x%02x " % b, end="")
        epOut.write(b.to_bytes(1, byteorder='big'))
    print("")

# def send(data):
#     print("SENDING: ", end="")
#     for b in data:
#         print("0x%02x " % b, end="")
#     epOut.write(data)
#     print("")


def read():
    recv = int.from_bytes(epIn.read(epIn.wMaxPacketSize, 100), byteorder='big')
    print("0x%02x " % recv)
    return recv

signal.signal(signal.SIGINT, signal_handler)

dev = None
devices = list(usb.core.find(find_all=True, idVendor=0xcafe, idProduct=0x4011))
for d in devices:
    dev = d

if dev is None:
    raise ValueError('Device not found')

reattach = False
if (os.name != "nt"):
    if dev.is_kernel_driver_active(0):
        try:
            reattach = True
            dev.detach_kernel_driver(0)
            print("kernel driver detached")
        except usb.core.USBError as e:
            sys.exit("Could not detach kernel driver: %s" % str(e))
    else:
        print("no kernel driver attached")

dev.reset()

dev.set_configuration()

cfg = dev.get_active_configuration()

intf = cfg[(2,0)]   # Or find interface with class 0xff

epIn = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert epIn is not None

epOut = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert epOut is not None


# Control transfer to enable webserial on device
dev.ctrl_transfer(bmRequestType = 1, bRequest = 0x22, wIndex = 2, wValue = 0x01)



# Load image from before
image = Image.open("dithered.png")
img = np.array(ImageOps.fit(image, (160, 144)))
# create the byte array to store the entire image
data = bytearray()
for y in range(144):
    for x in range(0, 160, 4):
        byte = 0
        byte = byte + (int(img[y][x] / 64) << 6)
        byte = byte + (int(img[y][x+1] / 64) << 4)
        byte = byte + (int(img[y][x+2] / 64) << 2)
        byte = byte + int(img[y][x+3] / 64)
        data.append(byte)




send(INQU)
recv = read()
if recv == 0x8100:
    print("Printer is there :D")
else:
    print("Printer is not there :(")
    #exit_gracefully()


send(INIT)
read()

c = 0
# Send the data over for each of the 9 sections of the image
for i in range(9):
    DATA_SD = bytearray(649)
    checksum = 0x04 + 0x08 + 0x02
    dataSection = data[i*640:(i+1)*640]

    for j in range(len(dataSection)):
        checksum = checksum + dataSection[j]

    DATA_SD[:] = DATA_header
    DATA_SD[6:6+len(dataSection)] = dataSection
    DATA_SD.append(checksum & 0x00FF)
    DATA_SD.append(min(checksum >> 8, 255))
    DATA_SD.append(0)
    DATA_SD.append(0)
    send(DATA_SD)
    read()

send(INQU)
read()
send(PRNT)
read()
send(INQU)
read()

while True:
    send(INQU)
    time.sleep(1.2)
exit_gracefully()