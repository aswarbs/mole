
randomize();

var WIDTH = 10;
var HEIGHT = 10;

var cx = 0;
var cy = 400;

PATH = ds_list_create();
ds_list_add(PATH, [cx, cy])	

instance_create_layer(cx + 100, cy + 100, "Instances", o_player);

for(var i = 1; i < WIDTH; i++)
{
	cx = (i * 100)
	
	ds_list_add(PATH, [cx, cy])	
	
	if(random_range(0, 10) > 6){
		ty = irandom_range(0, 9) * 100;
		while(cy != ty){
			if(cy < ty){cy += 100}
			else if(cy > ty){cy -= 100}
			ds_list_add(PATH, [cx, cy]);
		}
	}
}

instance_create_layer(cx + 50, cy + 50, "Instances", o_coin);

// Iterate over the ds_list and get each element
var list_size = ds_list_size(PATH);
for (var i = 0; i < list_size; i++) {
    var element = ds_list_find_value(PATH, i);
    instance_create_layer(element[0] + 50, element[1] + 50, "Instances", o_path);
}

// Fill in the rest of it
function in_path(_x, _y, _PATH){
	var list_size = ds_list_size(_PATH);
	for (var i = 0; i < list_size; i++) {
		var element = ds_list_find_value(_PATH, i);
		if(_x == element[0] && _y == element[1]){
			return true;
		}
	}
	return false;
}

var nos = 50;
var count = 0;
while(count < nos){
	count++;
	var rx = irandom_range(0, 9) * 100;
	var ry = irandom_range(0, 9) * 100;
	while(in_path(rx, ry, PATH)){
		var rx = irandom_range(0, 9) * 100;
		var ry = irandom_range(0, 9) * 100;		
	}
	instance_create_layer(rx + 50, ry + 50, "Instances", o_bush);
}


var rx = irandom_range(0, 9) * 100;
var ry = irandom_range(0, 9) * 100;
while(!in_path(rx, ry, PATH) && !(rx == 0 && ry == 400)){
	var rx = irandom_range(0, 9) * 100;
	var ry = irandom_range(0, 9) * 100;		
}
instance_create_layer(rx + 50, ry + 50, "Instances", o_barrier);
var cx = rx;
var cy = ry;

var rx = irandom_range(0, 9) * 100;
var ry = irandom_range(0, 9) * 100;
while(!in_path(rx, ry, PATH) && !(rx == 0 && ry == 400) && !(rx == cx && ry == cy)){
	var rx = irandom_range(0, 9) * 100;
	var ry = irandom_range(0, 9) * 100;		
}
instance_create_layer(rx + 50, ry + 50, "Instances", o_barrier);