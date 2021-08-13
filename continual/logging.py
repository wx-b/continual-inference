""" PyTorch Lightning compatible logging """

from functools import wraps
import logging


def _process_rank():
    try:
        import pytorch_lightning as pl

        if pl.utilities._HOROVOD_AVAILABLE:
            import horovod.torch as hvd

            hvd.init()
            return hvd.rank()
        else:
            return pl.utilities.rank_zero_only.rank

    except ModuleNotFoundError:
        return 0


process_rank = _process_rank()


def if_rank_zero(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        global process_rank
        if process_rank == 0:
            fn(*args, **kwargs)

    return wrapped


def getLogger(name):
    logger = logging.getLogger(name)
    logger._log = if_rank_zero(logger._log)
    return logger
