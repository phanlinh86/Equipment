"""
This module is the class for power supply instruments. 
"""
from base import Base

class PowerSupply(Base):
    """
    class PowerSupply(Base)
    
    Description:
        This class is the base class for all the power supply instruments. This class will have the following functions
        set(voltage, channel) - Set the voltage and current
        get(property) - Get voltage, current, channel or other properties
        on() - Turn on the output
        off() - Turn off the output
    """
    def __init__(self, address = None) -> None:
        super().__init__(address)
        self.voltage = None
        self.current = None
        self.channel = None
        
    def __str__(self) -> str:
        str_instrument = self.get()
        
        if str_instrument:
            return str_instrument
        else:
            return 'Instrument not connected'
    
    def on(self):
        """on()
        
        Description: 
            Turn on the output of the power supply            
        Args:
            None
        Returns:
            None                                    
        """
        if self.status:
            self.inst.write('OUTP ON')
        else:
            print('Error: Instrument not connected')
            
    def off(self):
        """off()
        
        Description: 
            Turn off the output of the power supply            
        Args:
            None
        Returns:
            None                                    
        """
        if self.status:
            self.inst.write('OUTP OFF')
        else:
            print('Error: Instrument not connected')

    def set(self, voltage = None, current = None, channel = None):
        """set(voltage = None, current = None, channel = None):
        
        Description: 
            Set the property of the power supply, including voltage, current and channel            
            
        Args:
            property - Property to set
            value - Value to set
        Returns:
            None
        """

        if self.status:
            if channel is not None:
                self.inst.write(f'INST {channel}')
                self.channel = channel
            if voltage is not None:
                self.inst.write(f'VOLT {voltage}')
                self.voltage = voltage
            if current is not None:
                self.inst.write(f'CURR {current}')
                self.current = current
        else:
            print('Error: Instrument not connected')

    def get(self, field = None):
        """get(field = None)
        
        Description: 
            Get the property of the power supply, including voltage, current and channel            
            
        Args:
            property - Property to get
        Returns:
            Value of the property
        """
        if self.status:
            if field is None:
                self.voltage = float(self.inst.query('VOLT?').strip())
                self.current = float(self.inst.query('CURR?').strip())
                self.channel = self.inst.query('INST?').strip()
                return f'{self.channel}: {self.voltage}V, {self.current}A'
            else:
                if field == 'voltage':
                    self.voltage = float(self.inst.query('VOLT?').strip())
                    return self.voltage
                elif field == 'current':
                    self.current = float(self.inst.query('CURR?').strip())
                    return self.current
                elif field == 'channel':
                    self.channel = self.inst.query('INST?').strip()
                    return self.channel
                else:
                    print('Error: Property not found')
                                        
        else:
            print('Error: Instrument not connected')
        return None



# This is the main function to test the PowerSupply class
# 1. Connect to the power supply instrument, display the list of available resources and identify the instrument
# 2. Turn on and off the output of the power supply. Check the voltage, current and channel of the power supply
# 3. Set the voltage and current of the power supply
# 4. Disconnect from the power supply
# 5. Check the status of the power supply

if __name__ == '__main__':
    # 1. Connect to the power supply instrument, display the list of available resources and identify the instrument
    print('Step1. Connect to the power supply instrument, display the list of available resources and identify the instrument')
    ps = PowerSupply('GPIB:7')
    print(ps.list())
    print(ps.identify())
    # 2. Turn on and off the output of the power supply. Check the voltage, current and channel of the power supply
    print('Step2. Turn on and off the output of the power supply. Check the voltage, current and channel of the power supply')
    ps.on()
    ps.off()
    print(ps)
    # 3. Set the voltage and current of the power supply
    print('Step3. Set the voltage and current of the power supply')
    ps.set(5, 1, 'P25V')
    print(ps)
    print(ps.get('voltage'))
    print(ps.get('current'))
    print(ps.get('channel'))
    # 4. Disconnect from the power supply
    print('Step4. Disconnect from the power supply')
    ps.disconnect()
    # 5. Check the status of the power supply
    print('Step5. Check the status of the power supply')
    print(ps)