#!/usr/bin/env bash

# Autohook
# A very, very small Git hook manager with focus on automation
# 
# Author:   Nik Kantar <http://nkantar.com>
# Version:  2.1.2
# Website:  https://github.com/nkantar/Autohook
# 
# Addition of “post-push” hook by Alexander Bôhn <http://github.com/fish2000>

echo() {
    builtin echo "[Autohook] $@";
}

install() {
    hook_types=(
        "applypatch-msg"
        "commit-msg"
        "post-applypatch"
        "post-checkout"
        "post-commit"
        "post-merge"
        "post-push"
        "post-receive"
        "post-rewrite"
        "post-update"
        "pre-applypatch"
        "pre-auto-gc"
        "pre-commit"
        "pre-push"
        "pre-rebase"
        "pre-receive"
        "prepare-commit-msg"
        "update"
    )
    
    repo_root=$(git rev-parse --show-toplevel)
    hooks_dir="${repo_root}/.git/hooks"
    autohook_linktarget="../../hooks/autohook.sh"
    
    for hook_type in "${hook_types[@]}"; do
        hook_symlink="${hooks_dir}/${hook_type}"
        ln -s $autohook_linktarget $hook_symlink
    done
}

main() {
    calling_file=$(basename $0)
    debug=${AUTOHOOK_DEBUG:-0}
    silent=${AUTOHOOK_SILENT:-0}
    
    if [[ $calling_file == "autohook.sh" ]]; then
        command=$1
        if [[ $command == "install" ]]; then
            install
        fi
    else
        repo_root=$(git rev-parse --show-toplevel)
        hook_type=$calling_file
        symlinks_dir="${repo_root}/hooks/${hook_type}"
        files=("${symlinks_dir}"/*)
        number_of_symlinks="${#files[@]}"
        
        if [[ $number_of_symlinks == 1 ]]; then
            if [[ "$(basename ${files[0]})" == "*" ]]; then
                number_of_symlinks=0
            fi
        fi
        
        if (( $debug )); then
            echo "Running ${number_of_symlinks} scripts for hook: ${hook_type}"
        fi
        
        if [[ $number_of_symlinks -gt 0 ]]; then
            hook_exit_code=0
            
            for file in "${files[@]}"; do
                scriptname=$(basename $file)
                
                if (( $debug )); then
                    echo "running hook: ${scriptname}"
                fi
                
                if (( $silent )); then
                    eval $file &> /dev/null
                else
                    eval $file
                fi
                
                script_exit_code=$?
                if [[ $script_exit_code != 0 ]]; then
                    hook_exit_code=$script_exit_code
                fi
                
                if (( $debug )); then
                    echo "hook run complete: ${scriptname}"
                fi
            done
            
            if [[ $hook_exit_code != 0 ]]; then
              echo "A ${hook_type} script yielded negative exit code ${hook_exit_code}"
              exit $hook_exit_code
            fi
            
        fi
    fi
}

main "$@"
