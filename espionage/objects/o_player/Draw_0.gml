/// @description Insert description here
// You can write your code in this editor

draw_self();
draw_text(x + 110, y, "X: " + string(x) + "  Y:" + string(y));
draw_text(x + 110, y + 15, "OX: " + string(original_x) + "  OY:" + string(original_y));
draw_text(x + 110, y + 30, "TX: " + string(target_x) + "  TY:" + string(target_y));
draw_text(x + 110, y + 35, "DIR: " + string(direction) + "  SPD:" + string(speed));