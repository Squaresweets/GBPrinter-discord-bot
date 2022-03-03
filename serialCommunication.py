import usb.core
import usb.util
import signal
import sys
import time
import os

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


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit_gracefully()


def send(data):
    print("SENDING: ", end="")
    for b in data:
        print("0x%02x " % b, end="")
        epOut.write(b.to_bytes(1, byteorder='big'))
    print("")


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

send(INQU)
recv = int.from_bytes(epIn.read(epIn.wMaxPacketSize, 100), byteorder='little')
if recv == 0x81:
    print("Printer is there :D")


exit_gracefully()