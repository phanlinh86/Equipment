"""
This module is the class for AWG instruments.
"""
from base import Base
import os

class Awg(Base):
    """
    class Awg(Base)

    Description:
        This class is the base class for Arbitrary Waveform Generator instruments. This class will have the following functions
    """

    def __init__(self, address=None) -> None:
        super().__init__(address)
        self.type = None
        self.model = None
        self.serial_no = None
        self.firmware = None

    def identify(self):
        self.type, self.model, self.serial_no, self.firmware = super().identify()
        return [self.type, self.model, self.serial_no, self.firmware]

    def is_support(self):
        pass


# Main program to test this Base function which does following things
# 1. List all the available resources
# 2. Connect to the resource
# 3. Disconnect from the resource
# 4. Check if the connection is established or not
if __name__ == "__main__":
    print("Connect to base")
    awg = Awg()
    # Step1. List all the available resources
    list_avail_resource = '\n'.join(awg.list())
    print(f'List all devices connected to this PC {os.environ["COMPUTERNAME"]}:\n{list_avail_resource}')

    # Step2. Connect to the device
    print('Connecting to IP:10.39.174.140', end=' ')
    if awg.connect('IP:10.39.174.140'):
        print('successfully !!')
    else:
        print('failed !!')
    print(f'Identity of the instrument: {awg.identify()}')
    # Step3. Disconnect from the resource
    awg.disconnect()
    # Step4. Check if the connection is established or not
    base1 = Base('IP:10.39.174.140')
    print(f'Is connected: {base1.status}')