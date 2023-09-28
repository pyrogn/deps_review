from collections import defaultdict, namedtuple
from dataclasses import dataclass, field


def read_src_data(filename):
    data = []
    DataRow = namedtuple("DataRow", ["fio", "dep", "team", "title", "mark", "salary"])
    with open(filename) as f:
        _ = f.readline()  # skip colnames
        for row in f.readlines():
            row = row.strip().split(";")
            row = DataRow(*row)
            data.append(row)
    return data


data = read_src_data("Corp_Summary.csv")


def vis_dep_hierarchy(data=data):
    deps = defaultdict(set)
    for row in data:
        deps[row.dep].add(row.team)
    deps_sorted = {}
    for dep, team in dict(sorted(deps.items())).items():
        deps_sorted[dep] = sorted(team)
    string_out = []
    for dep, teams in deps_sorted.items():
        string_out.extend([dep, "\t" + "\n\t".join(teams)])
    return "\n".join(string_out)  # return an actual string


print(vis_dep_hierarchy(data))


@dataclass
class DepStats:
    employee_cnt: int = 0
    salary_list: list[float] = field(default_factory=list)


def get_data_for_stats(data=data):
    dep_stats_raw = defaultdict(DepStats)
    for row in data:
        dep_stats_raw[row.dep].employee_cnt += 1
        dep_stats_raw[row.dep].salary_list.append(float(row[5]))
    return dep_stats_raw


raw_stats = get_data_for_stats(data)
print(raw_stats)


def get_data_out(dep_stats_raw=raw_stats):
    data_out = []
    for dep, stats in dep_stats_raw.items():
        print(dep)
        print("\t", stats.employee_cnt)
        slry = stats.salary_list
        min_slry = min(slry)
        max_slry = max(slry)
        mean_slry = round(sum(slry) / len(slry), 2)
        data_out.append((dep, stats.employee_cnt, min_slry, max_slry, mean_slry))
        print(f"\t {min_slry:.0f} {mean_slry:.2f} {max_slry:.0f}")
    return data_out


data_out = get_data_out(raw_stats)
# print(data_out)


def write_csv_dep(data_out=data_out):
    with open("out.csv", "w") as f:
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


def menu():
    available_options = [1, 2, 3]
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
