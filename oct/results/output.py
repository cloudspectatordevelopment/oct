from __future__ import print_function

import os
import time
from jinja2 import Environment, FileSystemLoader

from oct.results import graphs
from oct.results.report import ReportResults
from oct.results.writer import ReportWriter


def output(results_dir, config, parent='../../'):
    """Write the results output for the given test

    :param str results_dir: the directory for the results
    :param dict config: the configuration of the test
    :param str parents: the parent directory
    """
    start = time.time()
    print("Compiling results...")
    results_dir = os.path.abspath(results_dir)
    results = ReportResults(config['run_time'], config['results_ts_interval'])
    results.compile_results()
    print("Results compiled in {} seconds\n".format(time.time() - start))

    if results.total_transactions == 0:
        print("No results, cannot create report")
        return False

    print('transactions: %i' % results.total_transactions)
    print('timers: %i' % results.total_timers)
    print('errors: %i' % results.total_errors)
    print('test start: %s' % results.start_datetime)
    print('test finish: %s\n' % results.finish_datetime)

    data = {
        'report': results,
        'run_time': config['run_time'],
        'ts_interval': config['results_ts_interval'],
        'turrets_config': results.turrets,
        'all_results': {"all": results.main_results, "timers": results.timers_results}
    }

    print("Generating graphs...")
    partial = time.time()
    graphs.resp_graph_raw(results.main_results['raw'], 'All_Transactions_response_times.svg', results_dir)
    graphs.resp_graph(results.main_results['compiled'], 'All_Transactions_response_times_intervals.svg', results_dir)
    graphs.tp_graph(results.main_results['compiled'], 'All_Transactions_throughput.svg', results_dir)

    for key, value in results.timers_results.items():
        graphs.resp_graph_raw(value['raw'], key + '_response_times.svg', results_dir)
        graphs.resp_graph(value['compiled'], key + '_response_times_intervals.svg', results_dir)
        graphs.tp_graph(value['compiled'], key + '_throughput.svg', results_dir)
    print("All graphs generated in {} seconds\n".format(time.time() - partial))

    print("Generating html report...")
    partial = time.time()
    j_env = Environment(loader=FileSystemLoader(os.path.join(results_dir, parent, 'templates')))
    template = j_env.get_template('report.html')

    report_writer = ReportWriter(results_dir, parent)
    report_writer.write_report(template.render(data))
    print("HTML report generated in {} seconds\n".format(time.time() - partial))
    print("Full report generated in {} seconds".format(time.time() - start))
    return True