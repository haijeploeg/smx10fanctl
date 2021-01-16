from cement import Controller, ex
from ..core.ipmi import IPMI
from ..core.coretemp import get_current_cpu_temp
from ..core.exc import NoFullFanProfileFound, CouldNotSetFanProfile

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
        profiles = self.app.config.get('ipmi', 'profiles')

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

        # Before starting, ensure the full fan mode is set
        if 'full' not in profiles:
            self.app.log.fatal('No fan profile with the name: full found in the configuration')
            raise NoFullFanProfileFound()

        full_profile_id = profiles['full']
        if full_profile_id != ipmi.get_current_fan_profile():
            result = ipmi.set_fan_profile(full_profile_id)
            if not ipmi.set_fan_profile(full_profile_id):
                self.app.log.fatal('Could not set fan profile with id: {}'.format(full_profile_id))
                raise CouldNotSetFanProfile()
            else:
                self.app.log.info('Successfully changed the fan profile to full with id {}'.format(
                    full_profile_id
                ))

        while True:
            # Get the current temp
            current_temp = get_current_cpu_temp(coretemp_label_prefix)
            self.app.log.info('Current CPU temperature: {}'.format(current_temp))

            # If the system flag is applied, follow this logic
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

                # Get the configured target temperature and its configured fan percentage
                target_system_temp = system_target_temperatures[index]
                target_system_percentage = system_configuration[target_system_temp]

                # Execute the command to set the fan speed in the system zone
                result = ipmi.set_fan_speed('system', target_system_percentage)
                if not result:
                    self.app.log.error('Failed to set the fan speed to {}% in zone system'.format(
                        target_system_percentage
                    ))
                else:
                    self.app.log.info('Successfully set the fan speed to {}% in zone system'.format(
                        target_system_percentage
                    ))

            # If the peripheral flag is applied, follow this logic
            if peripheral:
                peripheral_temp_list = peripheral_target_temperatures.copy()
                # if the current temperature does not match exact any of the
                # configured pwm steps target temperatures, ensure the current
                # temperature is placed in the correct place in the list. And 
                # get the correct index value -1. If the current temperature does
                # match any of the configured values, get that exact index.
                if current_temp not in peripheral_temp_list:
                    bisect.insort(peripheral_temp_list, current_temp)
                    index = max(0, peripheral_temp_list.index(current_temp) - 1)
                else:
                    index = peripheral_temp_list.index(current_temp)

                target_peripheral_temp = peripheral_target_temperatures[index]
                target_peripheral_percentage = peripheral_configuration[target_peripheral_temp]
                
                # Execute the command to set the fan speed in the system zone
                result = ipmi.set_fan_speed('peripheral', target_peripheral_percentage)
                if not result:
                    self.app.log.error('Failed to set the fan speed to {}% in zone peripheral'.format(
                        target_peripheral_percentage
                    ))
                else:
                    self.app.log.info('Successfully set the fan speed to {}% in zone peripheral'.format(
                        target_peripheral_percentage
                    ))

            # Sleep the configured poll_interval_seconds
            time.sleep(poll_interval)