import enum
import os
import time

import attr
from pexpect import TIMEOUT

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

        Discard every prompt from the previous boot by waiting for the new
        GRUB line, then walk login / ha-cli / host-shell until labgrid can
        inject run() on a real host prompt.
        """
        self._status = 0
        self.console.expect(r"Booting `", timeout=timeout)

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            remaining = max(1, deadline - time.monotonic())
            try:
                idx = self.console.expect(
                    [
                        r"(?:homeassistant|grol5000) login: ",
                        r"ha >",
                        r"(?:# |grol > )",
                        r"Password: ",
                    ],
                    timeout=min(15, remaining),
                )
            except TIMEOUT:
                self.console.sendline("")
                continue

            if idx == 0:
                self.console.sendline(self.username)
                continue
            if idx == 1:
                # Stock HAOS appliance CLI (including after OTA to upstream).
                self.console.sendline("login")
                continue
            if idx == 3:
                raise RuntimeError(
                    "unexpected password prompt while reconnecting root console"
                )

            # idx == 2: host shell (# or grol >)
            self._status = 1
            self._inject_run()
            self._check_prompt()
            return

        raise TIMEOUT(f"reconnect_after_reboot exceeded {timeout}s")


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
