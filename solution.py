def parse_input(file_path):
    """
    Reads the input file from the path and extracts paint_code,
    capacity and profit lists from it.
    :param file_path: path of input file
    """
    with open(file_path, 'r') as fi:
        input_file_read = fi.read()
    if len(input_file_read) == 0:
        return None, None, None
    else:
        input_line_split = input_file_read.split("\n")
        # initialize required arrays
        paint_code = []
        capacity = []
        profit = []
        # loop across the lines of the file
        for i in input_line_split:
            each_split = i.replace("/", " ").split()
            paint_code.append(each_split[0])
            capacity.append(int(each_split[1]))
            profit.append(int(each_split[2]))
        return paint_code, capacity, profit


def run_optimisation(
        codes,
        capacity,
        profit,
        max_limit=1000,
):
    """
    Runs and solves the paint code optimisation problem
    using recursive Dynamic programming approach with
    Memoization using a helper function.
    :param codes: list of paint codes
    :param capacity: list of corresponding capacities
    :param profit: list of corresponding profits
    :param max_limit: maximum capacity(ltrs)
    """
    # defining helper function to run recursion
    def optimiser_func(max_cap, list_cap, list_prof, n):
        """
        Helper function to implement recursion with memoization
        :param max_cap: maximum capacity(ltrs)
        :param list_cap: list of capacities
        :param list_prof: list of profits
        :param n: number of items
        """
        # define base cases
        if n == 0 or max_cap == 0:
            return 0
        if tmp_table[n][max_cap] != 0:
            return tmp_table[n][max_cap]
        if list_cap[n - 1] <= max_cap:
            tmp_table[n][max_cap] = max(
                list_prof[n - 1] + optimiser_func(
                    max_cap - list_cap[n - 1], list_cap, list_prof, n - 1
                ),
                optimiser_func(max_cap, list_cap, list_prof, n - 1)
            )
            return tmp_table[n][max_cap]
        elif list_cap[n - 1] > max_cap:
            tmp_table[n][max_cap] = optimiser_func(
                max_cap, list_cap, list_prof, n - 1
            )
            return tmp_table[n][max_cap]

    # Check if lists are non-empty
    if codes is None:
        output_string = "ERROR : EmptyInput - Please provide a valid input."
        return output_string

    # trigger the recursion
    num_of_paints = len(codes)
    tmp_table = [
        [0 for _ in range(max_limit + 1)] for _ in range(num_of_paints + 1)
    ]
    optimised_profit = optimiser_func(max_limit, capacity, profit, num_of_paints)

    # retrieve solution from the temp table
    list_result = []
    tmp_limit = max_limit
    tmp_profit = optimised_profit
    for i in range(num_of_paints, 0, -1):
        if tmp_profit <= 0:
            break
        if tmp_profit == tmp_table[i - 1][tmp_limit]:
            continue
        else:
            list_result.append(codes[i - 1])
            tmp_profit = tmp_profit - profit[i - 1]
            tmp_limit = tmp_limit - capacity[i - 1]

    # Formatting the output strings
    result_paint_codes = [res for res in list_result[::-1]]
    str_paint_codes = ",".join(result_paint_codes)
    if len(str_paint_codes) == 0:
        str_paint_codes = "No paints can be funded with given constraint."
        # generate output strings
    paints_to_fund = (
            "The paints that should be funded: " +
            str_paint_codes
    )
    str_total_profit = f"Total profit: {str(optimised_profit)}"
    str_capacity_remaining = f"Capacity remaining: {str(tmp_limit)}"
    output_string = (
            paints_to_fund + "\n" +
            str_total_profit + "\n" +
            str_capacity_remaining
    )
    return output_string


def write_output(file_path, out_str):
    """
    Writes the provided string inputs into a file
    specified by the path.
    :param file_path: output file path
    :param out_str: string to be written to the file
    """
    with open(file_path, "w") as fout:
        fout.write(out_str)
        fout.close()
    return None


if __name__ == '__main__':
    # define parameters
    input_file_path = 'inputPS16.txt'
    output_file_path = 'outputPS16.txt'

    # read and parse input data
    input_paint_code, input_capacity, input_profit = parse_input(input_file_path)

    # run optimisation and produce required results
    output = run_optimisation(input_paint_code, input_capacity, input_profit, 1000)

    # write output into required path
    write_output(output_file_path, output)

