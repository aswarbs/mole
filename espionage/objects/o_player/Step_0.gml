/// @description Insert description here
// You can write your code in this editor

/* Assign target from instructions */
if(current_step >= step_target){
	original_x = x;
	original_y = y;
	
	if (ds_list_empty(instructions)){
		return;
	}
	
	var next_instr = ds_list_find_value(instructions, 0);
	ds_list_delete(instructions, 0);
	
	current_step = 0;
	current_instr = next_instr
	switch(next_instr){
		case FORWARD:
			step_target = 100;
			break;
		case TURN:
			step_target = 90;
			break;
		case SHOOT:
			current_step = step_target;
			break;
	}
	
}

switch(current_instr){
	case FORWARD:
		x = x + lengthdir_x(1, direction);
		y = y + lengthdir_y(1, direction);
		current_step += 1;
		break;
	case TURN:
		direction += 1;
		image_angle += 1;
		current_step += 1;
		break;
	case SHOOT:
		break;	
}