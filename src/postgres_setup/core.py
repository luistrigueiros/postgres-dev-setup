
import subprocess

from .commands import Command


class PostgresDevSetup(Command):
    def __init__(self):
        super().__init__(name="__postgres_dev_setup__", description="Internal helper")
