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


def _expect_index(console, pattern, timeout=-1):
    """labgrid ConsoleExpectMixin.expect returns a 4-tuple, not an index."""
    result = console.expect(pattern, timeout=timeout)
    if isinstance(result, tuple):
        return result[0]
    return result


HOST_PROMPT = r"(?:# |grol > )"


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
        """Re-establish a fully initialized ShellDriver after a reboot."""
        self._status = 0

        exp = getattr(self.console, "_expect", self.console)
        buf_type = getattr(exp, "buffer_type", None)
        if buf_type is not None:
            exp._buffer = buf_type()
            if hasattr(exp, "_before"):
                exp._before = buf_type()
        exp.before = b""
        exp.after = None
        exp.match = None
        exp.match_index = None

        self.console.sendline("")

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            remaining = max(1, deadline - time.monotonic())
            try:
                idx = _expect_index(
                    self.console,
                    [
                        r"(?:homeassistant|grol5000) login: ",
                        r"ha >",
                    ],
                    timeout=min(15, remaining),
                )
            except TIMEOUT:
                self.console.sendline("")
                continue

            if idx == 0:
                self.console.sendline(self.username)
                idx = _expect_index(
                    self.console,
                    [
                        HOST_PROMPT,
                        r"ha >",
                        r"Password: ",
                    ],
                    timeout=30,
                )
                if idx == 2:
                    raise RuntimeError(
                        "unexpected password prompt while reconnecting root console"
                    )

            if idx == 1:
                self.console.sendline("login")
                _expect_index(self.console, HOST_PROMPT, timeout=30)

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
            return
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
