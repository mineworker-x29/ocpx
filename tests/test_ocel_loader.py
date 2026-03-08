from pathlib import Path

import pandas as pd

from ocpx.ocel.adapters import pm4py_tables_to_canonical


def test_pm4py_tables_to_canonical_minimal():
    events = pd.DataFrame(
        [
            {
                "ocel:eid": "e1",
                "ocel:activity": "Create Order",
                "ocel:timestamp": "2024-01-01T10:00:00",
                "cost": 100,
            }
        ]
    )
    objects = pd.DataFrame(
        [
            {
                "ocel:oid": "o1",
                "ocel:type": "order",
                "priority": "high",
            }
        ]
    )
    relations = pd.DataFrame(
        [
            {
                "ocel:eid": "e1",
                "ocel:oid": "o1",
                "ocel:type": "order",
                "ocel:qualifier": "creation",
            }
        ]
    )

    canonical = pm4py_tables_to_canonical(events, objects, relations)

    assert len(canonical.events) == 1
    assert len(canonical.objects) == 1
    assert len(canonical.relations) == 1
    assert canonical.events[0].activity == "Create Order"
    assert canonical.objects[0].object_type == "order"
    assert canonical.relations[0].qualifier == "creation"