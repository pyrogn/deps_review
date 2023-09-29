from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple


class DataRow(NamedTuple):
    dep: str
    team: str
    salary: float


def parse_data_row(row) -> DataRow:
    idx_to_read = [1, 2, 5]  # dep, team, salary
    row = row.strip().split(";")
    row = [row[idx] for idx in idx_to_read]
    row[2] = float(row[2])  # convert salary to float
    return DataRow(*row)


def read_src_data(filename: str) -> list[DataRow]:
    data = []
    with Path(filename).open() as f:
        _ = f.readline()  # skip colnames
        for row in f.readlines():
            data.append(parse_data_row(row))
    return data


data = read_src_data("Corp_Summary.csv")


def sort_dep_teams(data=data):
    deps = defaultdict(set)
    for row in data:
        deps[row.dep].add(row.team)
    deps_sorted = {}
    for dep, team in dict(sorted(deps.items())).items():
        deps_sorted[dep] = sorted(team)
    return deps_sorted


def vis_dep_hierarchy(data=data):
    deps = sort_dep_teams(data)
    string_out = []
    for dep, teams in deps.items():
        string_out.extend([dep, "\t" + "\n\t".join(teams)])
    return "\n".join(string_out)  # return an actual string


print(vis_dep_hierarchy(data))


@dataclass
class DepStatsRaw:
    employee_cnt: int = 0
    salary_list: list[float] = field(default_factory=list)


def get_data_for_stats(data=data) -> defaultdict[str, DepStatsRaw]:
    dep_stats_raw: defaultdict[str, DepStatsRaw] = defaultdict(DepStatsRaw)
    for row in data:
        dep_stats_raw[row.dep].employee_cnt += 1
        dep_stats_raw[row.dep].salary_list.append(float(row.salary))
    return dep_stats_raw


raw_stats = get_data_for_stats(data)


# print(raw_stats)
def sort_dict(dikt):
    return dict(sorted(dikt.items()))


class DepStats(NamedTuple):
    dep: str
    employee_cnt: int
    min_slry: float
    max_slry: float
    mean_slry: float


def get_data_out(dep_stats_raw=raw_stats):
    data_out = []
    for dep, stats in sort_dict(dep_stats_raw).items():
        slry = stats.salary_list
        min_slry = min(slry)
        max_slry = max(slry)
        mean_slry = round(sum(slry) / len(slry), 2)
        data_out.append(
            DepStats(dep, stats.employee_cnt, min_slry, max_slry, mean_slry)
        )
    return data_out


def get_deps_stats_pretty(stats: list[DepStats]):
    string_out = []
    for dep_stat in stats:
        string_out.append(
            f"{dep_stat.dep}\n"
            f"\t{dep_stat.employee_cnt} {dep_stat.min_slry} {dep_stat.max_slry} {dep_stat.mean_slry}"
        )
    return "\n".join(string_out)


data_out = get_data_out(raw_stats)
print(get_deps_stats_pretty(data_out))


def write_csv_dep(data_out=data_out):
    with Path("out.csv").open("w") as f:
        headers = [
            "dep_name",
            "employee_cnt",
            "min_salary",
            "max_salary",
            "mean_salary",
        ]
        f.write(";".join(headers) + "\n")
        for row in data_out:
            row = ";".join(map(str, row)) + "\n"
            f.write(row)


def menu() -> None:
    available_options = {
        1: "Print deps and teams",
        2: "Get stats on deps with cnt employees and salary",
        3: "Write stats on deps",
    }
    print("\n".join(f"{num}. {command}" for num, command in available_options.items()))
    while True:
        try:
            choice = int(input("What's ur option, brother: "))
            if choice not in available_options:
                print("Enter a valid number of command")
            else:
                idx_choose = choice - 1
                break
        except ValueError:
            print("Enter a number from 1 to 3")
    #     might want to add else block if choice is successful

    ordered_options = [vis_dep_hierarchy, get_data_out, write_csv_dep]
    option_to_func = dict(enumerate(ordered_options))
    print(option_to_func[idx_choose]())


if __name__ == "__main__":
    pass
    # menu()
