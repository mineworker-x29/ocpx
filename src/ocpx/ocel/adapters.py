from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from .models import CanonicalOCEL, EventRecord, ObjectRecord, RelationRecord
from .validators import validate_pm4py_ocel_tables, validate_canonical_ocel


STANDARD_EVENT_COLUMNS = {"ocel:eid", "ocel:activity", "ocel:timestamp"}
STANDARD_OBJECT_COLUMNS = {"ocel:oid", "ocel:type"}
STANDARD_RELATION_COLUMNS = {"ocel:eid", "ocel:oid", "ocel:type", "ocel:qualifier"}


def _row_attributes(row: pd.Series, excluded_columns: set[str]) -> Dict[str, Any]:
    return {
        col: row[col]
        for col in row.index
        if col not in excluded_columns and pd.notna(row[col])
    }


def pm4py_tables_to_canonical(
    events: pd.DataFrame,
    objects: pd.DataFrame,
    relations: pd.DataFrame,
) -> CanonicalOCEL:
    validate_pm4py_ocel_tables(events=events, objects=objects, relations=relations)

    events_df = events.copy()
    objects_df = objects.copy()
    relations_df = relations.copy()

    events_df["ocel:timestamp"] = pd.to_datetime(events_df["ocel:timestamp"], errors="raise")

    canonical_events: List[EventRecord] = []
    for _, row in events_df.iterrows():
        canonical_events.append(
            EventRecord(
                event_id=str(row["ocel:eid"]),
                activity=str(row["ocel:activity"]),
                timestamp=row["ocel:timestamp"],
                attributes=_row_attributes(row, STANDARD_EVENT_COLUMNS),
            )
        )

    canonical_objects: List[ObjectRecord] = []
    for _, row in objects_df.iterrows():
        canonical_objects.append(
            ObjectRecord(
                object_id=str(row["ocel:oid"]),
                object_type=str(row["ocel:type"]),
                attributes=_row_attributes(row, STANDARD_OBJECT_COLUMNS),
            )
        )

    canonical_relations: List[RelationRecord] = []
    for _, row in relations_df.iterrows():
        qualifier = row["ocel:qualifier"] if "ocel:qualifier" in relations_df.columns else None
        qualifier = None if pd.isna(qualifier) else str(qualifier)

        canonical_relations.append(
            RelationRecord(
                event_id=str(row["ocel:eid"]),
                object_id=str(row["ocel:oid"]),
                object_type=str(row["ocel:type"]),
                qualifier=qualifier,
                attributes=_row_attributes(row, STANDARD_RELATION_COLUMNS),
            )
        )

    canonical = CanonicalOCEL(
        events=canonical_events,
        objects=canonical_objects,
        relations=canonical_relations,
    )
    validate_canonical_ocel(canonical)
    return canonical


def pm4py_ocel_to_canonical(pm4py_ocel: Any) -> CanonicalOCEL:
    if not hasattr(pm4py_ocel, "events"):
        raise TypeError("pm4py_ocel must have an 'events' attribute")
    if not hasattr(pm4py_ocel, "objects"):
        raise TypeError("pm4py_ocel must have an 'objects' attribute")
    if not hasattr(pm4py_ocel, "relations"):
        raise TypeError("pm4py_ocel must have a 'relations' attribute")

    return pm4py_tables_to_canonical(
        events=pm4py_ocel.events,
        objects=pm4py_ocel.objects,
        relations=pm4py_ocel.relations,
    )