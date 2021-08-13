from abc import ABC
from enum import Enum
from typing import Tuple
from torch import Tensor


class CoModule(ABC):
    """Base class for continual modules.
    Deriving from this class enforces that neccessary class methods are implemented
    """

    def __init_subclass__(cls) -> None:
        CoModule._validate_class(cls)

    @staticmethod
    def _validate_class(cls):
        for fn, description in [
            ("forward_step", "forward computation for a single temporal step"),
            (
                "forward_steps",
                "forward computation for multiple temporal step",
            ),
            (
                "forward",
                "a forward computation which is identical to a regular non-continual forward.",
            ),
        ]:
            assert callable(
                getattr(cls, fn, None)
            ), f"{cls.__name__} should implement a `{fn}` function which performs {description} to satisfy the CoModule interface."

        assert hasattr(cls, "delay") and type(cls.delay) in {
            int,
            property,
        }, f"{cls.__name__} should implement a `delay` property to satisfy the CoModule interface."

    def forward_step(self, input: Tensor) -> Tensor:
        """Clip-wise forward computation with state initialisation"""
        ...  # pragma: no cover

    def forward_steps(self, input: Tensor) -> Tensor:
        """Clip-wise forward computation with state initialisation"""
        ...  # pragma: no cover

    def forward(self, input: Tensor) -> Tensor:
        """Clip-wise forward without state initialisation, but which is identical to the non-continual component"""
        ...  # pragma: no cover

    @property
    def delay(self) -> int:
        """Temporal delay of the module

        Returns:
            int: Temporal delay of the module
        """
        ...  # pragma: no cover

    def clean_state(self):
        """Clean module state
        This serves as a dummy function for modules which do not require state-cleanup
        """
        ...  # pragma: no cover


class TensorPlaceholder:
    shape: Tuple[int]

    def __init__(self, shape: Tuple[int]):
        self.shape = shape

    def size(self):
        return self.shape


class FillMode(Enum):
    REPLICATE = "replicate"
    ZEROS = "zeros"
