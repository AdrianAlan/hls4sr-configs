import argparse
import hls4ml
import json
import os
import sympy
import subprocess


def main(part, precision):
    complexity_of_operators = {}
    with open('ops.json') as f:
        data = json.load(f)
        for key, val in data['binary'].items():
            equation = val.replace("x", "x0").replace("y", "x1")
            expression = sympy.parsing.sympy_parser.parse_expr(equation)
            hls_model = hls4ml.converters.convert_from_symbolic_expression(
                expression,
                n_symbols=2,
                output_dir='tmp_test',
                precision=precision,
                part=part
            )
            hls_model.write()
            process = subprocess.run(
                ["vivado_hls",
                 "-f",
                 "build_prj.tcl",
                 "\"reset=1 synth=1 csim=0 cosim=0 validation=0 export=0\""],
                cwd='tmp_test')
            result = subprocess.check_output(
                ["awk",
                 "NR==32",
                 "myproject_prj/solution1/syn/report/myproject_csynth.rpt"],
                cwd='tmp_test')
            cc = result.decode("utf-8").replace(" ", "").split("|")[1]
            complexity_of_operators[key] = int(cc)
        for key, val in data['unary'].items():
            equation = val.replace('sympy.', '')
            if 'x' in equation and key != 'exp':
                equation = equation.replace("x", "x0")
            else:
                equation += '(x0)'
            expression = sympy.parsing.sympy_parser.parse_expr(equation)
            hls_model = hls4ml.converters.convert_from_symbolic_expression(
                expression,
                n_symbols=1,
                output_dir='tmp_test',
                precision=precision,
                part=part
            )
            hls_model.write()
            process = subprocess.run(
                ["vivado_hls",
                 "-f",
                 "build_prj.tcl",
                 "\"reset=1 synth=1 csim=0 cosim=0 validation=0 export=0\""],
                cwd='tmp_test')
            result = subprocess.check_output(
                ["awk",
                 "NR==32",
                 "myproject_prj/solution1/syn/report/myproject_csynth.rpt"],
                cwd='tmp_test')
            cc = result.decode("utf-8").replace(" ", "").split("|")[1]
            complexity_of_operators[key] = int(cc)

    config = {}
    config['part'] = part
    config['precision'] = precision
    config['complexity_of_operators'] = complexity_of_operators

    os.makedirs('configs/{part}/{precision}'.format(
        part=part,
        precision=precision)
    )
    with open('configs/{part}/{precision}/config.json'.format(
        part=part,
        precision=precision
    ), 'w') as outfile:
        json.dump(config, outfile)


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Generate SR configs for hls4ml')
    parser.add_argument(
        '--part',
        type=str,
        help='Part name',
        default='xcvu9p-flga2577-2-e'
    )
    parser.add_argument(
        '--precision',
        type=str,
        help='Precision setting',
        default='ap_fixed<12, 6>'
    )
    args = parser.parse_args()

    main(args.part, args.precision)
