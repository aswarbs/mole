/// @description Insert description here
// You can write your code in this editor

raw_instructions = [RIGHT, RIGHT, UP];

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
