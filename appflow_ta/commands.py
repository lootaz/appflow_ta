from flask import current_app
from flask_script import Command, Option

from appflow_ta import services


class RunCommand(Command):
    option_list = (
        Option("--host", "-h", dest="host"),
        Option("--port", "-p", dest="port")
    )
    def run(self, host=None, port=None):
        services.run_crawler_service()

        host = host or current_app.config['HOST']
        port = port or current_app.config['PORT']

        current_app.run(host=host, port=port)
