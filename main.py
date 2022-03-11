def parse_input(file_path):
    """
    Reads the input file from the path and extracts paint_code,
    capacity and profit arrays from it.
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


def solve_optimization(codes, cap, prof, max_limit=1000):
    """
    Generates the output for the optimization problem using
    a knapsack Dynamic programming approach
    :param codes: array of paint codes
    :param cap: array of capacity(ltrs)
    :param prof: array of profits
    :param max_limit: maximum constraint
    """
    tbl_tmp = [[0]*(max_limit + 1) for _ in range(len(cap))]
    for i in range(len(cap)-1):
        for j in range(max_limit+1):
            if cap[i] <= j:
                tbl_tmp[i][j] = max(
                    prof[i] + tbl_tmp[i - 1][j - cap[i]], tbl_tmp[i - 1][j]
                )
            else:
                tbl_tmp[i][j] = tbl_tmp[i-1][j]
    # retrieve solution from the table
    x = len(tbl_tmp) - 2
    y = len(tbl_tmp[0]) - 1
    result = []
    while x >= 0 and y >= 0:
        if tbl_tmp[x][y] == tbl_tmp[x - 1][y]:
            x -= 1
        else:
            result.append(x)
            y -= cap[x]
            x -= 1
    return [[res, codes[res]] for res in result[::-1]]


def write_output(output_file_path,
                 arr_cap,
                 arr_prof,
                 arr_codes,
                 max_limit=1000):
    """
    Writes the output of optimisation into the output
    location as .txt file.
    :param max_limit: max-limit of capacity
    :param output_file_path: output file path
    :param arr_cap: input array of capacity(ltrs)
    :param arr_prof: input array of profits
    :param arr_codes: array of paint codes
    """
    if arr_codes is None:
        output_string = "ERROR : EmptyInput - Please provide a valid input."
    else:
        # solve optimisation problem
        arr_opt_solution = solve_optimization(
            arr_codes, arr_cap, arr_prof, max_limit
        )

        cap_remaining = max_limit - sum(
            [arr_cap[i] for i in [i[0] for i in arr_opt_solution]]
        )
        total_profit = sum(
            [arr_prof[i] for i in [i[0] for i in arr_opt_solution]]
        )
        str_paint_codes = ",".join([code[1] for code in arr_opt_solution])
        if len(str_paint_codes) == 0:
            str_paint_codes = "No paints can be funded with given constraint."

        # generate output strings
        paints_to_fund = (
                "The paints that should be funded: " +
                str_paint_codes
        )
        str_total_profit = f"Total profit: {str(total_profit)}"
        str_capacity_remaining = f"Capacity remaining: {str(cap_remaining)}"
        output_string = (
                paints_to_fund + "\n" +
                str_total_profit + "\n" +
                str_capacity_remaining
        )

    # write to output file
    with open(output_file_path, "w") as fout:
        fout.write(output_string)
        fout.close()
    return None


if __name__ == '__main__':
    # initialize input path
    input_file_path = 'inputPS16.txt'

    # read and parse input data
    arr_paint_code, arr_capacity, arr_profit = parse_input(input_file_path)

    # run optimisation and write output into required path
    write_output('outputPS16.txt', arr_capacity, arr_profit, arr_paint_code, 1000)
