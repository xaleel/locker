from locker.locker import Locker
    
def main():
    locker = Locker("/dev/bus/usb/002/009", 19200, 3)
    locker.fetch_status()
    print(locker.get_status())
    locker.open_door(1)

if __name__ == "__main__":
    main()
