from __future__ import annotations

from typing import Iterable

import pandas as pd

from .models import CanonicalOCEL


REQUIRED_EVENT_COLUMNS = {"ocel:eid", "ocel:activity", "ocel:timestamp"}
REQUIRED_OBJECT_COLUMNS = {"ocel:oid", "ocel:type"}
REQUIRED_RELATION_COLUMNS = {"ocel:eid", "ocel:oid", "ocel:type"}


def _missing_columns(df: pd.DataFrame, required: Iterable[str]) -> set[str]:
    return set(required) - set(df.columns)


def validate_pm4py_ocel_tables(
    events: pd.DataFrame,
    objects: pd.DataFrame,
    relations: pd.DataFrame,
) -> None:
    missing_events = _missing_columns(events, REQUIRED_EVENT_COLUMNS)
    missing_objects = _missing_columns(objects, REQUIRED_OBJECT_COLUMNS)
    missing_relations = _missing_columns(relations, REQUIRED_RELATION_COLUMNS)

    errors = []
    if missing_events:
        errors.append(f"events missing columns: {sorted(missing_events)}")
    if missing_objects:
        errors.append(f"objects missing columns: {sorted(missing_objects)}")
    if missing_relations:
        errors.append(f"relations missing columns: {sorted(missing_relations)}")

    if errors:
        raise ValueError(" | ".join(errors))

    if events["ocel:eid"].isna().any():
        raise ValueError("events contains null values in 'ocel:eid'")
    if objects["ocel:oid"].isna().any():
        raise ValueError("objects contains null values in 'ocel:oid'")
    if relations["ocel:eid"].isna().any() or relations["ocel:oid"].isna().any():
        raise ValueError("relations contains null values in 'ocel:eid' or 'ocel:oid'")

    if not pd.api.types.is_datetime64_any_dtype(events["ocel:timestamp"]):
        # 최대한 안전하게 datetime 변환 가능 여부만 먼저 검사
        try:
            pd.to_datetime(events["ocel:timestamp"], errors="raise")
        except Exception as exc:
            raise ValueError("events['ocel:timestamp'] cannot be parsed as datetime") from exc


def validate_canonical_ocel(ocel: CanonicalOCEL) -> None:
    event_ids = ocel.event_ids()
    object_ids = ocel.object_ids()

    for rel in ocel.relations:
        if rel.event_id not in event_ids:
            raise ValueError(f"relation references unknown event_id: {rel.event_id}")
        if rel.object_id not in object_ids:
            raise ValueError(f"relation references unknown object_id: {rel.object_id}")