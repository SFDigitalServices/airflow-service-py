""" Core module """
#pylint: disable=too-few-public-methods
import os
import sentry_sdk

class Core():
    """ Core module class"""
    logger_name = ''

    def __init__(self):

        # Initialize Sentry
        sentry_dsn = os.environ.get('SENTRY_DSN')
        if((os.environ.get('environment').lower() == 'production'
                or os.environ.get('environment').lower() == 'ci')
           and os.environ.get('SENTRY_DSN_PRODUCTION')):
            sentry_dsn = os.environ.get('SENTRY_DSN_PRODUCTION')

        sentry_sdk.init(
            sentry_dsn,
            environment=os.environ.get('environment')
        )

        self.logger_name = self.__class__.__name__.lower()
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('logger', self.logger_name)
