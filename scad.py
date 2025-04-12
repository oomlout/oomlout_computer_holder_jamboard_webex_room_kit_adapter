import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        thicknesses = [3,24]

        for thickness in thicknesses:
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = 5
            p3["height"] = 4
            p3["thickness"] = thickness
            #p3["extra"] = ""
            part["kwargs"] = p3
            nam = "base"
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            if not test:
                pass
                parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "single"
    locs = []
    locs.append([1, 1])
    #locs.append([2, 1])
    locs.append([1,2])
    locs.append([2,2])
    locs.append([1,3])
    locs.append([2,3])
    p3["locations"] = locs
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add jamboard
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cylinder"
        p3["depth"] = depth
        #p3["m"] = "#"
        p3["radius"] = 12.5
        pos1 = copy.deepcopy(pos)         
        pos1[0] += 17.5
        pos1[1] += -5
        pos1[2] += depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #cube 30 x 90 x depth
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 35
        hei = 90
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size
        p3["depth"] = dep
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 12.5
        pos1[1] += -50
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 22.45
        hei = 102.5
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size        
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 6.225
        pos1[1] += -43.75
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #extra cube 50 x 60 at 5,-50
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 50
        hei = 60
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size        
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 5
        pos1[1] += -42.5
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add bar
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 100
        hei = 85
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size        
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -8.5
        pos1[1] += 60
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 7.5
        hei = 100
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 30
        pos1[1] += 60
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)


        #front cube
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 7
        hei = 94
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 37
        pos1[1] += 60
        pos1[2] += 0
        p3["pos"] = pos1        
        oobb_base.append_full(thing,**p3)

        #radius clearance cube
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        wid = 4
        hei = 8
        dep = depth
        size = [wid, hei, dep]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 24.5
        pos1[1] += 13.6
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add screw
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["depth"] = 12
        p3["m"] = "#"
        p3["radius_name"] = "m3"
        pos1 = copy.deepcopy(pos)         
        pos1[0] += 0
        pos1[1] += 7.5
        pos1[2] += depth/2
        p3["pos"] = pos1
        rot1 = copy.deepcopy(rot)
        rot1[0] += 90
        rot1[1] += 0
        rot1[2] += 0
        p3["rot"] = rot1
        oobb_base.append_full(thing,**p3)  

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)