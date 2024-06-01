/// @description Insert description here
// You can write your code in this editor
if image_speed > 0
{
	if (image_index > image_number - 1)
	{
		instance_destroy();
		room_goto(rm_loser);
	}
}

