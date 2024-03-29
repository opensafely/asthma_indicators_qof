import argparse
import pathlib
import re
import glob

import pandas

MEASURE_FNAME_REGEX = re.compile(r"measure_ast007_(?P<id>\S+)\.csv")


def _check_for_practice(table):
    if "practice" in table.category.values:
        raise (
            AssertionError("Practice-level data should not be in final output")
        )


def _reshape_data(measure_table):
    try:
        assert len(measure_table.columns) < 6
    except AssertionError:
        raise (
            AssertionError("This script only supports one group_by category")
        )
    if measure_table.date[0] != measure_table.date[1]:
        # if sequential rows have different dates, then an individual date's
        # data has not been subdivided by category, and we can assume that
        # group_by = "population"
        # Therefore, the numerator and denominator will be the first columns
        numerator = measure_table.columns[0]
        denominator = measure_table.columns[1]
        measure_table["category"] = "population"
        measure_table["group"] = "population"
        group_by = None
        measure_table["name"] = measure_table.attrs["id"]

    else:
        denominator = measure_table.columns[-3]
        numerator = measure_table.columns[-4]
        group_by = measure_table.columns[-5]
        measure_table["category"] = group_by
        measure_table["name"] = measure_table.attrs["id"]

    measure_table.rename(
        columns={
            numerator: "numerator",
            denominator: "denominator",
            group_by: "group",
        },
        inplace=True,
    )
    # Assume we only need the numerator and the denominator
    measure_table.drop(columns=["population"], inplace=True, errors="ignore")
    return measure_table


def _join_tables(tables):
    return pandas.concat(tables)


def get_measure_tables(input_files):
    for input_file in input_files:
        measure_fname_match = re.match(MEASURE_FNAME_REGEX, input_file.name)
        print(input_file, measure_fname_match)
        if measure_fname_match is not None:
            # The `date` column is assigned by the measures framework.
            measure_table = pandas.read_csv(input_file, parse_dates=["date"])

            # We can reconstruct the parameters passed to `Measure` without
            # the study definition.
            measure_table.attrs["id"] = measure_fname_match.group("id")
            yield measure_table


def _round_table(measure_table, round_to):
    def custom_round(x, base):
        return int(base * round(float(x) / base))

    measure_table.numerator = measure_table.numerator.apply(
        lambda x: custom_round(x, round_to) if pandas.notnull(x) else x
    )
    measure_table.denominator = measure_table.denominator.apply(
        lambda x: custom_round(x, round_to) if pandas.notnull(x) else x
    )
    # recompute value
    measure_table.value = (measure_table.numerator /
                           measure_table.denominator)
    return measure_table


def write_table(measure_table, path, filename):
    create_dir(path)
    measure_table.to_csv(path / filename, index=False, header=True)


def create_dir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def get_path(*args):
    return pathlib.Path(*args).resolve()


def match_input(input_list):
    path = get_path(input_list)
    if path.exists():
        return path


def match_paths(pattern):
    return [get_path(x) for x in glob.glob(pattern)]


def parse_args():
    parser = argparse.ArgumentParser()
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input-files",
        required=False,
        type=match_paths,
        help="Glob pattern for matching one or more input files",
    )
    input_group.add_argument(
        "--input-list",
        required=False,
        type=match_input,
        action="append",
        help="Manually provide a list of one or more input files",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=pathlib.Path,
        help="Path to the output directory",
    )
    parser.add_argument(
        "--output-name",
        required=True,
        help="Name for joined measures file",
    )
    parser.add_argument(
        "--round-to",
        required=False,
        default=10,
        type=int,
        help="Round to the nearest",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_files = args.input_files
    input_list = args.input_list
    output_dir = args.output_dir
    output_name = args.output_name
    round_to = args.round_to

    if not input_files and not input_list:
        raise FileNotFoundError("No files matched the input pattern provided")

    tables = []
    for measure_table in get_measure_tables(input_list or input_files):
        table = _reshape_data(measure_table)
        rounded = _round_table(table, round_to)
        tables.append(rounded)

    output = _join_tables(tables)
    _check_for_practice(output)
    write_table(output, output_dir, output_name)


if __name__ == "__main__":
    main()
