from cement import Controller, ex
from ..core.ipmi import IPMI
from ..core.coretemp import get_current_cpu_temp

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
        system = self.app.pargs.system
        peripheral = self.app.pargs.peripheral

        print(get_current_cpu_temp())