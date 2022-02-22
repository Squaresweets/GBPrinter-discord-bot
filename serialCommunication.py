# import serial
#
# serial_port = serial.Serial(
#     port='COM9',
#     baudrate=9600
#     )
#
# data = [0x88,0x33,0x0f,0x00,0x00,0x00,0x0f,0x00,0x00]
# serial_port.write(serial.to_bytes(data))
# while True:
#     data = serial_port.read()
#     if int.from_bytes(data,byteorder='big') != 0:
#         print(hex(int.from_bytes(data,byteorder='big')))

from winusbcdc import ComPort
p = ComPort("USB Serial Device (COM9)")  # friendly name as shown in device manager

p.open()
p.write(b"/x88/x33/x0f/x00/x00/x00/x0f/x00/x00")
print(p.read())
p.close()