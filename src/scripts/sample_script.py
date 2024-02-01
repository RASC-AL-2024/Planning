# Import Required Packages
from src.intelligence.highlevel.persona import Persona
import time
import sys

# Define Dictionaries for Input and High Level Objective
OBJECTIVE = ""
rover_state = {
    'battery_level': 1.0,
    'position': [0, 0, 0],
    'orientation': [0, 0, 0],
    'active': True,
    'planned_trajectory': [[0, 0, 1], [0, 1, 1,], [1, 1, 1]],
    'has_load': True
}

arm_state = {
    'battery_level': 1.0,
    'position': [0, 0, 0],
    'orientation': [0, 0, 0],
    'active': True,
    'current_action': ""
}

env_state = {
    'temperature': 42.0,
    'luminosity': 0.5,
    'material_deposits': "",
    'high_level_map_info': ""
}

high_level_planning_state: {
    'steps': "",
    'contingencies': ""
}


# Planning
input_dict = {
    'rover_state': rover_state,
    'arm_state': arm_state,
    'env_state': env_state,
    'high_level_planning_state': high_level_planning_state
}
system_args = {
    'input_dict': input_dict
}
prompt_args = {
    'objective': OBJECTIVE
}

print("Generating robot plan...")
starting_codegen_time = time.time()
planner = Persona(name = "planner", prompt_path = "lunar_ops.txt")
formatted = planner.format_prompt(system_args, system = True)
generated_code, _ = planner.chat(system_args, prompt_args)
ending_codegen_time = time.time()
print("Robot planning actions generated successfully.\n")
print("LLM Actions Generation Time: " + "{:.4f}".format(ending_codegen_time - starting_codegen_time) + " seconds.\n")

print('The following was output by the Large Language Model:\n')
print(generated_code)
print(' ')

# Terminate program if no code was generated due to an unclear objective
if "I'm sorry" or "incomplete" in generated_code:
    print("No code was generated due to an unclear objective.")
    sys.exit(1)

