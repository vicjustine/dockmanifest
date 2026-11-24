"""Core types for a dock loading manifest."""

from dataclasses import dataclass, field

# Trailers are rated by axle count; exceeding the rating is a load-out violation.
AXLE_LIMITS_KG = {2: 8000, 3: 14000, 4: 21000}


@dataclass
class Pallet:
    """One palletised consignment staged at a dock door."""

    pallet_id: str
    destination: str
    weight_kg: float
    stackable: bool = True


@dataclass
class Manifest:
    """A trailer's load-out, built door by door."""

    trailer_id: str
    axles: int
    pallets: list[Pallet] = field(default_factory=list)

    def add(self, pallet: Pallet) -> None:
        self.pallets.append(pallet)

    def total_weight_kg(self) -> float:
        return sum(p.weight_kg for p in self.pallets)

    def capacity_kg(self) -> int:
        return AXLE_LIMITS_KG[self.axles]

    def is_overweight(self) -> bool:
        return self.total_weight_kg() > self.capacity_kg()

    def destinations(self) -> list[str]:
        """Stops in the order they were loaded, de-duplicated."""
        seen: list[str] = []
        for pallet in self.pallets:
            if pallet.destination not in seen:
                seen.append(pallet.destination)
        return seen
