from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple, Callable, Any


class DataRow(NamedTuple):
    dep: str
    team: str
    salary: float


def parse_data_row(row: str) -> DataRow:
    """Read row and transform to NamedTuple with required attrs"""
    idx_to_read = [1, 2, 5]  # dep, team, salary
    row_list = row.strip().split(";")
    filtered_row: list = [row_list[idx] for idx in idx_to_read]
    filtered_row[2] = float(filtered_row[2])
    return DataRow(*filtered_row)


def read_src_data(filename: str) -> list[DataRow]:
    """Read source file and as list of DataRow"""
    data = []
    with Path(filename).open() as f:
        _ = f.readline()  # skip colnames
        for row in f.readlines():
            data.append(parse_data_row(row))
    return data


data = read_src_data("Corp_Summary.csv")

DepName = str
TeamName = str


def sort_dict_by_key(dikt: dict) -> dict:
    """Sort a dictionary by keys"""
    return dict(sorted(dikt.items()))


def sort_dep_teams(data: list[DataRow] = data) -> dict[DepName, list[TeamName]]:
    """Read data and return dictionary with department and its team, sorted"""
    deps = defaultdict(set)
    for row in data:
        deps[row.dep].add(row.team)
    deps_sorted = {}
    for dep, team in sort_dict_by_key(deps).items():
        deps_sorted[dep] = sorted(team)
    return deps_sorted


def get_deps_hierarchy(data: list[DataRow] = data) -> str:
    """Get department hierarchy as formatted string"""
    deps = sort_dep_teams(data)
    string_out = []
    for dep, teams in deps.items():
        string_out.extend([dep, "\t" + "\n\t".join(teams)])
    return "\n".join(string_out)


@dataclass
class DepStatsRaw:
    """Raw stats of department"""

    employee_cnt: int = 0
    salary_list: list[float] = field(default_factory=list)


def get_data_for_stats(data=data) -> dict[DepName, DepStatsRaw]:
    """Get raw stats for departments"""
    dep_stats_raw: defaultdict[str, DepStatsRaw] = defaultdict(DepStatsRaw)
    for row in data:
        dep_stats_raw[row.dep].employee_cnt += 1
        dep_stats_raw[row.dep].salary_list.append(float(row.salary))
    return dep_stats_raw


raw_stats = get_data_for_stats(data)


class DepStats(NamedTuple):
    """Clean stats of department"""

    dep: str
    employee_cnt: int
    min_slry: float
    max_slry: float
    mean_slry: float


def get_clean_stats(
    dep_stats_raw: dict[DepName, DepStatsRaw] = raw_stats
) -> list[DepStats]:
    """Get clean stats of departments"""
    data_out = []
    for dep, stats in sort_dict_by_key(dep_stats_raw).items():
        slry = stats.salary_list
        min_slry = min(slry)
        max_slry = max(slry)
        mean_slry = round(sum(slry) / len(slry), 2)
        data_out.append(
            DepStats(dep, stats.employee_cnt, min_slry, max_slry, mean_slry)
        )
    return data_out


dep_stats = get_clean_stats(raw_stats)


def get_deps_stats_pretty(stats: list[DepStats] = dep_stats) -> str:
    """Make clean stats of departments as formatted string"""
    string_out = []
    for dep_stat in stats:
        string_out.append(
            f"{dep_stat.dep}\n"
            f"\tEmployee count: {dep_stat.employee_cnt:.0f}\n\t"
            f"Mean salary: {dep_stat.mean_slry:.2f} "
            f"(min={dep_stat.min_slry:.2f}, max={dep_stat.max_slry:.2f})"
        )
    return "\n".join(string_out)


def write_csv_dep(
    dep_stats: list[DepStats] = dep_stats, filename: str = "clean_stats_deps.csv"
) -> str:
    """Write clean Departments stats to CSV file"""
    with Path(filename).open("w") as f:
        headers = [
            "dep_name",
            "employee_cnt",
            "min_salary",
            "max_salary",
            "mean_salary",
        ]
        f.write(";".join(headers) + "\n")
        for row in dep_stats:
            str_row = ";".join(map(str, row)) + "\n"
            f.write(str_row)
        return f"Saved as {Path(filename)}"


def menu() -> None:
    """Choose available action and get results"""

    available_options = {
        1: "Print deps and teams",
        2: "Get stats on deps with cnt employees and salary",
        3: "Write stats on deps",
    }
    str_options = "\n".join(
        f"{num}. {command}" for num, command in available_options.items()
    )
    print(str_options)

    while True:
        try:
            choice = int(input("What's ur option, brother: "))
            if choice not in available_options:
                raise ValueError
        except ValueError:
            print("Enter a number from 1 to 3")
        else:
            break

    ordered_funcs_as_options = [
        get_deps_hierarchy,
        get_deps_stats_pretty,
        write_csv_dep,
    ]
    option_to_func = dict(enumerate(ordered_funcs_as_options, start=1))
    result: str = option_to_func[choice]()
    print(result)


if __name__ == "__main__":
    menu()
