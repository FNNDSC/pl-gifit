import pytest

from innerspfit.model import Model


@pytest.fixture(scope='session')
def model() -> Model:
    return Model()


@pytest.mark.parametrize(
    'gi, matched',
    [
        (0.8, 1.00),
        (0.9, 1.00),
        (1.0, 1.00),
        (1.01, 1.02),
        (1.015, 1.02),
        (1.02, 1.02),
        (1.03, 1.05),
        (1.04, 1.05),
        (1.05, 1.05),
        (1.06, 1.07),
        (1.07, 1.07),
        (1.19, 1.20),
        (1.20, 1.20),
        (1.21, 1.20),
        (1.22, 1.20),
    ],
)
def test_get_params_for(gi: float, matched: float, model: Model):
    assert model._match_gi(gi) == matched
