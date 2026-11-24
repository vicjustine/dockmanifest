"""Tests for manifest weight and routing logic."""

from dockmanifest.model import Manifest, Pallet


def _pallet(pid: str, dest: str, kg: float) -> Pallet:
    return Pallet(pallet_id=pid, destination=dest, weight_kg=kg)


def test_total_weight_sums_pallets():
    manifest = Manifest(trailer_id="T-100", axles=3)
    manifest.add(_pallet("P1", "Oshawa", 1200))
    manifest.add(_pallet("P2", "Whitby", 800.5))
    assert manifest.total_weight_kg() == 2000.5


def test_three_axle_capacity():
    manifest = Manifest(trailer_id="T-101", axles=3)
    assert manifest.capacity_kg() == 14000


def test_overweight_detected():
    manifest = Manifest(trailer_id="T-102", axles=2)
    manifest.add(_pallet("P1", "Ajax", 9000))
    assert manifest.is_overweight() is True


def test_within_limits_not_flagged():
    manifest = Manifest(trailer_id="T-103", axles=4)
    manifest.add(_pallet("P1", "Pickering", 20000))
    assert manifest.is_overweight() is False


def test_destinations_deduplicated_in_load_order():
    manifest = Manifest(trailer_id="T-104", axles=3)
    manifest.add(_pallet("P1", "Oshawa", 100))
    manifest.add(_pallet("P2", "Whitby", 100))
    manifest.add(_pallet("P3", "Oshawa", 100))
    assert manifest.destinations() == ["Oshawa", "Whitby"]
