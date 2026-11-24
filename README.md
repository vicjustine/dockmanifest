# dockmanifest

Build and validate dock loading manifests for freight terminals.

A trailer is rated by axle count. `dockmanifest` reads a staging CSV exported from
the yard system, totals the pallet weights, lists the stops in load order and refuses
to dispatch an overweight trailer.

## Install

    pip install dockmanifest

## Use

    dockmanifest data/staging-door-7.csv --trailer T-204 --axles 3

Exit status is `1` when the trailer is overweight, so it can gate a dispatch script.

## Axle ratings

| Axles | Capacity |
|-------|----------|
| 2     | 8 000 kg |
| 3     | 14 000 kg |
| 4     | 21 000 kg |

All data in `data/` is synthetic.
