from .contants import PARTS
import serial, time


class Locker:
    def __init__(self, port_name: str, baudrate: int, timeout: int):
        self.serial = serial.Serial(
            port=port_name,
            baudrate=baudrate,
            timeout=timeout,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
        )
        self.all_doors: list[str] = []
        for part in PARTS:
            self.all_doors += part["doors"]
        self.last_status: list[int] = []
        self.last_record = time.time()

    def fetch_status(self):
        total_status: list[int] = []
        for part in PARTS:
            self.serial.write(bytes.fromhex(part["segment"]))
            res = self.serial.read(1000)
            print(part["segment"], res)
            if not len(res.hex()):
                continue
            total_status += self.decode_status(res.hex())
        self.last_status = total_status
        self.last_record = time.time()
    
    def get_status(self):
        return self.last_status
    
    def open_door(self, door_idx: int):
        door_idx -= 1
        
        if door_idx < 0 or door_idx >= len(self.all_doors):
            raise Exception("Invalid door index")
        self.serial.write(bytes.fromhex(self.all_doors[door_idx]))

    def decode_status(self, status: str):
        chunks = [status[i:i+2] for i in range(0, len(status), 2)]
        door_status = self.left_pad(8, self.hex_to_bin(chunks[3])) + self.left_pad(8, self.hex_to_bin(chunks[4]))
        arr = [int(c) for c in door_status]
        return arr[0:8][::-1] + arr[8:]
    
    def left_pad(self, max_len: int, val: str):
        return "0" * (max_len - len(val)) + val
    
    def hex_to_bin(self, hex_str: str):
        return bin(int(hex_str, 16))[2:]
