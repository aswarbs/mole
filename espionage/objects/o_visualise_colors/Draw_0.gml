/// @description Insert description here
// You can write your code in this editor

for(var _k = 0; _k < ds_list_size(global.LAST_PROGRAM); _k++){
	switch global.LAST_PROGRAM[|_k]{
		case "red":
			draw_set_color(c_red);
			break;
		case "green":
			draw_set_color(c_green);
			break;
		case "blue":
			draw_set_color(c_blue);
			break;
	}
	draw_circle(x + (40 * _k), y, 30, false);
	draw_set_color(c_black);
	draw_circle(x + (40 * _k), y, 31, true);
	draw_circle(x + (40 * _k), y, 32, true);
}

draw_set_color(c_white);