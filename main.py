import csv


def read_src_data(filename):
    with open(filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=";")
        next(csv_reader)
        data = list(csv_reader)
    return data


# print(colnames, data)
data = read_src_data("Corp_Summary.csv")
deps = {}
for row in data:
    try:
        deps[row[1]].add(row[2])
    except KeyError:
        deps[row[1]] = {row[2]}
# print(deps)


# add sorting to deps and teams
def vis_dep_hierarchy(deps=deps):
    for dep, teams in deps.items():
        print(dep)
        print("\t" + "\n\t".join(teams))
    return  # return an actual string


# print(vis_dep_hierarchy(deps))


def get_row_stats(data=data):
    dep_stats_raw = {}
    for row in data:
        try:
            dep_stats_raw[row[1]]["employee"] += 1
        except KeyError:
            dep_stats_raw[row[1]] = {}
            dep_stats_raw[row[1]]["employee"] = 1
        try:
            dep_stats_raw[row[1]]["salary"].append(float(row[5]))
        except KeyError:
            dep_stats_raw[row[1]]["salary"] = [float(row[5])]
    return dep_stats_raw


raw_stats = get_row_stats(data)
print(raw_stats)


def get_data_out(dep_stats_raw=raw_stats):
    data_out = []
    for dep, stats in dep_stats_raw.items():
        print(dep)
        print("\t", stats["employee"])
        slry = stats["salary"]
        min_slry = min(slry)
        max_slry = max(slry)
        mean_slry = round(sum(slry) / len(slry), 2)
        data_out.append((dep, stats["employee"], min_slry, max_slry, mean_slry))
        print(f"\t {min_slry:.0f} {mean_slry:.2f} {max_slry:.0f}")
    return data_out


data_out = get_data_out(raw_stats)
print(data_out)


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
            row = ";".join([str(i) for i in row]) + "\n"
            f.write(row)


def menu():
    available_options = [1, 2, 3]
    while (choice := input("What s ur option, brother")) not in map(
        str, available_options
    ):
        ...
    option_to_func = dict(enumerate([vis_dep_hierarchy, get_data_out, write_csv_dep]))
    print(option_to_func, choice)
    print(option_to_func[int(choice) - 1]())


# menu()
