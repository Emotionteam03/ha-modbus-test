from pymodbus.client import ModbusSerialClient
import struct

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=19200,
    parity='E',
    stopbits=1,
    bytesize=8,
    timeout=3
)

print("Connexion...")
if client.connect():
    print("Connecté. Lecture du registre 3028...")
    result = client.read_holding_registers(address=3028, count=2, unit=1)
    client.close()

    if result.isError():
        print(f"Erreur Modbus : {result}")
    else:
        regs = result.registers
        print(f"Registres bruts : {regs}")
        raw = (regs[0] << 16) + regs[1]
        voltage = struct.unpack('>f', raw.to_bytes(4, byteorder='big'))[0]
        print(f"Tension lue : {voltage:.2f} V")
else:
    print("Échec de connexion série")
