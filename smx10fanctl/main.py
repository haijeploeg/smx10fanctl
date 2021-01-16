from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import AppError
from .controllers.base import Base
from .controllers.auto import Auto
from .controllers.set import Set


# configuration defaults
CONFIG = init_defaults('general', 'ipmi', 'zones')
CONFIG['general']['poll_interval'] = 5
CONFIG['general']['coretemp_label_prefix'] = None
CONFIG['ipmi']['host'] = 'localhost'
CONFIG['ipmi']['username'] = None
CONFIG['ipmi']['password'] = None
CONFIG['ipmi']['profiles'] = {'full': 1}
CONFIG['zones']['system'] = {0: 30, 80: 100}
CONFIG['zones']['peripheral'] = {0: 50, 60: 100}


class Smx10Fanctl(App):
    """Supermicro X10 Fancontroller primary application."""

    class Meta:
        label = 'smx10fanctl'

        # configuration defaults
        config_defaults = CONFIG
        config_files = ['./.smx10fanctl.yml']

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'print',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # register handlers
        handlers = [
            Base,
            Auto,
            Set,
        ]


def main():
    with Smx10Fanctl() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except AppError as e:
            print('AppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
