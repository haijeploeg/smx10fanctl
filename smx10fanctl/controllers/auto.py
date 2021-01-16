from cement import Controller, ex
from ..core.ipmi import IPMI
from ..core.coretemp import get_current_cpu_temp

import time
import bisect


class Auto(Controller):
    class Meta:
        label = 'auto'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='automatic fan controlling based on your configuration',
        arguments=[
            ( ['-s', '--system'],
              {'help': 'controls the fans in the system zone (FAN[1-5])',
               'action': 'store_true',
               'dest': 'system'} ),
            ( ['-p', '--peripheral'],
              {'help': 'controls the fans in the peripheral zone (FAN[A-C])',
               'action': 'store_true',
               'dest': 'peripheral'} ),
        ])
    def auto(self):
        # Get arguments
        system = self.app.pargs.system
        peripheral = self.app.pargs.peripheral

        # Get configuration settings
        poll_interval = self.app.config.get('general', 'poll_interval')
        coretemp_label_prefix = self.app.config.get('general', 'coretemp_label_prefix')
        
        host = self.app.config.get('ipmi', 'host')
        username = self.app.config.get('ipmi', 'username')
        password = self.app.config.get('ipmi', 'password')

        if system:
            system_configuration = self.app.config.get('zones', 'system')
            system_target_temperatures = [*system_configuration]
            system_target_temperatures.sort()
        if peripheral:
            peripheral_configuration = self.app.config.get('zones', 'peripheral')
            peripheral_target_temperatures = [*peripheral_configuration]
            peripheral_target_temperatures.sort()
        
        # Setup IPMI
        ipmi = IPMI(host=host, username=username, password=password)

        while True:
            # Get the current temp
            current_temp = get_current_cpu_temp(coretemp_label_prefix)

            # If the system flag is applied
            if system:
                system_temp_list = system_target_temperatures.copy()
                # if the current temperature does not match exact any of the
                # configured pwm steps target temperatures, ensure the current
                # temperature is placed in the correct place in the list. And 
                # get the correct index value -1. If the current temperature does
                # match any of the configured values, get that exact index.
                if current_temp not in system_temp_list:
                    bisect.insort(system_temp_list, current_temp)
                    index = max(0, system_temp_list.index(current_temp) - 1)
                else:
                    index = system_temp_list.index(current_temp)

                target_system_temp = system_target_temperatures[index]
                target_system_percentage = system_configuration[target_system_temp]

            print('ZONE SYSTEM - TEMP: {} - FAN: {}%'.format(current_temp, target_system_percentage))

            time.sleep(poll_interval)