#!/usr/bin/env bash

configdir="${PROJECT_ROOT}/.config"
cachedir="${PROJECT_ROOT}/.cache"
scriptbin="${PROJECT_ROOT}/.script-bin"

localbin="/usr/local/bin"
locallib="/usr/local/lib"
localopt="/usr/local/opt"

function CLU_python_module_run () {
    # Usage:
    # $ python_module_run python3 bpython  --config=path/to/config ...
    # $ python_module_run python3 IPython  --config=path/to/config ...
    # $ python_module_run python3 ptpython --config-dir=path/to/config-dir ...
    # $ python_module_run python2 bpython  --config=path/to/config.py2 ...
    # … Issuing one of the above commands will first ensure that:
    #  [a] `python3` is an available executable on the current PATH,
    #  [b] `~/.script-bin/repl-bpython.py` is a readable file, and
    #  [c] ${pythonpath} contains '~/.script-bin' and $PWD, as well as
    #       anything from any existing $PYTHONPATH variable
    # … If all of these conditions are met, it will assemble a command:
    # $ PYTHONPATH=$pythonpath $executable -m $module $config -i $replenv $@
    # … using the arguments it was passed and its environment to populate
    #   the variables from which this command is built. Ultimately this will
    #   execute a Python REPL (read-evaluate-print-loop) interpreter that
    #   exposes an interactive Python environment.
    # N.B.: Users will generally not execute `python_module_run` themselves;
    #   see below for examples of functions that set up arguments to a specific
    #  `python_module_run` command and then execute that.
    # set -x
    executable="${1:?- [ERROR] Python interpreter expected}"
    modulename="${2:?- [ERROR] Python module name expected}"
    configflag="${3:?- [ERROR] REPL configuration expected}"
    replenv="${PROJECT_SCRIPTS}/repl-${modulename,,}.py"
    shift 3 # restore the original $@ argument-set
    if [[ ! -e $executable ]]; then
        executable="$(which ${executable})"
    fi
    if [[ ! -x $executable ]]; then
        echo "» [ERROR] bad Python interpreter: ${executable}"
        return 1
    fi
    if [[ ! -r $replenv ]]; then
        echo "» [ERROR] unknown REPL env setup: ${replenv}"
        return 1
    fi
    if [[ $PYTHONPATH ]]; then
        pythonpath="${PYTHONPATH}"
    else
        pythonpath="${PROJECT_SITE}:${PROJECT_BASE}:${PROJECT_MODULE}:${scriptbin}:${PROJECT_SCRIPTS}"
    fi
    PYTHONPATH=${pythonpath} ${executable} -m ${modulename} \
                                              ${configflag} \
                                           -i ${replenv} $@
    # set +x
}

function CLU_bpy3 () {
    # set -x
    pyversion="3"
    pyname="python${pyversion}"
    modname="bpython"
    config="${configdir}/${modname}/config.py${pyversion}"
    CLU_python_module_run $pyname $modname --config=${config} $@
    # set +x
}

alias bpy="CLU_bpy3"

