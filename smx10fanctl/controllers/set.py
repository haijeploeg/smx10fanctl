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
        system = self.app.pargs.system
        peripheral = self.app.pargs.peripheral
        percentage = self.app.pargs.percentage

        ipmi = IPMI()

        if system:
            result = ipmi.set_fan_speed('system', percentage)
            self.app.log.info(result)

        if peripheral:
            result = ipmi.set_fan_speed('peripheral', percentage)
            self.app.log.info(result)