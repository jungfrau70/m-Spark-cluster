Reference:
- https://gist.github.com/MohamedAlaa/2961058

export WORKDIR='/root/PySpark/workspace/'
cd $WORKDIR

#########################################################################################
# 1. Prepare tmux console
#########################################################################################

## Install tmux
yum install tmux

or
apt-get install tmux

## Create tmux session
tmux

## detach tmux session
ctrl+b, d

## list tmux session
tmux ls

## attach tmux session
tmux attach -t 0

## tmux short-keys
ctrl+b, %  # Add new pane in column
ctrl_b, "  # Add new pane in row
ctrl+b, >  # Move with direction-arrow key
ctrl+b, x  # Exit the current pane
ctrl+b, &  # Exit all pane
ctrl+b, o  # Rotate pane within session
ctrl+b, ,  # Change session name
ctrl+b, [  # Go to copy-mode, and drag the text to copy
ctrl+b, ]  # Paste