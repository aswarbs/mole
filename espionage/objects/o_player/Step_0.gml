/// @description Insert description here
// You can write your code in this editor

/* Assign target from instructions */
if(target_x == x && target_y == y){
	original_x = x;
	original_y = y;
	
	if (ds_list_empty(instructions)){
		return;
	}
	
	var next_instr = ds_list_find_value(instructions, 0);
	ds_list_delete(instructions, 0);
	
	switch(next_instr){
		case UP:
			target_y = y - 100;
			target_x = x;
			break;
		case LEFT:
			target_y = y;
			target_x = x - 100;
			break;
		case RIGHT:
			target_y = y;
			target_x = x + 100;
			break;
		case DOWN:
			target_y = y + 100;
			target_x = x;
			break;
	}
	
}


/* Move to target */
if(x < target_x){ x += 1; }
if(x > target_x){ x -= 1; }
if(y < target_y){ y += 1; }
if(y > target_y){ y -= 1; }