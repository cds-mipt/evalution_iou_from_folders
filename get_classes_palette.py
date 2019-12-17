# For winter city dataset

color_mask_dict = {
        "background":"000000",
        "traffic_sign": "00ffff",
        "car": "ff0000",
        "double_solid": "ffc1ff", 
        "intermittent": "8000ff",
        "person": "cc99ff",
        "solid": "ffc125",
        "stop_lane": "8055ff",
        "traffic_light": "0080ff",
        "borders": "b496c8",  
        "road": "ff00ff",
        "sky": "87ceff"
    }

def convert_str_to_rgb(str_value):
    return (int(str_value[4:6],16), int(str_value[2:4],16), int(str_value[0:2],16))

def get_classes_palette():
    '''
    to get dict "classes" - color to number of class
           dict "palette" - number of class to name of class
    '''
    palette = {} 
    classes = {} 
    for i, obj in enumerate(color_mask_dict):
        color = convert_str_to_rgb(color_mask_dict[obj])
        palette[color] = i
        classes[i] = obj

    palette[convert_str_to_rgb("ff8000")] = 2 # truck to car 
    
    return classes, palette