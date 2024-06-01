/// @description Insert description here
// You can write your code in this editor

raw_instructions = [];
direction = 0;
instructions = ds_list_create();

// Add elements to the list
for(var i = 0; i < array_length(raw_instructions); i++)
{
	ds_list_add(instructions, raw_instructions[i]);
}

original_x = x;
original_y = y;

target_x = x;
target_y = y;

current_instr = 0;
step_target = 0;
current_step = 0;