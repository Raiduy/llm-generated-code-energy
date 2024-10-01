from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import os
import requests
import subprocess
import shlex
import time

SERVER_HOST = '192.168.0.103:5000'

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "1"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'experiments'"""
    results_output_path:        Path            = ROOT_DIR / 'experiments'

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

        #llm = FactorModel("llm", ['code-millenials-34b_temp_0.0', 'speechless-codellama-34b_temp_0.0', 'wizardcoder-33b-1.1_temp_0.0'])
        llm = FactorModel("llm", ['chatgpt_temp_0.0', 'gpt-4_temp_0.0', 'deepseek-coder-33b-instruct_temp_0.0'])
        code = FactorModel("code", ['4', '61', '79', '63', '90', '53', '66', '52', '16'])
        self.run_table_model = RunTableModel(
            factors = [llm, code],
            repetitions=21,
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""

        output.console_log("Config.before_experiment() called!")

    def before_run(self) -> None:
        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""

        output.console_log("Config.before_run() called!")

        git_log = open(f'./experiments/{self.name}/git_log.log', 'a')
        subprocess.call('git add --all && git commit -m "Experiment checkpoint" && git push',
                        shell=True, stdout=git_log, stderr=git_log)

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""

        output.console_log("Config.start_run() called!")
        
        llm = context.run_variation['llm']
        code = context.run_variation['code']

        profiler_cmd = f'python3 ./code/{llm}/{code}.py'

        #time.sleep(1) # allow the process to run a little before measuring
        self.target = subprocess.Popen(shlex.split(profiler_cmd))

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        output.console_log("Starting measurement on the dev computer...")

        llm = context.run_variation['llm']
        code = context.run_variation['code']

        output.console_log(f'LLM: {llm}')
        output.console_log(f'CODE: {code}')

        dev_pc_filename = str(context.run_dir).split(f'/')[-1]

        res = requests.post(f'http://{SERVER_HOST}/start/{dev_pc_filename}', json={}, headers={'Content-Type': 'application/json'})
        output.console_log(res.text)

        self.profiler = subprocess.Popen(['sar', '-A', '-o', context.run_dir / "sar_log.file", '1', '800'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.ROOT_DIR,
        )

        output.console_log("Config.start_measurement() called!")
        time.sleep(1) # allow the process to run a little before measuring


    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""
        self.target.wait()


    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        output.console_log("Stopping measurement on the dev computer...")

        self.profiler.kill()
        res = requests.post(f'http://{SERVER_HOST}/stop', json={}, headers={'Content-Type': 'application/json'})
        output.console_log(res.text)

        output.console_log("Config.stop_measurement called!")

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""

        output.console_log("Config.stop_run() called!")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""

        output.console_log("Config.populate_run_data() called!")
        return None

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""

        git_log = open(f'./experiments/{self.name}/git_log.log', 'a')
        subprocess.call('git add --all && git commit -m "Experiment checkpoint" && git push',
                        shell=True, stdout=git_log, stderr=git_log)


        output.console_log("Config.after_experiment() called!")

        git_log = open(f'./{self.name}/git_log.log', 'a')
        subprocess.call('git add --all && git commit -m "Experiment finished" && git push',
                        shell=True, stdout=git_log, stderr=git_log)

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
