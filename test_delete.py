#!/usr/bin/python3
"""Test delete feature"""
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
print("New State: {}".format(new_state))

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))

# Delete the new State
fs.delete(new_state)
fs.save()

# All States after delete
all_states = fs.all(State)
print("All States after delete: {}".format(len(all_states.keys())))
