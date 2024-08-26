from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath

import os
import signal
import pandas as pd
import time
import subprocess
import shlex

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "1"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'experiments'"""
    results_output_path:        Path             = ROOT_DIR 

    """Experiment operation type. Unless you manually want to initiate each run, use `OperationType.AUTO`."""
    operation_type:             OperationType   = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes.
    This can be essential to accommodate for cooldown periods on some systems."""
    time_between_runs_in_ms:    int             = 60000


    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # e.g. Setting some variable based on some criteria
    def __init__(self):
        """Executes immediately after program start, on config load"""

        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN       , self.before_run       ),
            (RunnerEvents.START_RUN        , self.start_run        ),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT         , self.interact         ),
            (RunnerEvents.STOP_MEASUREMENT , self.stop_measurement ),
            (RunnerEvents.STOP_RUN         , self.stop_run         ),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT , self.after_experiment )
        ])
        self.run_table_model = None  # Initialized later
        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""
        sampling_factor = FactorModel("sampling", [200])
        llm = FactorModel("llm", ['chatgpt_temp_0.0', 'gpt-4_temp_0.0', 'deepseek-coder-33b-instruct_temp_0.0'])
        code = FactorModel("code", ['4', '61', '79', '63', '90', '53', '66', '52', '16'])
        self.run_table_model = RunTableModel(
            factors = [sampling_factor, llm, code],
            data_columns=['Time', 'TOTAL_DRAM_ENERGY (J)', 'TOTAL_PACKAGE_ENERGY (J)',
                          'TOTAL_PP0_ENERGY (J)', 
                          'TOTAL_MEMORY', 'TOTAL_SWAP',
                          'AVG_USED_MEMORY', 'AVG_USED_SWAP', 
                          'TOTAL_ENERGY (J)'],
            repetitions=21,
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""
        pass

    def before_run(self) -> None:
        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""
        
        git_log = open(f'./{self.name}/git_log.log', 'a')
        subprocess.call('git add --all && git commit -m "Experiment checkpoint" && git push',
                        shell=True, stdout=git_log, stderr=git_log)


    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""
        pass

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        sampling_interval = context.run_variation['sampling']
        llm = context.run_variation['llm']
        code = context.run_variation['code']

        profiler_cmd = f'sudo energibridge \
                        --interval {sampling_interval} \
                        --output {context.run_dir / "energibridge.csv"} \
                        --summary \
                        python3 ./code/{llm}/{code}.py'

        #time.sleep(1) # allow the process to run a little before measuring
        energibridge_log = open(f'{context.run_dir}/energibridge.log', 'w')
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd), stdout=energibridge_log)

    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""

        # No interaction. We just run it for XX seconds.
        # Another example would be to wait for the target to finish, e.g. via `self.target.wait()`
        pass

    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        self.profiler.wait()

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""
        pass
    
    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""

        # energibridge.csv - Power consumption
        df = pd.read_csv(context.run_dir / "energibridge.csv")
        with open(context.run_dir / "energibridge.log", 'r') as reader:
            contents = reader.read()
        
        time = contents.split('for ')[1]
        time = time.split(' sec')[0]
        energy = contents.split('joules: ')[1]
        energy = energy.split(' for ')[0]

        if time:
            total_time = float(time)
        else:
            total_time = -1

        if energy:
            total_energy = float(energy)
        else:
            total_energy = -1

        run_data = {
                'Time'                        : round(total_time, 3),
                'TOTAL_DRAM_ENERGY (J)'       : round(df['DRAM_ENERGY (J)'].sum(), 3),
                'TOTAL_PACKAGE_ENERGY (J)'    : round(df['PACKAGE_ENERGY (J)'].sum(), 3),
                'TOTAL_PP0_ENERGY (J)'        : round(df['PP0_ENERGY (J)'].sum(), 3),
                'TOTAL_MEMORY'                : round(df['TOTAL_MEMORY'].mean() if df['TOTAL_MEMORY'].std() == 0 else -1, 3),
                'TOTAL_SWAP'                  : round(df['TOTAL_SWAP'].mean() if df['TOTAL_SWAP'].std() == 0 else -1, 3),
                'AVG_USED_MEMORY'             : round(df['USED_MEMORY'].mean(), 3),
                'AVG_USED_SWAP'               : round(df['USED_SWAP'].mean(), 3),
                'TOTAL_ENERGY (J)'            : round(total_energy, 3),
        }
        return run_data

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""
        pass

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
