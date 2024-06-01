/// @description Handles Server Connection & Parses Hand Data
/// @author Toby Benjamin Clark
/// @date   16/01/2023

var n_id = ds_map_find_value(async_load, "id");
if(n_id == server_socket)
{
    var t = ds_map_find_value(async_load, "type");
    var socketlist = ds_list_create();

    if(t == network_type_connect)
    {
        var sock = ds_map_find_value(async_load, "socket");
        ds_list_add(socketlist, sock);
    }

    if(t == network_type_data)
    {
        var t_buffer = ds_map_find_value(async_load, "buffer"); 
        var cmd_type = buffer_read(t_buffer, buffer_string);

        // Original string
        var originalString = string(cmd_type);

        jsonData = json_parse(originalString)

        // Check if the struct has left variable
        if variable_struct_exists(jsonData, "contours")
        {
			show_debug_message(jsonData.contours);
			
			var contours = jsonData.contours;
			with(o_player){
				for(var i = 0; i < array_length(contours); i++){
					var elem = contours[i];
					switch elem{
						
						case "red":
							ds_list_add(instructions, FORWARD);
							break;
						case "green":
							ds_list_add(instructions, TURN);
							break;
						case "blue":
							ds_list_add(instructions, SHOOT);
							break;
						
					}
				}
			}
        }
		
		if variable_struct_exists(jsonData, "button")
        {
			show_debug_message(jsonData.button);
			
			var button = jsonData.button;
			with(o_player){
				for(var i = 0; i < array_length(button); i++){
					var elem = button[i];
					switch elem{
						
						case "1":
							show_debug_message("1");
							break;
						case "2":
							show_debug_message("2");
							break;
						case "3":
							show_debug_message("3");
							break;
						case "4":
							show_debug_message("4");
							break;
						
					}
				}
			}
        }



        show_debug_message(jsonData)

    }
}