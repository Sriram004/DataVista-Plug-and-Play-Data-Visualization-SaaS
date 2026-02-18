from app.services.query_service import QueryService


def test_aggregate_sum() -> None:
    rows = [
        {"region": "APAC", "sales": 10},
        {"region": "APAC", "sales": 15},
        {"region": "EMEA", "sales": 5},
    ]

    out = QueryService.aggregate(rows, "region", "sales", "sum")
    assert {item["region"]: item["sum_sales"] for item in out} == {"APAC": 25.0, "EMEA": 5.0}
