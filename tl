#!/bin/bash

tmuxp load ~/.tmux/layouts/`find ~/.tmux/layouts -type f -name "*.yaml" | xargs basename | fzf`
