"""
This module is the base class for all the instruments. 
"""
import os
import pyvisa


class Base(object):
    """ 
    class Base(object)
    This is the base class for all the instruments. This class will have the following functions
    connect(address) - Connect to the instrument
    disconnect() - Disconnect from the instrument
    list() - List all the available resources        
    """

    SUPPORTED_DEVICE = {
        'AWG'   :   ['AWG70002B', 'AWG7082C'],
        'PS'    :   ['E3631A', 'E3644A'],
    }

    def __init__(self, address = None) -> None:
        self.status = False         # Connection status
        self.__rm = pyvisa.ResourceManager()  # Resource Manager
        self.inst = None          # Instrument object        
        if address is not None:
            self.connect(address)   # Connect to the instrument uf address is provided
        else:
            self.address = None     # Address of the instrument


    def connect(self, address):
        """connect(address)
        
        Description: 
            Connect to the instrument using instrument address. (Support GPIB and IP)            
        Args:
            address:    Address of the instrument. For example,
                        GPIB:7  - GPIB address 7
                        IP:10.1.1.1 - IP address 10.1.1.1
        Returns:
            None                                    
        """
        # Check if resource manager is available. If not, create one
        if hasattr(self, '__rm') is False:
            self.__rm = pyvisa.ResourceManager()  # Resource Manager
            self.inst = None
        # Address components
        connect_type, connect_address = address.split(':')
        # this is the string address of the instrument used by pyvisa
        if connect_type == 'IP':
            visa_address = f'TCP{connect_type}0::{connect_address}::inst0::INSTR'
        elif connect_type == 'GPIB':
            visa_address = f'{connect_type}0::{connect_address}::INSTR'
        status = False  # This variable is used to check if the connection is established sucessfully
        error_message = ''  # This variable will be used to store the error message if any
        try:
            self.inst = self.__rm.open_resource(visa_address)
            status = True
        except Exception as e:
            print(f'Error: {e}')
            error_message = e
            status = False

        if status:
            self.address = address
            self.status = status

        return status, error_message

    def disconnect(self):
        """disconnect()
        
        Description: 
            Disconnect the instrument.
        Args:
            None
        
        Returns:
            None                                    
        """
        if self.status:
            self.inst.close()
            self.status = False
            self.inst = None
            print(f'Disconnected from {self.address}')
        else:
            print(f'Not connected to any device')

    def list(self):
        """list()
        
        Description:
            List all the available resources.
        Args:   
            None
        
        Returns:
            List of all the available resources.                                    
        """
        return self.__rm.list_resources()

    def identify(self):
        """identify()
        
        Description:
            Identify the instrument.
        Args:
            None
        
        Returns:
            Identity of the instrument.                                    
        """
        if self.status:
            return self.inst.query('*IDN?').split(',')
        else:
            return 'Not connected to any device'


# Main program to test this Base function which does following things
# 1. List all the available resources
# 2. Connect to the resource
# 3. Disconnect from the resource
# 4. Check if the connection is established or not
if __name__ == "__main__":
    print("Connect to base")
    base = Base()
    # Step1. List all the available resources
    list_avail_resource = '\n'.join(base.list())
    print(f'List all devices connected to this PC {os.environ["COMPUTERNAME"]}:\n{list_avail_resource}')
    # Step2. Connect to the resource
    print('Connecting to GPIB:5', end=' ')
    if base.connect('GPIB:5'):
        print('successfully !!')
    else:
        print('failed !!')
    print(f'Identity of the instrument: {base.identify()}')
    # Step3. Disconnect from the resource
    base.disconnect()
    # Step4. Create another object and check if the connection is established or not
    base1 = Base('GPIB:5')
    print(f'Is connected: {base1.status}')