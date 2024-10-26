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
    def __init__(self, address = None) -> None:
        self.address = address      # Address of the instrument
        self.status = False         # Connection status
        self.__rm = pyvisa.ResourceManager()  # Resource Manager
        self.__inst = None          # Instrument object        

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
        # Address components
        connect_type, connect_address = address.split(':')
        # this is the string address of the instrument used by pyvisa
        visa_address = f'{connect_type}0::{connect_address}::INSTR'
        status = False  # This variable is used to check if the connection is established sucessfully
        error_message = ''  # This variable will be used to store the error message if any
        if visa_address in self.list():
            try:
                self.__inst = self.__rm.open_resource(visa_address)
                status = True
            except Exception as e:
                print(f'Error: {e}')
                error_message = e
                status = False
        else:
            print(f'Error: {address} not found')
            status = False

        if status:
            self.address = address
            self.status = status
            print(f'Connected to {address}')

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
            self.__inst.close()
            self.status = False
            self.__inst = None
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
            return self.__inst.query('*IDN?').split(',')
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
    print(f'List all devices connected to this PC {os.environ["COMPUTERNAME"]}: {', '.join(base.list())}')
    # Step2. Connect to the resource
    print('Connecting to GPIB:7', end=' ')
    if base.connect('GPIB:7'):
        print('successfully !!')
    else:
        print('failed !!')
    print(f'Identity of the instrument: {base.identify()}')
    # Step3. Disconnect from the resource
    base.disconnect()
