import usb.core
import usb.util
import signal
import sys
import time
import os

def exit_gracefully():
    if dev is not None:
        usb.util.dispose_resources(dev)
        if reattach:
            dev.attach_kernel_driver(0)
    print('Done.')

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit_gracefully()

signal.signal(signal.SIGINT, signal_handler)


dev = None
devices = list(usb.core.find(find_all=True, idVendor=0xcafe, idProduct=0x4011))
for d in devices:
    print('Device: %s' % d.product)
    #if d.product.endswith('PRIMARY'):
    dev = d

#dev = usb.core.find(idVendor=0xcafe, idProduct=0x4011)

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

#print('Interface: %s' % intf)

epIn = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert epIn is not None

#print('EP In: %s' % epIn)

epOut = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert epOut is not None

#print('EP Out: %s' % epOut)


# Control transfer to enable webserial on device
print("control transfer out...")
dev.ctrl_transfer(bmRequestType = 1, bRequest = 0x22, wIndex = 2, wValue = 0x01)

data = bytearray(b'\x88\x33\x0F\x00\x00\x00\x0F\x00\x00')
# GB Printer commands
for b in data:
    print("SEND: 0x%02x" % b)
    epOut.write(b.to_bytes(1, byteorder='big'))
    recv = epIn.read(epIn.wMaxPacketSize, 100)
    print("recv from secondary: 0x%02x" % int.from_bytes(recv, byteorder='big'))

exit_gracefully()