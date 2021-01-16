from cement import Controller, ex
from ..core.ipmi import IPMI


class Set(Controller):
    class Meta:
        label = 'set'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        label='set',
        help='set the fan speed manually',
        arguments=[
            ( ['-s', '--system'],
              {'help': 'controls the fans in the system zone (FAN[1-5])',
               'action': 'store_true',
               'dest': 'system'} ),
            ( ['-p', '--peripheral'],
              {'help': 'controls the fans in the peripheral zone (FAN[A-C])',
               'action': 'store_true',
               'dest': 'peripheral'} ),
            ( ['percentage'],
              {'help': 'the percentage to set',
               'action': 'store',
               'type': int} ),
        ])
    def set_manually(self):
        # Get arguments
        system = self.app.pargs.system
        peripheral = self.app.pargs.peripheral
        percentage = self.app.pargs.percentage

        # Get configuration
        host = self.app.config.get('ipmi', 'host')
        username = self.app.config.get('ipmi', 'username')
        password = self.app.config.get('ipmi', 'password')

        # Setup IPMI
        ipmi = IPMI(host=host, username=username, password=password)

        # If the system flag is supplied, set the fan speed
        if system:
            result = ipmi.set_fan_speed('system', percentage)
            if not result:
                self.app.log.error('Failed to set the fan speed to {}% in zone system.'.format(
                    percentage
                ))
            else:
                self.app.log.info('Successfully set the fan speed to {}% in zone system.'.format(
                    percentage
                ))

        # If the peripheral flag is supplied, set the fan speed
        if peripheral:
            result = ipmi.set_fan_speed('peripheral', percentage)
            if not result:
                self.app.log.error('Failed to set the fan speed to {}% in zone peripheral.'.format(
                    percentage
                ))
            else:
                self.app.log.info('Successfully set the fan speed to {}% in zone peripheral.'.format(
                    percentage
                ))
