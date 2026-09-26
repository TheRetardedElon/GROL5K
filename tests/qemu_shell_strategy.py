import enum
import os

import attr

from labgrid import target_factory, step
from labgrid.driver import ShellDriver
from labgrid.strategy import Strategy, StrategyError


class Status(enum.Enum):
    unknown = 0
    off = 1
    shell = 2


@target_factory.reg_driver
@attr.s(eq=False)
class CustomTimeoutShellDriver(ShellDriver):
    """ShellDriver with a config-customizable timeout for run and run_check."""
    command_timeout = attr.ib(default=30, validator=attr.validators.instance_of(int))

    def run(self, cmd: str, *, timeout=None, codec="utf-8", decodeerrors="strict"):
        return super().run(cmd, timeout=timeout or self.command_timeout, codec=codec, decodeerrors=decodeerrors)

    def run_check(self, cmd: str, *, timeout=None, codec="utf-8", decodeerrors="strict"):
        return super().run_check(cmd, timeout=timeout or self.command_timeout, codec=codec, decodeerrors=decodeerrors)

    def reconnect_after_reboot(self, timeout=180):
        """Re-establish a fully initialized ShellDriver after a reboot.

        The pre-reboot driver state is invalid once the machine restarts.
        Reconnect to either GROL5000 or stock HAOS, then restore the same
        internal state ShellDriver.on_activate() normally establishes,
        including the injected run() helper used by run_check().
        """
        # Any prior shell state belongs to the old boot.
        self._status = 0

        idx = self.console.expect(
            [
                r"(?:homeassistant|grol5000) login: ",
                r"ha > ",
            ],
            timeout=timeout,
        )

        if idx == 0:
            self.console.sendline(self.username)
            idx = self.console.expect(
                [
                    r"(?:# |grol > )",
                    r"ha > ",
                    r"Password: ",
                ],
                timeout=30,
            )
            if idx == 2:
                raise RuntimeError(
                    "unexpected password prompt while reconnecting root console"
                )

        if idx == 1:
            # Stock HAOS lands in the appliance CLI. Enter the host shell.
            self.console.sendline("login")
            self.console.expect(r"# ", timeout=30)

        # We now own a real host shell on the new boot. Recreate the state
        # ShellDriver.on_activate() would normally establish.
        self._status = 1
        self._check_prompt()
        self._inject_run()



@target_factory.reg_driver
@attr.s(eq=False)
class QEMUShellStrategy(Strategy):
    """Strategy for starting a QEMU VM and running shell commands within it."""

    bindings = {
        "qemu": "QEMUDriver",
        "shell": "CustomTimeoutShellDriver",
    }

    status = attr.ib(default=Status.unknown)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        if "-accel kvm" in self.qemu.extra_args and os.environ.get("NO_KVM"):
            self.qemu.extra_args = self.qemu.extra_args.replace(
                "-accel kvm", ""
            ).strip()

    @step(args=["status"])
    def transition(self, status, *, step):  # pylint: disable=redefined-outer-name
        if not isinstance(status, Status):
            status = Status[status]
        if status == Status.unknown:
            raise StrategyError(f"can not transition to {status}")
        elif status == self.status:
            step.skip("nothing to do")
            return  # nothing to do
        elif status == Status.off:
            self.target.deactivate(self.qemu)
            self.target.deactivate(self.shell)
        elif status == Status.shell:
            self.target.activate(self.qemu)
            self.qemu.on()
            self.target.activate(self.shell)
        else:
            raise StrategyError(f"no transition found from {self.status} to {status}")
        self.status = status
