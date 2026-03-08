from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pandas as pd


@dataclass(slots=True)
class EventRecord:
    event_id: str
    activity: str
    timestamp: pd.Timestamp
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ObjectRecord:
    object_id: str
    object_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RelationRecord:
    event_id: str
    object_id: str
    object_type: str
    qualifier: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CanonicalOCEL:
    events: List[EventRecord]
    objects: List[ObjectRecord]
    relations: List[RelationRecord]
    event_id_column: str = "ocel:eid"
    object_id_column: str = "ocel:oid"
    object_type_column: str = "ocel:type"
    activity_column: str = "ocel:activity"
    timestamp_column: str = "ocel:timestamp"

    def event_ids(self) -> set[str]:
        return {e.event_id for e in self.events}

    def object_ids(self) -> set[str]:
        return {o.object_id for o in self.objects}

    def object_types(self) -> set[str]:
        return {o.object_type for o in self.objects}

    def to_event_dataframe(self) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        for event in self.events:
            row = {
                self.event_id_column: event.event_id,
                self.activity_column: event.activity,
                self.timestamp_column: event.timestamp,
            }
            row.update(event.attributes)
            rows.append(row)
        return pd.DataFrame(rows)

    def to_object_dataframe(self) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        for obj in self.objects:
            row = {
                self.object_id_column: obj.object_id,
                self.object_type_column: obj.object_type,
            }
            row.update(obj.attributes)
            rows.append(row)
        return pd.DataFrame(rows)

    def to_relation_dataframe(self) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        for rel in self.relations:
            row = {
                self.event_id_column: rel.event_id,
                self.object_id_column: rel.object_id,
                self.object_type_column: rel.object_type,
            }
            if rel.qualifier is not None:
                row["ocel:qualifier"] = rel.qualifier
            row.update(rel.attributes)
            rows.append(row)
        return pd.DataFrame(rows)