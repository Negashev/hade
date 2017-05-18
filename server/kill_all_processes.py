import signal, os, errno
from .log import log


def ignore_signals_and_raise_keyboard_interrupt(signame):
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    raise KeyboardInterrupt(signame)


class AlarmException(Exception):
    pass


def raise_alarm_exception():
    raise AlarmException('Alarm')


signal.signal(signal.SIGTERM, lambda signum, frame: ignore_signals_and_raise_keyboard_interrupt('SIGTERM'))
signal.signal(signal.SIGINT, lambda signum, frame: ignore_signals_and_raise_keyboard_interrupt('SIGINT'))
signal.signal(signal.SIGALRM, lambda signum, frame: raise_alarm_exception())


def kill_all_processes(time_limit=0):
    log.info("Killing all processes...")
    time_limit += 20
    try:
        os.kill(-1, signal.SIGTERM)
    except OSError:
        pass
    signal.alarm(time_limit)
    try:
        # Wait until no more child processes exist.
        done = False
        while not done:
            try:
                os.waitpid(-1, 0)
            except OSError as e:
                if e.errno == errno.ECHILD:
                    done = True
                else:
                    raise
    except AlarmException:
        log.warn("Not all processes have exited in time. Forcing them to exit.")
        try:
            os.kill(-1, signal.SIGKILL)
        except OSError:
            pass
    finally:
        signal.alarm(0)
