from collections import defaultdict


class QueryService:
    @staticmethod
    def aggregate(records: list[dict], group_by: str, metric: str, op: str) -> list[dict]:
        buckets: dict[str, list[float]] = defaultdict(list)
        for row in records:
            buckets[str(row[group_by])].append(float(row.get(metric, 0) or 0))

        output = []
        for key, values in buckets.items():
            if op == "sum":
                value = sum(values)
            elif op == "avg":
                value = sum(values) / len(values)
            else:
                value = len(values)
            output.append({group_by: key, f"{op}_{metric}": value})
        return output
