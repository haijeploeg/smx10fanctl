from cement import Controller, ex
from ..core.ipmi import IPMI
from ..core.coretemp import get_current_cpu_temp

import time


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
        if peripheral:
            peripheral_configuration = self.app.config.get('zones', 'peripheral')
        
        # Setup IPMI
        ipmi = IPMI(host=host, username=username, password=password)

        while True:
            current_temp = get_current_cpu_temp(coretemp_label_prefix)
            self.app.print(current_temp)

            time.sleep(poll_interval)