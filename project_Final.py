#-------------------------------------------------------------------------------------------
#Small assignments

#TODO: fix scale additive
#linear increase, linear decrease (1, 2, 3) (1, 0.8, 0.6) (1, -0.8, 0.6) (1, -1.2, 1.4)
#exponential increase, exponential decrease (1, 2, 4) (1, 0.5, 0.25) (1, -2, 4) (1, -0.5, 0.25)
#fix duplicate + scale doing opposite of what u want

#TODO: pivot for modify/dup
#fix duplicate + modify working on repeat (with by individual block checked or not)
#need to center pivot after each duplication? otherwise modify after dup is done based off of first gen's pivot...
#or modify modifies by each dup's pivot by default ?
#fix scale/rotate pivot in the modifier and duplicater
#duplicater puts every pivot at baseline or centers every pivot?
#pivot to center checkbox for both duplicater and modifier 

#hide duplicated/mirrored base planes checboxes in the modify section and/or in the duplicater?

#add all the other primitive shapes!!! cones, pyramids etc.

#--------------------------------------------------------------------------------------------
#Big assignment 1

#TODO: #mirror option inside the duplicater (note, mirror creates dup1, dup2... like duplicater that way naming works ez)
#needs to maintain all the functionality of the duplicater + can choose offset or clamp

#TODO: presets
# primitive shapes: cone, pyramid, etc
# sky: dust particles, clouds, rain ...
# cyberpunk: skyscrapers, sky pathways, dystopian buildings, cyberpunk, transformers, flying lazaro shit ...
# regular city: city, town
# terrains: bamboos, grass, pebbles, rocks, fields, mountains, dirt/rocky pathways ?

#TODO: edge cases:
#does centering every gen at 0,0,0 make sense every time? or should I add a checkbox option to not do that? i think it's fine
#gen settings (modify) and gen clipboard after relaunch code? after regen/gen? try modifying shit then relaunching code?
#save gen ?
#duplicate, modify ?

#--------------------------------------------------------------------------------------------
#Big assignment 2

#TODO: make all slider just one function that way can modify slider more easily (for reset button for instance)
#reset button for all sliders (both in the generator tab and in the gen tabs)
#      use default_gen_settings dictionary for the gen tabs, and use default_settings preset for the generator tab
#make sliders real time while dragging for the modify sliders
#reset default settings for the modify tabs

#TODO: restructure code
#confirm whether or not u should put some of the code at the bottom of generate function inside the create tab fct
#one universal fct with reset options etc
#other shit ...

#-------------------------------------------------------------------------------------------
#Extra

#TODO:
#modifier: modify shape !! all cubes -> all cones

#TODO: transfer all global settings into a dictionary so that instead of doing global ... for all settings just do global SETTINGS
#TODO: make it so that can save a city preset ? and delete it ?
#TODO: remember last settings before closed script ? both for gen and for modify ???

#TODO: merge gens option ? takes all the groups and objects in one gen and places them into another (maybe keeps both old gens and renames them and hides them?)
#requires renaming of block groups and buildings of 2nd gen by just incrementing block 1 1, 1 2, 2 1, 2 2 to block 4 1, 4 2, 5 1, 5 2

#TODO: option to modify the initial object
#ez option: option to modify object before generation and all objects generated have those changes! (eg torus inner radius)
#or more advanced option would be to also have those attributes randomizables, for instance torus inner radius randomizable...

#TODO: deformer (move v/e/f, scale e/f, rotate e/f, bevel v/e/f, inset e/f, extrude f)
#TODO: scatterer

#voir iPhone notes (Maya Python v1, v2, ... v9)

#-------------------------------------------------------------------------------------------

#Assets, textures, lights

#TODO: model buildings and import or no?
# if keep simple cubes: bevels? windows? echaffaudage? roofs? variations on buildings?
#TODO: actual roads? trees? streetlights? wires? cars? people?
#TODO: lights inside buildings and on roofs? window emissive textures? tokyo signs?
#TODO: background? sky? fog? dust particles? lazaro flying shit?

#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import random
import re
import maya.mel as mel
import subprocess
import platform



#generation trackers
generations = {}  # key = gen_number, value = group containing the list of block groups of that generation
gen_tabs = {} # key = gen_number, value = UI tab layout
gen_number = 0

initial_gen_settings = {} #to reset a gen tab to its initial state
gen_settings = {} #settings for each gen tab (all settings: modify, duplicate, ...)

save_gen = set() #list of gen numbers that saved
save_button = {}

gen_clipboard = {} #key = gen_number, value = settings at the moment of generation of that city 
gen_undo_settings = {} 
gen_redo_settings = {}
gen_at_each_modif = True



#shape settings
shape = ""
shapes = ["cube", "sphere", "cylinder", "torus"]

#building size parameters
min_height = 8 
max_height = 30
min_width = 4 
max_width = 4 
min_depth = 3
max_depth = 7 

#building translate parameters
min_tran_X = 0
max_tran_X = 0
min_tran_Y = 0
max_tran_Y = 0
min_tran_Z = 0
max_tran_Z = 0

#building rotation parameters
min_rot_X = 0
max_rot_X = 0
min_rot_Y = 0
max_rot_Y = 0
min_rot_Z = 0
max_rot_Z = 0



#scatter parameters
min_num_buildings = 16
max_num_buildings = 16
subdiv_w = 4 
subdiv_h = 4 
num_blocks_x = 3
num_blocks_z = 3 

#block size parameters
block_size_X = 33  
block_size_Z = 33  
space_between_blocks_X = 12 
space_between_blocks_Z = 12 



#block scale parameters
block_min_size = 1
block_max_size = 1

block_min_scale_X = 1
block_max_scale_X = 1
block_min_scale_Y = 1
block_max_scale_Y = 1
block_min_scale_Z = 1
block_max_scale_Z = 1

#block translate parameters
block_min_tran_X = 0
block_max_tran_X = 0
block_min_tran_Y = 0
block_max_tran_Y = 0
block_min_tran_Z = 0
block_max_tran_Z = 0

#block rotation parameters
block_min_rot_X = 0
block_max_rot_X = 0
block_min_rot_Y = 0
block_max_rot_Y = 0
block_min_rot_Z = 0
block_max_rot_Z = 0



#global scale parameters
global_min_size = 1
global_max_size = 1

global_min_scale_X = 1
global_max_scale_X = 1
global_min_scale_Y = 1
global_max_scale_Y = 1
global_min_scale_Z = 1
global_max_scale_Z = 1

#block translate parameters
global_min_tran_X = 0
global_max_tran_X = 0
global_min_tran_Y = 0
global_max_tran_Y = 0
global_min_tran_Z = 0
global_max_tran_Z = 0

#block rotation parameters
global_min_rot_X = 0
global_max_rot_X = 0
global_min_rot_Y = 0
global_max_rot_Y = 0
global_min_rot_Z = 0
global_max_rot_Z = 0

#base plane parameters
hide_base_planes = False



#gen tab modify settings
gen_building_size = {}
gen_building_rot = {}
gen_checkbox_mod_indiv_building = {}
gen_block_size = {}
gen_block_rot = {}
gen_checkbox_mod_indiv_block = {}
gen_checkbox_mod_indiv_duplicate = {}
gen_global_size = []
gen_global_rot = []

gen_slider_tranX_global = {}
gen_slider_tranY_global = {}
gen_slider_tranZ_global = {}
gen_slider_size_global = {}
gen_slider_scaleX_global = {}
gen_slider_scaleY_global = {}
gen_slider_scaleZ_global = {}
gen_slider_rotX_global = {}
gen_slider_rotY_global = {}
gen_slider_rotZ_global = {}
gen_checkbox_hide_planes = {}

#gen tab duplicate settings
gen_slider_dup_iterations = {}
gen_checkbox_dup_prior_dup = {}
gen_checkbox_dup_indiv_dup = {}
gen_checkbox_dup_indiv_block = {}
gen_checkbox_dup_indiv_building = {}

gen_checkbox_dup_scale_mult = {}
gen_slider_dup_size = {}
gen_slider_dup_scaleX = {}
gen_slider_dup_scaleY = {}
gen_slider_dup_scaleZ = {}

gen_checkbox_dup_tran_add = {}
gen_slider_dup_tranX = {}
gen_slider_dup_tranY = {}
gen_slider_dup_tranZ = {}

gen_checkbox_dup_rot_add = {}
gen_slider_dup_rotX = {}
gen_slider_dup_rotY = {}
gen_slider_dup_rotZ = {}



#color paramrters
subsub_color = (0.32, 0.32, 0.34)
sub_color = (0.37, 0.37, 0.37)
green_color = (0.34, 0.5, 0.34)
green_color2 = (0.32, 0.44, 0.32)
red_color = (0.5, 0.24, 0.24)



# generate ------------------------------ 
def retab_existing_gens():
    global generations, gen_settings

    all_groups = cmds.ls("GEN*_GRP")  #get all groups starting with "GEN"
    gen_groups = [g for g in all_groups if re.fullmatch(r"GEN\d+_GRP", g)]  #filter only the gen groups (NOT the block groups)
    if gen_groups:
        for gen in gen_groups: 
            temp = gen
            gen_num = int(temp.split("_")[0].replace("GEN", "")) #every existing gen number
            
            generations[gen_num] = gen
            gen_settings[gen_num] = default_gen_settings({}, gen_num)
            create_generation_tab(gen_num) 
            save_generation(gen_num)
            save_gen.add(gen_num)

def regenerate_city(*args):
    global gen_number, gen_settings, save_gen, shape, subdiv_w, subdiv_h
    
    #compute next generation number (normal regeneration process)
    gen_number = 0
    for gen_num in generations.keys():
        if gen_num >= gen_number:
            gen_number = gen_num

    #retrieve highest existing generation number
    if gen_number == 0: #IF PRESS REGENERATE RIGHT AFTER EXECUTING CODE (NO GEN TABS YET)
        gen_groups = cmds.ls("GEN*_GRP")  #get all groups starting with "GEN"
        if gen_groups:
            for gen in gen_groups:
                temp = gen
            num = int(temp.split("___")[0].replace("GEN", "")) #highest existing gen number
            gen_number = num

    gen_number += 1 
    block_grp = []

    no_sw = False
    no_sh = False
    if (subdiv_w == 1):
        no_sw = True
        subdiv_w = 2
    if (subdiv_h == 1):
        no_sh = True
        subdiv_h = 2

    for y in range(num_blocks_z): #each block y
        for x in range(num_blocks_x): #each block x
            #base planes
            basePlane = cmds.polyPlane(w=block_size_X-space_between_blocks_X, h=block_size_Z-space_between_blocks_Z, sw=subdiv_w-1, sh=subdiv_h-1, name=f"GEN{gen_number}___block{x+1}_{y+1}_basePlane")
            basePlaneLarger = cmds.polyPlane(w=block_size_X, h=block_size_Z, name=f"GEN{gen_number}___block{x+1}_{y+1}_basePlaneLarger")
            if(hide_base_planes):
                cmds.hide(f"GEN{gen_number}___block{x+1}_{y+1}_basePlane")
                cmds.hide(f"GEN{gen_number}___block{x+1}_{y+1}_basePlaneLarger")

            #number of vertices on the base plane
            num_vertices = cmds.polyEvaluate(f"GEN{gen_number}___block{x+1}_{y+1}_basePlane", vertex=True)
                   
            if (no_sw):
                subdiv_w = 1
            if (no_sh):
                subdiv_h = 1
            

            #number of buildings to generate per block
            num_buildings = random.randint(min_num_buildings, max_num_buildings)
            
            #list containing random sample of indices of vertices on the base plane, where list size = num_buildings
            #chosen_vertices = random.sample(range(num_vertices), min(num_buildings, num_vertices))

            j = 0
            while (num_buildings > 0):
                chosen_vertices = random.sample(range(num_vertices), min(num_buildings, num_vertices))

                for i in chosen_vertices: #each building
                    j += 1

                    #get vertex location
                    vertex_x = cmds.xform(f"GEN{gen_number}___block{x+1}_{y+1}_basePlane.vtx[{i}]", q=True, t=True, ws=True)[0]
                    vertex_y = cmds.xform(f"GEN{gen_number}___block{x+1}_{y+1}_basePlane.vtx[{i}]", q=True, t=True, ws=True)[1]
                    vertex_z = cmds.xform(f"GEN{gen_number}___block{x+1}_{y+1}_basePlane.vtx[{i}]", q=True, t=True, ws=True)[2]

                    if no_sw:
                        vertex_x = 0   # force X to plane center
                    if no_sh:
                        vertex_z = 0   # force Z to plane center

                    #choose cube shape
                    cube_name = f"GEN{gen_number}___block{x+1}_{y+1}_building{j}"
                    
                    if (shape == ""):
                        shape = "cube"
                        obj = cmds.polyCube(name=cube_name)[0]
                    elif (shape == "cube"):
                        obj = cmds.polyCube(name=cube_name)[0]
                    elif (shape == "sphere"):
                        obj = cmds.polySphere(name=cube_name)[0]
                    elif (shape == "cylinder"):
                        obj = cmds.polyCylinder(name=cube_name)[0]
                    elif (shape == "torus"):
                        obj = cmds.polyTorus(name=cube_name)[0]

                    #move cube to random vertex location                
                    cmds.move(vertex_x, vertex_y, vertex_z)

                    #move cube up to baseline
                    h = cmds.getAttr(f"{obj}.scale")[0][1]
                    if (shape == "cube"):
                        cmds.move(0, h/2, 0, r=True)               
                    elif (shape == "sphere"):
                        cmds.move(0, h, 0, r=True)
                    elif (shape == "cylinder"):
                        cmds.move(0, h, 0, r=True)
                    elif (shape == "torus"):
                        cmds.move(0, h/2, 0, r=True)

                    #move building pivot to baseline
                    px, py, pz = cmds.xform(cube_name, q=True, ws=True, rp=True)
                    baseLineHeight = cmds.xform(f"GEN{gen_number}___block{1}_{1}_basePlane", q=True, t=True)[1]
                    cmds.xform(cube_name, ws=True, piv=[px, baseLineHeight, pz]) # moves both rotate and scale pivots

                    # scale
                    ran_scale1 = random.uniform(min_width, max_width)
                    ran_scale2 = random.uniform(min_height, max_height)
                    ran_scale3 = random.uniform(min_depth, max_depth)
                    gen_building_size[cube_name] = [ran_scale1, ran_scale2, ran_scale3]

                    # rotate
                    ran_rot1 = random.uniform(min_rot_X, max_rot_X)
                    ran_rot2 = random.uniform(min_rot_Y, max_rot_Y)
                    ran_rot3 = random.uniform(min_rot_Z, max_rot_Z)
                    gen_building_rot[cube_name] = [ran_rot1, ran_rot2, ran_rot3]

                    # translate
                    ran_tran1 = random.uniform(min_tran_X, max_tran_X)
                    ran_tran2 = random.uniform(min_tran_Y, max_tran_Y)
                    ran_tran3 = random.uniform(min_tran_Z, max_tran_Z)

                    if (ran_scale1 == 0 or ran_scale2 == 0 or ran_scale3 == 0):
                        cmds.delete(cube_name)
                    
                    else:
                        cmds.scale(ran_scale1, ran_scale2, ran_scale3)
                        cmds.rotate(ran_rot1, ran_rot2, ran_rot3)
                        cmds.move(ran_tran1, ran_tran2, ran_tran3, r=True)

                num_buildings -= num_vertices

            # Create a group containing all the buildings and planes in this block
            buildings = cmds.ls(f"GEN{gen_number}___block{x+1}_{y+1}_building*")
            grp = cmds.group(buildings, 
                            f"GEN{gen_number}___block{x+1}_{y+1}_basePlane", 
                            f"GEN{gen_number}___block{x+1}_{y+1}_basePlaneLarger",
                            name=f"GEN{gen_number}___block{x+1}_{y+1}_GRP")   #block group: group containing all buildings and planes for this block
            
            #move group to new block location
            cmds.move(x*block_size_X, 0, y*block_size_Z, grp)

            #move block group pivot to baseline
            px, py, pz = cmds.xform(grp, q=True, ws=True, rp=True)
            baseLineHeight = cmds.xform(f"GEN{gen_number}___block{1}_{1}_basePlane", q=True, t=True)[1]
            cmds.xform(grp, ws=True, piv=[px, baseLineHeight, pz]) # moves both rotate and scale pivots

            #block scale
            block_ran_size = random.uniform(block_min_size, block_max_size)
            block_ran_scale1 = random.uniform(block_min_scale_X, block_max_scale_X)
            block_ran_scale2 = random.uniform(block_min_scale_Y, block_max_scale_Y)
            block_ran_scale3 = random.uniform(block_min_scale_Z, block_max_scale_Z)
            gen_block_size[grp] = [block_ran_size * block_ran_scale1, block_ran_size * block_ran_scale2, block_ran_size * block_ran_scale3]

            #block translate
            block_ran_tran1 = random.uniform(block_min_tran_X, block_max_tran_X)
            block_ran_tran2 = random.uniform(block_min_tran_Y, block_max_tran_Y)
            block_ran_tran3 = random.uniform(block_min_tran_Z, block_max_tran_Z)

            #block rotate
            block_ran_rot1 = random.uniform(block_min_rot_X, block_max_rot_X)
            block_ran_rot2 = random.uniform(block_min_rot_Y, block_max_rot_Y)
            block_ran_rot3 = random.uniform(block_min_rot_Z, block_max_rot_Z)
            gen_block_rot[grp] = [block_ran_rot1, block_ran_rot2, block_ran_rot3]
            
            cmds.scale(block_ran_size * block_ran_scale1, block_ran_size * block_ran_scale2, block_ran_size * block_ran_scale3)
            cmds.move(block_ran_tran1, block_ran_tran2, block_ran_tran3, r=True)
            cmds.rotate(block_ran_rot1, block_ran_rot2, block_ran_rot3)

            block_grp.append(grp) #block group list: list of all block groups of this generation

    if block_grp:
        gen_grp = cmds.group(block_grp, name=f"GEN{gen_number}_GRP") #gen group: group containing the list of block groups of this generation
        generations[gen_number] = gen_grp

        #move gen group pivot to baseline
        px, py, pz = cmds.xform(gen_grp, q=True, ws=True, rp=True)
        baseLineHeight = cmds.xform(f"GEN{gen_number}___block{1}_{1}_basePlane", q=True, t=True)[1]
        cmds.xform(gen_grp, ws=True, piv=[px, baseLineHeight, pz]) # moves both rotate and scale pivots
        
        #move gen to world center
        center_group_to_origin(gen_grp)

        #global scale
        global_ran_size = random.uniform(global_min_size, global_max_size)
        global_ran_scale1 = random.uniform(global_min_scale_X, global_max_scale_X)
        global_ran_scale2 = random.uniform(global_min_scale_Y, global_max_scale_Y)
        global_ran_scale3 = random.uniform(global_min_scale_Z, global_max_scale_Z)
        gen_global_size = [global_ran_size * global_ran_scale1, global_ran_size * global_ran_scale2, global_ran_size * global_ran_scale3]

        #global translate
        global_ran_tran1 = random.uniform(global_min_tran_X, global_max_tran_X)
        global_ran_tran2 = random.uniform(global_min_tran_Y, global_max_tran_Y)
        global_ran_tran3 = random.uniform(global_min_tran_Z, global_max_tran_Z)

        #global rotate
        global_ran_rot1 = random.uniform(global_min_rot_X, global_max_rot_X)
        global_ran_rot2 = random.uniform(global_min_rot_Y, global_max_rot_Y)
        global_ran_rot3 = random.uniform(global_min_rot_Z, global_max_rot_Z)
        gen_global_rot = [global_ran_rot1, global_ran_rot2, global_ran_rot3]

        cmds.scale(global_ran_size * global_ran_scale1, global_ran_size * global_ran_scale2, global_ran_size * global_ran_scale3)
        cmds.move(global_ran_tran1, global_ran_tran2, global_ran_tran3, r=True)
        cmds.rotate(global_ran_rot1, global_ran_rot2, global_ran_rot3)

        #tab shit
        default_settings = {
            "buildingSizes": {
                "1": gen_building_size,
            },
            "buildingRots": {
                "1": gen_building_rot,
            } ,            

            "blockSizes": {
                "1": gen_block_size,
            },
            "blockRots": {
                "1": gen_block_rot,
            },

            "duplicateSizes": {
                "1": gen_global_size,
            },
            "duplicateRots": {
                "1": gen_global_rot,
            },
            
            "globalSizes": gen_global_size,
            "globalRots": gen_global_rot,

            "hideBasePlanes": hide_base_planes,
        }
        gen_settings[gen_number] = default_gen_settings(default_settings, gen_number)
        create_generation_tab(gen_number) 
        gen_clipboard[gen_number] = getCurrentSettings() 

def generate_city(*args):
    global gen_number

    #reset generation counter to 0
    gen_number = 0

    # Delete all existing generations
    gen_objects = cmds.ls("GEN*")  # get all objects starting with "GEN"
    if gen_objects:
        for obj in gen_objects:
            gen_num = int(obj.split("GEN")[1].split("_")[0])
            if (gen_num) in save_gen:
                continue
            else:
                if cmds.objExists(obj):
                    cmds.delete(obj)

    #delete all gen tabs
    delete_all_gen_tabs()

    regenerate_city()    

def center_group_to_origin(group):
    # 1. Get bounding-box center of the entire hierarchy
    bbox = cmds.xform(group, q=True, ws=True, bb=True)
    cx = (bbox[0] + bbox[3]) / 2.0
    cy = (bbox[1] + bbox[4]) / 2.0
    cz = (bbox[2] + bbox[5]) / 2.0

    # 2. Move the group *by the negative center* to bring it to origin
    cmds.move(-cx, 0, -cz, group, r=True, ws=True)

    # freeze transform (apply transform so that it's back at 0, 0, 0)
    cmds.makeIdentity(group, apply=True, t=True)



# presets/settings -----------------------
def presets(*args):
    def cube_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
    
        shape = "cube"
        min_height = 10
        max_height = 10
        min_width = 10
        max_width = 10
        min_depth = 10
        max_depth = 10
        min_tran_X = 0
        max_tran_X = 0
        min_tran_Y = 0
        max_tran_Y = 0
        min_tran_Z = 0
        max_tran_Z = 0
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 1
        max_num_buildings = 1
        subdiv_w = 1
        subdiv_h = 1
        num_blocks_x = 1
        num_blocks_z = 1
        block_size_X = 0.1
        block_size_Z = 0.1
        space_between_blocks_X = 0
        space_between_blocks_Z = 0
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False

    def sphere_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
    
        shape = "sphere"
        min_height = 5
        max_height = 5
        min_width = 5
        max_width = 5
        min_depth = 5
        max_depth = 5
        min_tran_X = 0
        max_tran_X = 0
        min_tran_Y = 0
        max_tran_Y = 0
        min_tran_Z = 0
        max_tran_Z = 0
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 1
        max_num_buildings = 1
        subdiv_w = 1
        subdiv_h = 1
        num_blocks_x = 1
        num_blocks_z = 1
        block_size_X = 0.1
        block_size_Z = 0.1
        space_between_blocks_X = 0
        space_between_blocks_Z = 0
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0

        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False

    def default_city_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
        
        #shape settings
        shape = "cube"

        #building size parameters
        min_height = 8 
        max_height = 30
        min_width = 4 
        max_width = 4 
        min_depth = 3
        max_depth = 7 

        #building translate parameters
        min_tran_X = 0
        max_tran_X = 0
        min_tran_Y = 0
        max_tran_Y = 0
        min_tran_Z = 0
        max_tran_Z = 0

        #building rotation parameters
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0

        #scatter parameters
        min_num_buildings = 16
        max_num_buildings = 16
        subdiv_w = 4 
        subdiv_h = 4 
        num_blocks_x = 3
        num_blocks_z = 3  

        #block size parameters
        block_size_X = 33  
        block_size_Z = 33  
        space_between_blocks_X = 12 
        space_between_blocks_Z = 12

        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1

        #block translate parameters
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0

        #block rotation parameters
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0

        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        #base plane parameters
        hide_base_planes = False

    def small_clouds_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
        
        shape = "sphere"
        min_height = 1
        max_height = 1
        min_width = 1
        max_width = 1
        min_depth = 1
        max_depth = 1
        min_tran_X = 0
        max_tran_X = 3
        min_tran_Y = 0
        max_tran_Y = 2
        min_tran_Z = 0
        max_tran_Z = 1
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 50
        max_num_buildings = 100
        subdiv_w = 36
        subdiv_h = 36
        num_blocks_x = 5
        num_blocks_z = 5
        block_size_X = 25
        block_size_Z = 25
        space_between_blocks_X = 50
        space_between_blocks_Z = 50
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 20
        block_max_tran_Y = 30
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = True

    def small_clouds_settings2():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
    
        shape = "sphere"
        min_height = 1
        max_height = 1
        min_width = 1
        max_width = 1
        min_depth = 1
        max_depth = 1
        min_tran_X = 0
        max_tran_X = 3
        min_tran_Y = 0
        max_tran_Y = 2
        min_tran_Z = 0
        max_tran_Z = 1
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 50
        max_num_buildings = 100
        subdiv_w = 36
        subdiv_h = 36
        num_blocks_x = 5
        num_blocks_z = 5
        block_size_X = 25
        block_size_Z = 25
        space_between_blocks_X = 50
        space_between_blocks_Z = 50
        block_min_size = 0.8
        block_max_size = 2
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = -50
        block_max_tran_X = 50
        block_min_tran_Y = -10
        block_max_tran_Y = 10
        block_min_tran_Z = -50
        block_max_tran_Z = 50
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = True

    def rain_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        shape = "sphere"
        min_height = 0.7
        max_height = 1.3
        min_width = 0.5
        max_width = 0.5
        min_depth = 0.5
        max_depth = 0.5
        min_tran_X = -100
        max_tran_X = 100
        min_tran_Y = -30
        max_tran_Y = 30
        min_tran_Z = -80
        max_tran_Z = 80
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 4
        max_num_buildings = 8
        subdiv_w = 4
        subdiv_h = 4
        num_blocks_x = 5
        num_blocks_z = 5
        block_size_X = 33
        block_size_Z = 33
        space_between_blocks_X = 12
        space_between_blocks_Z = 12
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = True

    def cyber_particles_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        shape = "cube"
        min_height = 1
        max_height = 5
        min_width = 0.5
        max_width = 0.5
        min_depth = 0.5
        max_depth = 0.5
        min_tran_X = -80
        max_tran_X = 80
        min_tran_Y = -30
        max_tran_Y = 30
        min_tran_Z = -80
        max_tran_Z = 80
        min_rot_X = 90
        max_rot_X = 90
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 4
        max_num_buildings = 8
        subdiv_w = 4
        subdiv_h = 4
        num_blocks_x = 10
        num_blocks_z = 10
        block_size_X = 33
        block_size_Z = 33
        space_between_blocks_X = 12
        space_between_blocks_Z = 12
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = True

    def cyber_planes_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        shape = "cube"
        min_height = 5
        max_height = 20
        min_width = 2
        max_width = 2
        min_depth = 2
        max_depth = 2
        min_tran_X = -40
        max_tran_X = 40
        min_tran_Y = -10
        max_tran_Y = 10
        min_tran_Z = -40
        max_tran_Z = 40
        min_rot_X = 90
        max_rot_X = 90
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 1
        max_num_buildings = 1
        subdiv_w = 4
        subdiv_h = 4
        num_blocks_x = 10
        num_blocks_z = 10
        block_size_X = 33
        block_size_Z = 33
        space_between_blocks_X = 12
        space_between_blocks_Z = 12
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = True

    def small_town_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        #shape settings
        shape = "cube"

        #building size parameters
        min_height = 5 
        max_height = 12
        min_width = 3 
        max_width = 6 
        min_depth = 3
        max_depth = 6 

        #building translate parameters
        min_tran_X = 0
        max_tran_X = 0
        min_tran_Y = 0
        max_tran_Y = 0
        min_tran_Z = 0
        max_tran_Z = 0

        #building rotation parameters
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0

        #scatter parameters
        min_num_buildings = 20
        max_num_buildings = 25
        subdiv_w = 5 
        subdiv_h = 5 
        num_blocks_x = 3
        num_blocks_z = 3 

        #block size parameters   
        block_size_X = 33  
        block_size_Z = 33  
        space_between_blocks_X = 12 
        space_between_blocks_Z = 12 

        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1

        #block translate parameters
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0

        #block rotation parameters
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0

        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        #base plane parameters
        hide_base_planes = False

    def skycrapers_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        shape = "cube"
        min_height = 0.1
        max_height = 30
        min_width = 0.1
        max_width = 4
        min_depth = 0.1
        max_depth = 7
        min_tran_X = 0
        max_tran_X = 0
        min_tran_Y = 0
        max_tran_Y = 0
        min_tran_Z = 0
        max_tran_Z = 0
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 200
        max_num_buildings = 200
        subdiv_w = 3
        subdiv_h = 3
        num_blocks_x = 2
        num_blocks_z = 1
        block_size_X = 0.1
        block_size_Z = 0.1
        space_between_blocks_X = 0
        space_between_blocks_Z = 0
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False
    
    def dystopian1_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
    
        shape = "cube"
        min_height = 0.1
        max_height = 20
        min_width = 0.1
        max_width = 4
        min_depth = 4
        max_depth = 7
        min_tran_X = -5
        max_tran_X = 5
        min_tran_Y = 0
        max_tran_Y = 50
        min_tran_Z = -5
        max_tran_Z = 5
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 200
        max_num_buildings = 200
        subdiv_w = 2
        subdiv_h = 2
        num_blocks_x = 1
        num_blocks_z = 1
        block_size_X = 10.8
        block_size_Z = 22.9
        space_between_blocks_X = 25.9
        space_between_blocks_Z = 35.6
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False

    def dystopian2_settings():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes
    
        shape = "cube"
        min_height = 0.1
        max_height = 10
        min_width = 0.1
        max_width = 4
        min_depth = 4
        max_depth = 7
        min_tran_X = 0
        max_tran_X = 1.5
        min_tran_Y = 0
        max_tran_Y = 30
        min_tran_Z = 0
        max_tran_Z = 2.5
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 200
        max_num_buildings = 200
        subdiv_w = 20
        subdiv_h = 2
        num_blocks_x = 1
        num_blocks_z = 1
        block_size_X = 10.8
        block_size_Z = 22.9
        space_between_blocks_X = 25.9
        space_between_blocks_Z = 35.6
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False

    def dystopian3_settings3():
        global shape
        global min_height, max_height, min_width, max_width, min_depth, max_depth
        global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
        global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
        global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
        global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
        global block_min_size, block_max_size
        global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
        global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
        global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
        global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
        global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
        global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
        global hide_base_planes

        shape = "cube"
        min_height = 0.1
        max_height = 10
        min_width = 0.1
        max_width = 4
        min_depth = 4
        max_depth = 7
        min_tran_X = 0
        max_tran_X = 1.5
        min_tran_Y = 0
        max_tran_Y = 30
        min_tran_Z = 0
        max_tran_Z = 2.5
        min_rot_X = 0
        max_rot_X = 0
        min_rot_Y = 0
        max_rot_Y = 0
        min_rot_Z = 0
        max_rot_Z = 0
        min_num_buildings = 200
        max_num_buildings = 200
        subdiv_w = 20
        subdiv_h = 2
        num_blocks_x = 1
        num_blocks_z = 1
        block_size_X = 10.8
        block_size_Z = 22.9
        space_between_blocks_X = 25.9
        space_between_blocks_Z = 35.6
        block_min_size = 1
        block_max_size = 1
        block_min_scale_X = 1
        block_max_scale_X = 1
        block_min_scale_Y = 1
        block_max_scale_Y = 1
        block_min_scale_Z = 1
        block_max_scale_Z = 1
        block_min_tran_X = 0
        block_max_tran_X = 0
        block_min_tran_Y = 0
        block_max_tran_Y = 0
        block_min_tran_Z = 0
        block_max_tran_Z = 0
        block_min_rot_X = 0
        block_max_rot_X = 0
        block_min_rot_Y = 0
        block_max_rot_Y = 0
        block_min_rot_Z = 0
        block_max_rot_Z = 0
        
        #global scale parameters
        global_min_size = 1
        global_max_size = 1

        global_min_scale_X = 1
        global_max_scale_X = 1
        global_min_scale_Y = 1
        global_max_scale_Y = 1
        global_min_scale_Z = 1
        global_max_scale_Z = 1

        #block translate parameters
        global_min_tran_X = 0
        global_max_tran_X = 0
        global_min_tran_Y = 0
        global_max_tran_Y = 0
        global_min_tran_Z = 0
        global_max_tran_Z = 0

        #block rotation parameters
        global_min_rot_X = 0
        global_max_rot_X = 0
        global_min_rot_Y = 0
        global_max_rot_Y = 0
        global_min_rot_Z = 0
        global_max_rot_Z = 0

        hide_base_planes = False

    if args[0] == "Cube":
        cube_settings()
    elif args[0] == "Sphere":
        sphere_settings()    
    elif args[0] == "Default City":
        default_city_settings()
    elif args[0] == "Small Clouds":
        small_clouds_settings2()
    elif args[0] == "Rain":
        rain_settings()    
    elif args[0] == "Cyber Particles":
        cyber_particles_settings()
    elif args[0] == "Cyber Planes":
        cyber_planes_settings()    
    elif args[0] == "Small Town":
        small_town_settings()
    elif args[0] == "Skycrapers":
        skycrapers_settings()
    elif args[0] == "Dystopian1":
        dystopian1_settings()
    elif args[0] == "Dystopian2":
        dystopian2_settings()
    elif args[0] == "Dystopian3":
        dystopian3_settings3() 

    update_all_sliders()
    set_undo_redo_and_generate("Generate")

def update_all_sliders(*args):
    for i in range(len(shapes)):
        if shape == shapes[i]:
            cmds.radioButtonGrp(shape_selector, e=True, select=i+1) 

    cmds.floatSliderGrp(slider_min_height, e=True, value=min_height)
    cmds.floatSliderGrp(slider_max_height, e=True, value=max_height)
    cmds.floatSliderGrp(slider_min_width,  e=True, value=min_width)
    cmds.floatSliderGrp(slider_max_width,  e=True, value=max_width)
    cmds.floatSliderGrp(slider_min_depth,  e=True, value=min_depth)
    cmds.floatSliderGrp(slider_max_depth,  e=True, value=max_depth)

    cmds.floatSliderGrp(slider_min_tran_X, e=True, value=min_tran_X)
    cmds.floatSliderGrp(slider_max_tran_X, e=True, value=max_tran_X)
    cmds.floatSliderGrp(slider_min_tran_Y, e=True, value=min_tran_Y)
    cmds.floatSliderGrp(slider_max_tran_Y, e=True, value=max_tran_Y)
    cmds.floatSliderGrp(slider_min_tran_Z, e=True, value=min_tran_Z)
    cmds.floatSliderGrp(slider_max_tran_Z, e=True, value=max_tran_Z)   

    cmds.floatSliderGrp(slider_min_rot_X, e=True, value=min_rot_X)
    cmds.floatSliderGrp(slider_max_rot_X, e=True, value=max_rot_X)
    cmds.floatSliderGrp(slider_min_rot_Y, e=True, value=min_rot_Y)
    cmds.floatSliderGrp(slider_max_rot_Y, e=True, value=max_rot_Y)
    cmds.floatSliderGrp(slider_min_rot_Z, e=True, value=min_rot_Z)
    cmds.floatSliderGrp(slider_max_rot_Z, e=True, value=max_rot_Z)

    cmds.intSliderGrp(slider_min_num_buildings, e=True, value=min_num_buildings)
    cmds.intSliderGrp(slider_max_num_buildings, e=True, value=max_num_buildings)
    cmds.intSliderGrp(slider_subdiv_w, e=True, value=subdiv_w)
    cmds.intSliderGrp(slider_subdiv_h, e=True, value=subdiv_h)
    cmds.intSliderGrp(slider_num_blocks_x, e=True, value=num_blocks_x)
    cmds.intSliderGrp(slider_num_blocks_z, e=True, value=num_blocks_z)

    cmds.floatSliderGrp(slider_block_size_x, e=True, value=block_size_X)
    cmds.floatSliderGrp(slider_block_size_z, e=True, value=block_size_Z)
    cmds.floatSliderGrp(slider_space_between_blocks_x, e=True, value=space_between_blocks_X)
    cmds.floatSliderGrp(slider_space_between_blocks_z, e=True, value=space_between_blocks_Z)
   
    cmds.floatSliderGrp(slider_block_min_size, e=True, value=block_min_size)
    cmds.floatSliderGrp(slider_block_max_size, e=True, value=block_max_size)
    cmds.floatSliderGrp(slider_block_min_scale_X, e=True, value=block_min_scale_X)
    cmds.floatSliderGrp(slider_block_max_scale_X, e=True, value=block_max_scale_X)
    cmds.floatSliderGrp(slider_block_min_scale_Y, e=True, value=block_min_scale_Y)
    cmds.floatSliderGrp(slider_block_max_scale_Y, e=True, value=block_max_scale_Y)
    cmds.floatSliderGrp(slider_block_min_scale_Z, e=True, value=block_min_scale_Z)
    cmds.floatSliderGrp(slider_block_max_scale_Z, e=True, value=block_max_scale_Z)

    cmds.floatSliderGrp(slider_block_min_tran_X, e=True, value=block_min_tran_X)
    cmds.floatSliderGrp(slider_block_max_tran_X, e=True, value=block_max_tran_X)
    cmds.floatSliderGrp(slider_block_min_tran_Y, e=True, value=block_min_tran_Y)
    cmds.floatSliderGrp(slider_block_max_tran_Y, e=True, value=block_max_tran_Y)
    cmds.floatSliderGrp(slider_block_min_tran_Z, e=True, value=block_min_tran_Z)
    cmds.floatSliderGrp(slider_block_max_tran_Z, e=True, value=block_max_tran_Z)

    cmds.floatSliderGrp(slider_block_min_rot_X, e=True, value=block_min_rot_X)
    cmds.floatSliderGrp(slider_block_max_rot_X, e=True, value=block_max_rot_X)
    cmds.floatSliderGrp(slider_block_min_rot_Y, e=True, value=block_min_rot_Y)
    cmds.floatSliderGrp(slider_block_max_rot_Y, e=True, value=block_max_rot_Y)
    cmds.floatSliderGrp(slider_block_min_rot_Z, e=True, value=block_min_rot_Z)
    cmds.floatSliderGrp(slider_block_max_rot_Z, e=True, value=block_max_rot_Z)
    
    cmds.floatSliderGrp(slider_global_min_size, e=True, value=global_min_size)
    cmds.floatSliderGrp(slider_global_max_size, e=True, value=global_max_size)
    cmds.floatSliderGrp(slider_global_min_scale_X, e=True, value=global_min_scale_X)
    cmds.floatSliderGrp(slider_global_max_scale_X, e=True, value=global_max_scale_X)
    cmds.floatSliderGrp(slider_global_min_scale_Y, e=True, value=global_min_scale_Y)
    cmds.floatSliderGrp(slider_global_max_scale_Y, e=True, value=global_max_scale_Y)
    cmds.floatSliderGrp(slider_global_min_scale_Z, e=True, value=global_min_scale_Z)
    cmds.floatSliderGrp(slider_global_max_scale_Z, e=True, value=global_max_scale_Z)

    cmds.floatSliderGrp(slider_global_min_tran_X, e=True, value=global_min_tran_X)
    cmds.floatSliderGrp(slider_global_max_tran_X, e=True, value=global_max_tran_X)
    cmds.floatSliderGrp(slider_global_min_tran_Y, e=True, value=global_min_tran_Y)
    cmds.floatSliderGrp(slider_global_max_tran_Y, e=True, value=global_max_tran_Y)
    cmds.floatSliderGrp(slider_global_min_tran_Z, e=True, value=global_min_tran_Z)
    cmds.floatSliderGrp(slider_global_max_tran_Z, e=True, value=global_max_tran_Z)

    cmds.floatSliderGrp(slider_global_min_rot_X, e=True, value=global_min_rot_X)
    cmds.floatSliderGrp(slider_global_max_rot_X, e=True, value=global_max_rot_X)
    cmds.floatSliderGrp(slider_global_min_rot_Y, e=True, value=global_min_rot_Y)
    cmds.floatSliderGrp(slider_global_max_rot_Y, e=True, value=global_max_rot_Y)
    cmds.floatSliderGrp(slider_global_min_rot_Z, e=True, value=global_min_rot_Z)
    cmds.floatSliderGrp(slider_global_max_rot_Z, e=True, value=global_max_rot_Z)

    cmds.checkBox(checkbox_hide_base_planes, e=True, value=hide_base_planes)

def copySettings(*args):
    copy_to_clipboard(getCurrentSettings())

def getCurrentSettings(*args):
    shape_ = ""
    index = cmds.radioButtonGrp(shape_selector, q=True, select=True)         
    shape_ = shapes[index-1]

    values = {
        "shape": shape_,

        "min_height": cmds.floatSliderGrp(slider_min_height, q=True, value=True),
        "max_height": cmds.floatSliderGrp(slider_max_height, q=True, value=True),
        "min_width": cmds.floatSliderGrp(slider_min_width, q=True, value=True),
        "max_width": cmds.floatSliderGrp(slider_max_width, q=True, value=True),
        "min_depth": cmds.floatSliderGrp(slider_min_depth, q=True, value=True),
        "max_depth": cmds.floatSliderGrp(slider_max_depth, q=True, value=True),

        "min_tran_X": cmds.floatSliderGrp(slider_min_tran_X, q=True, value=True),
        "max_tran_X": cmds.floatSliderGrp(slider_max_tran_X, q=True, value=True),
        "min_tran_Y": cmds.floatSliderGrp(slider_min_tran_Y, q=True, value=True),
        "max_tran_Y": cmds.floatSliderGrp(slider_max_tran_Y, q=True, value=True),
        "min_tran_Z": cmds.floatSliderGrp(slider_min_tran_Z, q=True, value=True),
        "max_tran_Z": cmds.floatSliderGrp(slider_max_tran_Z, q=True, value=True),

        "min_rot_X": cmds.floatSliderGrp(slider_min_rot_X, q=True, value=True),
        "max_rot_X": cmds.floatSliderGrp(slider_max_rot_X, q=True, value=True),
        "min_rot_Y": cmds.floatSliderGrp(slider_min_rot_Y, q=True, value=True),
        "max_rot_Y": cmds.floatSliderGrp(slider_max_rot_Y, q=True, value=True),
        "min_rot_Z": cmds.floatSliderGrp(slider_min_rot_Z, q=True, value=True),
        "max_rot_Z": cmds.floatSliderGrp(slider_max_rot_Z, q=True, value=True),

        "min_num_buildings": cmds.intSliderGrp(slider_min_num_buildings, q=True, value=True),
        "max_num_buildings": cmds.intSliderGrp(slider_max_num_buildings, q=True, value=True),
        "subdiv_w": cmds.intSliderGrp(slider_subdiv_w, q=True, value=True),
        "subdiv_h": cmds.intSliderGrp(slider_subdiv_h, q=True, value=True),
        "num_blocks_x": cmds.intSliderGrp(slider_num_blocks_x, q=True, value=True),
        "num_blocks_z": cmds.intSliderGrp(slider_num_blocks_z, q=True, value=True),

        "block_size_X": cmds.floatSliderGrp(slider_block_size_x, q=True, value=True),
        "block_size_Z": cmds.floatSliderGrp(slider_block_size_z, q=True, value=True),
        "space_between_blocks_X": cmds.floatSliderGrp(slider_space_between_blocks_x, q=True, value=True),
        "space_between_blocks_Z": cmds.floatSliderGrp(slider_space_between_blocks_z, q=True, value=True),

        "block_min_size": cmds.floatSliderGrp(slider_block_min_size, q=True, value=True),
        "block_max_size": cmds.floatSliderGrp(slider_block_max_size, q=True, value=True),
        "block_min_scale_X": cmds.floatSliderGrp(slider_block_min_scale_X, q=True, value=True),
        "block_max_scale_X": cmds.floatSliderGrp(slider_block_max_scale_X, q=True, value=True),
        "block_min_scale_Y": cmds.floatSliderGrp(slider_block_min_scale_Y, q=True, value=True),
        "block_max_scale_Y": cmds.floatSliderGrp(slider_block_max_scale_Y, q=True, value=True),
        "block_min_scale_Z": cmds.floatSliderGrp(slider_block_min_scale_Z, q=True, value=True),
        "block_max_scale_Z": cmds.floatSliderGrp(slider_block_max_scale_Z, q=True, value=True),

        "block_min_tran_X": cmds.floatSliderGrp(slider_block_min_tran_X, q=True, value=True),
        "block_max_tran_X": cmds.floatSliderGrp(slider_block_max_tran_X, q=True, value=True),
        "block_min_tran_Y": cmds.floatSliderGrp(slider_block_min_tran_Y, q=True, value=True),
        "block_max_tran_Y": cmds.floatSliderGrp(slider_block_max_tran_Y, q=True, value=True),
        "block_min_tran_Z": cmds.floatSliderGrp(slider_block_min_tran_Z, q=True, value=True),
        "block_max_tran_Z": cmds.floatSliderGrp(slider_block_max_tran_Z, q=True, value=True),

        "block_min_rot_X": cmds.floatSliderGrp(slider_block_min_rot_X, q=True, value=True),
        "block_max_rot_X": cmds.floatSliderGrp(slider_block_max_rot_X, q=True, value=True),
        "block_min_rot_Y": cmds.floatSliderGrp(slider_block_min_rot_Y, q=True, value=True),
        "block_max_rot_Y": cmds.floatSliderGrp(slider_block_max_rot_Y, q=True, value=True),
        "block_min_rot_Z": cmds.floatSliderGrp(slider_block_min_rot_Z, q=True, value=True),
        "block_max_rot_Z": cmds.floatSliderGrp(slider_block_max_rot_Z, q=True, value=True),

        "global_min_size": cmds.floatSliderGrp(slider_global_min_size, q=True, value=True),
        "global_max_size": cmds.floatSliderGrp(slider_global_max_size, q=True, value=True),
        "global_min_scale_X": cmds.floatSliderGrp(slider_global_min_scale_X, q=True, value=True),
        "global_max_scale_X": cmds.floatSliderGrp(slider_global_max_scale_X, q=True, value=True),
        "global_min_scale_Y": cmds.floatSliderGrp(slider_global_min_scale_Y, q=True, value=True),
        "global_max_scale_Y": cmds.floatSliderGrp(slider_global_max_scale_Y, q=True, value=True),
        "global_min_scale_Z": cmds.floatSliderGrp(slider_global_min_scale_Z, q=True, value=True),
        "global_max_scale_Z": cmds.floatSliderGrp(slider_global_max_scale_Z, q=True, value=True),

        "global_min_tran_X": cmds.floatSliderGrp(slider_global_min_tran_X, q=True, value=True),
        "global_max_tran_X": cmds.floatSliderGrp(slider_global_max_tran_X, q=True, value=True),
        "global_min_tran_Y": cmds.floatSliderGrp(slider_global_min_tran_Y, q=True, value=True),
        "global_max_tran_Y": cmds.floatSliderGrp(slider_global_max_tran_Y, q=True, value=True),
        "global_min_tran_Z": cmds.floatSliderGrp(slider_global_min_tran_Z, q=True, value=True),
        "global_max_tran_Z": cmds.floatSliderGrp(slider_global_max_tran_Z, q=True, value=True),

        "global_min_rot_X": cmds.floatSliderGrp(slider_global_min_rot_X, q=True, value=True),
        "global_max_rot_X": cmds.floatSliderGrp(slider_global_max_rot_X, q=True, value=True),
        "global_min_rot_Y": cmds.floatSliderGrp(slider_global_min_rot_Y, q=True, value=True),
        "global_max_rot_Y": cmds.floatSliderGrp(slider_global_max_rot_Y, q=True, value=True),
        "global_min_rot_Z": cmds.floatSliderGrp(slider_global_min_rot_Z, q=True, value=True),
        "global_max_rot_Z": cmds.floatSliderGrp(slider_global_max_rot_Z, q=True, value=True),

        "hide_base_planes": cmds.checkBox(checkbox_hide_base_planes, q=True, value=True)
    }

    lines = []
    for k, v in values.items():
        if isinstance(v, float):
            lines.append(f"{k} = {v:g}")
        elif isinstance(v, str):
            lines.append(f'{k} = "{v}"')
        else:
            lines.append(f"{k} = {v}")
    code_str = "\n".join(lines)

    return code_str

def copy_to_clipboard(text):
    system = platform.system()
    
    if system == "Windows":
        subprocess.run("clip", input=text.encode(), check=True, shell=True)
    elif system == "Darwin":  # macOS
        subprocess.run("pbcopy", input=text.encode(), check=True)
    else:  # Linux
        subprocess.run("xclip -selection clipboard", input=text.encode(), check=True, shell=True)

def get_clipboard_text():
    system = platform.system()
    
    if system == "Windows":
        return subprocess.check_output("powershell Get-Clipboard", shell=True, text=True)
    elif system == "Darwin":  # macOS
        return subprocess.check_output("pbpaste", text=True)
    else:  # Linux
        return subprocess.check_output("xclip -selection clipboard -o", shell=True, text=True)

def set_to_copied_settings(*args):
    global shape
    global min_height, max_height, min_width, max_width, min_depth, max_depth
    global min_rot_X, max_rot_X, min_rot_Y, max_rot_Y, min_rot_Z, max_rot_Z
    global min_tran_X, max_tran_X, min_tran_Y, max_tran_Y, min_tran_Z, max_tran_Z
    global min_num_buildings, max_num_buildings, subdiv_w, subdiv_h
    global num_blocks_x, num_blocks_z, block_size_X, block_size_Z, space_between_blocks_X, space_between_blocks_Z
    global block_min_size, block_max_size
    global block_min_scale_X, block_max_scale_X, block_min_scale_Y, block_max_scale_Y, block_min_scale_Z, block_max_scale_Z
    global block_min_rot_X, block_max_rot_X, block_min_rot_Y, block_max_rot_Y, block_min_rot_Z, block_max_rot_Z
    global block_min_tran_X, block_max_tran_X, block_min_tran_Y, block_max_tran_Y, block_min_tran_Z, block_max_tran_Z
    global global_min_size, global_max_size, global_min_scale_X, global_max_scale_X, global_min_scale_Y, global_max_scale_Y, global_min_scale_Z, global_max_scale_Z
    global global_min_tran_X, global_max_tran_X, global_min_tran_Y, global_max_tran_Y, global_min_tran_Z, global_max_tran_Z
    global global_min_rot_X, global_max_rot_X, global_min_rot_Y, global_max_rot_Y, global_min_rot_Z, global_max_rot_Z
    global hide_base_planes

    try:
        raw = get_clipboard_text()
        
        exec(raw, globals())

        update_all_sliders()
        generate_city()

        print("✔ Settings successfully applied from clipboard.")

    except Exception as e:
        cmds.warning(f"Failed to apply settings: {e}")



# create/delete tabs ---------------------
def delete_all_gen_tabs():
    global save_gen

    # Loop over a copy so dictionary can be modified safely
    for gen_num in list(generations.keys()):
        if gen_num in save_gen:
            continue
        
        else:
            # Delete generation group in the scene
            g = generations[gen_num]
            if cmds.objExists(g):
                cmds.delete(g)

            # Delete UI tab
            if gen_num in gen_tabs:
                if cmds.control(gen_tabs[gen_num], exists=True):
                    cmds.deleteUI(gen_tabs[gen_num])

                del gen_tabs[gen_num]

            # Remove entry from the dictionary
            del generations[gen_num]

def create_generation_tab(gen_num):
    global num_blocks_x, num_blocks_z, save_gen
    
    # Make sure new tab is created inside the tabLayout
    cmds.setParent(tabs) #tells maya that any new UI elements created will be children of the tabs tabLayout 

    child_tab = cmds.columnLayout(adj=True) # create new tab
    gen_tabs[gen_num] = child_tab  # key = gen_number, value = UI tab layout

    cmds.tabLayout(tabs, edit=True, tabLabel=(child_tab, f"GEN{gen_num}"))
    


    # BUTTON SECTION -------------------------------------------------------------------------------------
    # Save button
    cmds.columnLayout(adj=True, columnAlign="center")
    save_button[gen_num] = cmds.button(label="Save This Generation", command=lambda g: save_generation(gen_num), height=28, width=400, bgc=green_color)
    cmds.setParent("..")

    # Delete button
    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Delete This Generation", command=lambda g: delete_gen(gen_num), height=28, width=400, bgc=red_color)
    cmds.setParent("..")

    # Hide button
    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Hide This Generation", command=lambda g: hide_gen(gen_num), height=28, width=400, bgc=sub_color)
    cmds.setParent("..")

    # Show button
    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Show This Generation", command=lambda g: show_gen(gen_num), height=28, width=400, bgc=sub_color)
    cmds.setParent("..")

    # Copy initial gen settings
    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Copy Initial Settings to Clipboard", command=lambda g: copy_initial_settings(gen_num), height=28, width=400, bgc=sub_color)
    cmds.setParent("..")

    # Copy gen modify settings?



    # MODIFY SECTION -------------------------------------------------------------------------------------
    cmds.separator(height=4, style="single")
    cmds.separator(height=6, style="none")  # just blank space
    cmds.text(label=" Modify", align="left", font="boldLabelFont", height=20)
    cmds.separator(height=10, style="none")

    all_buildings = cmds.ls(f"GEN{gen_num}___block*_*_building*") #all buildings in this generation
    all_buildings = [b for b in all_buildings if "Shape" not in b] #removes all shape nodes

    """for building in all_buildings:  
        cmds.rotate(90, 0, 0, building, relative=True)"""

    for i in range(1, num_blocks_x + 1):      # i goes 1 → num_blocks_x
        for j in range(1, num_blocks_z + 1):  # j goes 1 → num_blocks_z
            pattern = f"GEN{gen_num}___block{i}_{j}_building*"
            all_buildings_in_block = cmds.ls(pattern) #all buildings per block in this generation
            all_buildings_in_block = [b for b in all_buildings_in_block if "Shape" not in b] #removes all shape nodes

    settings = gen_settings[gen_num]
    #valueX = settings["global_scaleX"]

    # general settings
    cmds.frameLayout(
        label="General Settings",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )    

    #per individual duplicate checkbox
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(115, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_mod_indiv_duplicate[gen_num] = cmds.checkBox(
        label="Scale and rotate per gen duplicate",
        value=False,
        changeCommand=lambda v, g=gen_num: mod_per_dup(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    #per individual block checkbox
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(115, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_mod_indiv_block[gen_num] = cmds.checkBox(
        label="Scale and rotate per block",
        value=False,
        changeCommand=lambda v, g=gen_num: mod_per_block(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    #per individual building checkbox
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(115, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_mod_indiv_building[gen_num] = cmds.checkBox(
        label="Scale and rotate per building",
        value=False,
        changeCommand=lambda v, g=gen_num: mod_per_building(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')
    cmds.setParent('..') #sub tab
 
    # global transform
    cmds.frameLayout(
        label="Global Transform",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )

    # translate global ---------------------------------------
    cmds.columnLayout(adj=True, rowSpacing=0)   # <– controls spacing between frames
    cmds.frameLayout(
        label="Translate",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=subsub_color,
        mw=5, mh=5
    )

    gen_slider_tranX_global[gen_num] = cmds.floatSliderGrp(
        label="Translate X",
        field=True,
        minValue=-100,
        maxValue=100,
        value=settings["global_tranX"],
        changeCommand=lambda v, g=gen_num: update_gen_tranX(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_tranY_global[gen_num] = cmds.floatSliderGrp(
        label="Translate Y",
        field=True,
        minValue=-100,
        maxValue=100,
        value=settings["global_tranY"],
        changeCommand=lambda v, g=gen_num: update_gen_tranY(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_tranZ_global[gen_num] = cmds.floatSliderGrp(
        label="Translate Z",
        field=True,
        minValue=-100,
        maxValue=100,
        value=settings["global_tranZ"],
        changeCommand=lambda v, g=gen_num: update_gen_tranZ(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..') #sub tab

    # scale global ----------------------------------------- 
    cmds.frameLayout(
        label="Scale",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=subsub_color,
        mw=5, mh=5
    )
    
    gen_slider_size_global[gen_num] = cmds.floatSliderGrp(
        label="Size",
        field=True,
        minValue=-20,
        maxValue=20,
        value=settings["global_scale"],
        changeCommand=lambda v, g=gen_num: update_gen_scale_global(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_scaleX_global[gen_num] = cmds.floatSliderGrp(
        label="Scale X",
        field=True,
        minValue=-20,
        maxValue=20,
        value=settings["global_scaleX"],
        changeCommand=lambda v, g=gen_num: update_gen_scaleX(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_scaleY_global[gen_num] = cmds.floatSliderGrp(
        label="Scale Y",
        field=True,
        minValue=-20,
        maxValue=20,
        value=settings["global_scaleY"],
        changeCommand=lambda v, g=gen_num: update_gen_scaleY(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_scaleZ_global[gen_num] = cmds.floatSliderGrp(
        label="Scale Z",
        field=True,
        minValue=-20,
        maxValue=20,
        value=settings["global_scaleZ"],
        changeCommand=lambda v, g=gen_num: update_gen_scaleZ(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..')

    # rotate global ----------------------------------------- 
    cmds.frameLayout(
        label="Rotate",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=subsub_color,
        mw=5, mh=5
    )

    gen_slider_rotX_global[gen_num] = cmds.floatSliderGrp(
        label="Rotate X",
        field=True,
        minValue=-180,
        maxValue=180,
        value=settings["global_rotX"],
        changeCommand=lambda v, g=gen_num: update_gen_rotX(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_rotY_global[gen_num] = cmds.floatSliderGrp(
        label="Rotate Y",
        field=True,
        minValue=-180,
        maxValue=180,
        value=settings["global_rotY"],
        changeCommand=lambda v, g=gen_num: update_gen_rotY(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_rotZ_global[gen_num] = cmds.floatSliderGrp(
        label="Rotate Z",
        field=True,
        minValue=-180,
        maxValue=180,
        value=settings["global_rotZ"],
        changeCommand=lambda v, g=gen_num: update_gen_rotZ(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..') #sub tab
    cmds.setParent('..') #tab
    cmds.setParent('..')

    # hide base planes ---------------------------------------
    cmds.frameLayout(
        label="Base Plane",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(150, 150, 150))
    cmds.separator(style="none")   # left empty space

    gen_checkbox_hide_planes[gen_num] = cmds.checkBox(
        label="Hide Base Plane",
        value=False,
        changeCommand=lambda v, g=gen_num: update_hide_base_planes(g, v),
    )

    cmds.separator(style="none")   # right empty space
    cmds.setParent("..")

    cmds.setParent('..') #tab

    #reset to initial state
    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Reset to Initial State", command=lambda g: reset_initial_state(gen_num), bgc=sub_color)
    cmds.setParent("..")



    # DUPLICATE SECTION ------------------------------------------------------------------------------------
    cmds.separator(height=5, style="none")  # just blank space
    cmds.separator(height=20, style="single")  # just blank space

    cmds.text(label=" Duplicate", align="left", font="boldLabelFont")
    cmds.separator(height=10, style="none")
    
    #general settings
    cmds.frameLayout(
        label="General Settings",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )    

    #iterations
    gen_slider_dup_iterations[gen_num] = cmds.intSliderGrp(
        label="Iterations",
        field=True,
        minValue=1,
        maxValue=50,
        value=1,
        changeCommand=lambda v, g=gen_num: dup_iterations(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    #per prior duplicate checkbox
    """
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_prior_dup[gen_num] = cmds.checkBox(
        label="Scale and rotate per prior duplicate",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_per_prior_dup(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')
    """
    
    #per individual duplicate checkbox
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_indiv_dup[gen_num] = cmds.checkBox(
        label="Scale and rotate per gen duplicate",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_per_dup(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    #per individual block checkbox
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_indiv_block[gen_num] = cmds.checkBox(
        label="Scale and rotate per block",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_per_block(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    #per individual building checkbox
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 250, 130))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_indiv_building[gen_num] = cmds.checkBox(
        label="Scale and rotate per building",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_per_building(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    cmds.setParent('..')

    #scale
    cmds.frameLayout(
        label="Scale",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 200, 150))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_scale_mult[gen_num] = cmds.checkBox(
        label="Set Scale to Multiplicative Offset",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_multiplicative_scale(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    gen_slider_dup_size[gen_num] = cmds.floatSliderGrp(
        label="Size",
        field=True,
        minValue=0.1,
        maxValue=50,
        value=1,
        changeCommand=lambda v, g=gen_num: dup_size(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_scaleX[gen_num] = cmds.floatSliderGrp(
        label="Scale (X)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=1,
        changeCommand=lambda v, g=gen_num: dup_scale_x(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_scaleY[gen_num] = cmds.floatSliderGrp(
        label="Scale (Y)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=1,
        changeCommand=lambda v, g=gen_num: dup_scale_y(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_scaleZ[gen_num] = cmds.floatSliderGrp(
        label="Scale (Z)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=1,
        changeCommand=lambda v, g=gen_num: dup_scale_z(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..') #tab

    #translate
    cmds.frameLayout(
        label="Translate",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 200, 150))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_tran_add[gen_num] = cmds.checkBox(
        label="Set Translate to Additive Offset",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_additive_translate(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    gen_slider_dup_tranX[gen_num] = cmds.floatSliderGrp(
        label="Translate (X)",
        field=True,
        minValue=-500,
        maxValue=500,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_tran_x(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_tranY[gen_num] = cmds.floatSliderGrp(
        label="Translate (Y)",
        field=True,
        minValue=-500,
        maxValue=500,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_tran_y(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_tranZ[gen_num] = cmds.floatSliderGrp(
        label="Translate (Z)",
        field=True,
        minValue=-500,
        maxValue=500,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_tran_z(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..') #tab

    #rotate
    cmds.frameLayout(
        label="Rotate",
        collapsable=True,
        collapse=True,        # set False if you want it open by default
        bgc=sub_color,
        mw=5, mh=5
    )

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(101, 200, 150))
    cmds.separator(style="none")   # left empty space
    gen_checkbox_dup_rot_add[gen_num] = cmds.checkBox(
        label="Set Rotate to Additive Offset",
        value=False,
        changeCommand=lambda v, g=gen_num: dup_additive_rotate(g, v),
    )
    cmds.separator(style="none")
    cmds.setParent('..')

    gen_slider_dup_rotX[gen_num] = cmds.floatSliderGrp(
        label="Rotate (X)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_rot_x(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_rotY[gen_num] = cmds.floatSliderGrp(
        label="Rotate (Y)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_rot_y(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    gen_slider_dup_rotZ[gen_num] = cmds.floatSliderGrp(
        label="Rotate (Z)",
        field=True,
        minValue=-50,
        maxValue=50,
        value=0,
        changeCommand=lambda v, g=gen_num: dup_rot_z(g, v),
        columnWidth=[(1, 100), (2, 100), (3, 50)]  # optional: adjust label, slider, field widths
    )

    cmds.setParent('..') #tab

    cmds.columnLayout(adj=True, columnAlign="center")
    cmds.button(label="Reset Duplicate Settings", command=lambda g: reset_duplicate_settings(gen_num), bgc=sub_color)
    cmds.separator(height=2, style="none")  # just blank space

    cmds.button(label="Duplicate", command=lambda g: duplicate(gen_num), bgc=sub_color)
    cmds.setParent("..")



    # MIRROR SECTION --------------------------------------------------------------------------------------
    cmds.separator(height=5, style="none")  # just blank space
    cmds.separator(height=20, style="single")  # just blank space

    cmds.text(label=" Mirror", align="left", font="boldLabelFont")
    cmds.separator(height=10, style="none")

    #modify individual buildings (translate/rotate/scale)
    #modify buildings per block (translate/rotate/scale)

    #modify block (translate/rotate/scale)
    #modify block size and space between blocks
    #hide block buildings/show block buildings
    #hide block base plane/show block base plane

    #modify global (translate/rotate/scale)
    #hide buildings/show buildings
    #hide base planes/show base planes
    
    #duplicate
    #mirror

def default_gen_settings(default_settings, gen_num):
    global initial_gen_settings

    if default_settings == {}:
        initial_gen_settings[gen_num] = {
            #modify section
            "building_sizes": {},
            "building_rots": {},
            "mod_per_individual_building": False,

            "block_sizes": {},
            "block_rots": {},
            "mod_per_individual_block": False,

            "duplicate_sizes": {
                "1": [1, 1, 1], 
            },
            "duplicate_rots": {
                "1": [0, 0, 0], 
            },
            "mod_per_individual_duplicate": False,

            "global_sizes": {
                "1": [1, 1, 1], 
            },
            "global_rots": {
                "1": [0, 0, 0], 
            },

            "global_tranX": 0,
            "global_tranY": 0,
            "global_tranZ": 0,

            "global_scale": 1,
            "global_scaleX": 1,
            "global_scaleY": 1,
            "global_scaleZ": 1,

            "global_rotX": 0,
            "global_rotY": 0,
            "global_rotZ": 0,

            "hide_base_planes": False,

            #duplicate section
            "iterations": 1,
            "per_prior_dup": False,
            "per_individual_dup": False,
            "per_individual_block": False,
            "per_individual_building": False,

            "multiplicative_scale": False,
            "additive_scale": False,
            "additive_translate": False,
            "additive_rotate": False,

            "size": 1,
            "scale_x": 1,
            "scale_y": 1,
            "scale_z": 1,

            "tran_x": 0,
            "tran_y": 0,
            "tran_z": 0,

            "rot_x": 0,
            "rot_y": 0,
            "rot_z": 0
        }
        return {
            #modify section
            "building_sizes": {},
            "building_rots": {},
            "mod_per_individual_building": False,

            "block_sizes": {},
            "block_rots": {},
            "mod_per_individual_block": False,

            "duplicate_sizes": {
                "1": [1, 1, 1], 
            },
            "duplicate_rots": {
                "1": [0, 0, 0], 
            },
            "mod_per_individual_duplicate": False,

            "global_sizes": {
                "1": [1, 1, 1], 
            },
            "global_rots": {
                "1": [0, 0, 0], 
            },

            "global_tranX": 0,
            "global_tranY": 0,
            "global_tranZ": 0,

            "global_scale": 1,
            "global_scaleX": 1,
            "global_scaleY": 1,
            "global_scaleZ": 1,

            "global_rotX": 0,
            "global_rotY": 0,
            "global_rotZ": 0,

            "hide_base_planes": False,

            #duplicate section
            "iterations": 1,
            "per_prior_dup": False,
            "per_individual_dup": False,
            "per_individual_block": False,
            "per_individual_building": False,

            "multiplicative_scale": False,
            "additive_scale": False,
            "additive_translate": False,
            "additive_rotate": False,

            "size": 1,
            "scale_x": 1,
            "scale_y": 1,
            "scale_z": 1,

            "tran_x": 0,
            "tran_y": 0,
            "tran_z": 0,

            "rot_x": 0,
            "rot_y": 0,
            "rot_z": 0
        }
    
    else:
        initial_gen_settings[gen_num] = {
            #modify section
            "building_sizes": default_settings["buildingSizes"],
            "building_rots": default_settings["buildingRots"],
            "mod_per_individual_building": False,

            "block_sizes": default_settings["blockSizes"],
            "block_rots": default_settings["blockRots"],
            "mod_per_individual_block": False,

            "duplicate_sizes": default_settings["duplicateSizes"],
            "duplicate_rots": default_settings["duplicateRots"],
            "mod_per_individual_duplicate": False,

            "global_sizes": default_settings["globalSizes"],
            "global_rots": default_settings["globalRots"],

            "global_tranX": 0,
            "global_tranY": 0,
            "global_tranZ": 0,

            "global_scale": 1,
            "global_scaleX": 1,
            "global_scaleY": 1,
            "global_scaleZ": 1,

            "global_rotX": 0,
            "global_rotY": 0,
            "global_rotZ": 0,

            "hide_base_planes": default_settings["hideBasePlanes"],

            #duplicate section
            "iterations": 1,
            "per_prior_dup": False,
            "per_individual_dup": False,
            "per_individual_block": False,
            "per_individual_building": False,

            "multiplicative_scale": False,
            "additive_scale": False,
            "additive_translate": False,
            "additive_rotate": False,

            "size": 1,
            "scale_x": 1,
            "scale_y": 1,
            "scale_z": 1,

            "tran_x": 0,
            "tran_y": 0,
            "tran_z": 0,

            "rot_x": 0,
            "rot_y": 0,
            "rot_z": 0
        }
        return {
            #modify section
            "building_sizes": default_settings["buildingSizes"],
            "building_rots": default_settings["buildingRots"],
            "mod_per_individual_building": False,

            "block_sizes": default_settings["blockSizes"],
            "block_rots": default_settings["blockRots"],
            "mod_per_individual_block": False,

            "duplicate_sizes": default_settings["duplicateSizes"],
            "duplicate_rots": default_settings["duplicateRots"],
            "mod_per_individual_duplicate": False,

            "global_sizes": default_settings["globalSizes"],
            "global_rots": default_settings["globalRots"],
            
            "global_tranX": 0,
            "global_tranY": 0,
            "global_tranZ": 0,

            "global_scale": 1,
            "global_scaleX": 1,
            "global_scaleY": 1,
            "global_scaleZ": 1,

            "global_rotX": 0,
            "global_rotY": 0,
            "global_rotZ": 0,

            "hide_base_planes": default_settings["hideBasePlanes"],

            #duplicate section
            "iterations": 1,
            "per_prior_dup": False,
            "per_individual_dup": False,
            "per_individual_block": False,
            "per_individual_building": False,

            "multiplicative_scale": False,
            "additive_scale": False,
            "additive_translate": False,
            "additive_rotate": False,

            "size": 1,
            "scale_x": 1,
            "scale_y": 1,
            "scale_z": 1,

            "tran_x": 0,
            "tran_y": 0,
            "tran_z": 0,

            "rot_x": 0,
            "rot_y": 0,
            "rot_z": 0
        }

def reset_initial_state(gen_num):
    buildingSizes = initial_gen_settings[gen_num]["building_sizes"]
    buildingRots = initial_gen_settings[gen_num]["building_rots"]
    #mp_bu = initial_gen_settings[gen_num]["mod_per_individual_building"]

    blockSizes = initial_gen_settings[gen_num]["block_sizes"]
    blockRots = initial_gen_settings[gen_num]["block_rots"]
    #mp_bl = initial_gen_settings[gen_num]["mod_per_individual_block"]

    duplicateSizes = initial_gen_settings[gen_num]["duplicate_sizes"]
    duplicateRots = initial_gen_settings[gen_num]["duplicate_rots"]

    globalSizes = initial_gen_settings[gen_num]["global_sizes"]
    globalRots = initial_gen_settings[gen_num]["global_rots"]

    h = initial_gen_settings[gen_num]["hide_base_planes"]

    #cmds.checkBox(gen_checkbox_mod_indiv_building[gen_num], e=True, value=mp_bu)
    #cmds.checkBox(gen_checkbox_mod_indiv_block[gen_num], e=True, value=mp_bl)

    cmds.floatSliderGrp(gen_slider_tranX_global[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_tranY_global[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_tranZ_global[gen_num], e=True, value=0)

    cmds.floatSliderGrp(gen_slider_size_global[gen_num],  e=True, value=1)
    cmds.floatSliderGrp(gen_slider_scaleX_global[gen_num], e=True, value=1)
    cmds.floatSliderGrp(gen_slider_scaleY_global[gen_num], e=True, value=1)
    cmds.floatSliderGrp(gen_slider_scaleZ_global[gen_num], e=True, value=1)

    cmds.floatSliderGrp(gen_slider_rotX_global[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_rotY_global[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_rotZ_global[gen_num], e=True, value=0)
    cmds.checkBox(gen_checkbox_hide_planes[gen_num], e=True, value=h)

    update_gen_tranX(gen_num, 0)
    update_gen_tranY(gen_num, 0)
    update_gen_tranZ(gen_num, 0)

    update_gen_scale_global(gen_num, 1)
    update_gen_scaleX(gen_num, 1)
    update_gen_scaleY(gen_num, 1)
    update_gen_scaleZ(gen_num, 1)

    update_gen_rotX(gen_num, 0)
    update_gen_rotY(gen_num, 0)
    update_gen_rotZ(gen_num, 0)

    reset_gen_building_sizes(gen_num, buildingSizes)
    reset_gen_building_rots(gen_num, buildingRots)
    #mod_per_building(gen_num, mp_bu)

    reset_gen_block_sizes(gen_num, blockSizes)
    reset_gen_block_rots(gen_num, blockRots)
    #mod_per_block(gen_num, mp_bl)

    reset_gen_duplicate_sizes(gen_num, duplicateSizes)
    reset_gen_duplicate_rots(gen_num, duplicateRots)

    reset_gen_size(gen_num, globalSizes)
    reset_gen_rot(gen_num, globalRots)

    reset_base_planes_visibility(gen_num, h)

def reset_duplicate_settings(gen_num):
    cmds.intSliderGrp(gen_slider_dup_iterations[gen_num], e=True, value=1)
    #cmds.checkBox(gen_checkbox_dup_prior_dup[gen_num], e=True, value=False)
    cmds.checkBox(gen_checkbox_dup_indiv_dup[gen_num], e=True, value=False)
    cmds.checkBox(gen_checkbox_dup_indiv_block[gen_num], e=True, value=False)
    cmds.checkBox(gen_checkbox_dup_indiv_building[gen_num], e=True, value=False)

    #cmds.checkBox(gen_checkbox_dup_scale_add[gen_num], e=True, value=False)
    cmds.checkBox(gen_checkbox_dup_scale_mult[gen_num], e=True, value=False)
    cmds.floatSliderGrp(gen_slider_dup_size[gen_num],  e=True, value=1)
    cmds.floatSliderGrp(gen_slider_dup_scaleX[gen_num], e=True, value=1)
    cmds.floatSliderGrp(gen_slider_dup_scaleY[gen_num], e=True, value=1)
    cmds.floatSliderGrp(gen_slider_dup_scaleZ[gen_num], e=True, value=1)

    cmds.checkBox(gen_checkbox_dup_tran_add[gen_num], e=True, value=False)
    cmds.floatSliderGrp(gen_slider_dup_tranX[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_dup_tranY[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_dup_tranZ[gen_num], e=True, value=0)

    cmds.checkBox(gen_checkbox_dup_rot_add[gen_num], e=True, value=False)
    cmds.floatSliderGrp(gen_slider_dup_rotX[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_dup_rotY[gen_num], e=True, value=0)
    cmds.floatSliderGrp(gen_slider_dup_rotZ[gen_num], e=True, value=0)

    dup_iterations(gen_num, 1)
    #dup_per_prior_dup(gen_num, False)
    dup_per_dup(gen_num, False)
    dup_per_block(gen_num, False)
    dup_per_building(gen_num, False)

    dup_additive_scale(gen_num, False)
    dup_multiplicative_scale(gen_num, False)
    dup_size(gen_num, 1)
    dup_scale_x(gen_num, 1)
    dup_scale_y(gen_num, 1)
    dup_scale_z(gen_num, 1)

    dup_additive_translate(gen_num, False)
    dup_tran_x(gen_num, 0)
    dup_tran_y(gen_num, 0)
    dup_tran_z(gen_num, 0)

    dup_additive_rotate(gen_num, False)
    dup_rot_x(gen_num, 0)
    dup_rot_y(gen_num, 0)
    dup_rot_z(gen_num, 0)



# Tab buttons ----------------------------
def save_generation(gen_num, *args):
    save_gen.add(gen_num)
    cmds.button(save_button[gen_num], e=True, label="Generation is Saved", command="", bgc=green_color2, height=20, enable=False)

def delete_gen(gen_num, *args):
    g = generations.get(gen_num)
    if g and cmds.objExists(g):
        cmds.delete(g)

    # Delete UI tab
    if gen_num in gen_tabs:
        if cmds.control(gen_tabs[gen_num], exists=True):
            cmds.deleteUI(gen_tabs[gen_num])
        del gen_tabs[gen_num]

    # Fully remove generation entry
    if gen_num in generations:
        del generations[gen_num]

    #if was a saved gen, remove gen index from save_gen set
    if gen_num in save_gen:
        save_gen.remove(gen_num)

def hide_gen(gen_num, *args):
    g = generations[gen_num]
    if cmds.objExists(g):
        cmds.hide(g)

def show_gen(gen_num, *args):
    g = generations[gen_num]
    if cmds.objExists(g):
        cmds.showHidden(g)

def copy_initial_settings(gen_num, *args):
    if gen_num in gen_clipboard:
        copy_to_clipboard(gen_clipboard[gen_num])
    else: 
        cmds.warning("Settings are no longer available for copy")

def duplicate(gen_num, *args):
    global gen_settings
    g = generations[gen_num]

    buildingSizes = gen_settings[gen_num]["building_sizes"]
    buildingRots = gen_settings[gen_num]["building_rots"]
    blockSizes = gen_settings[gen_num]["block_sizes"]
    blockRots = gen_settings[gen_num]["block_rots"]
    duplicateSizes = gen_settings[gen_num]["duplicate_sizes"]
    duplicateRots = gen_settings[gen_num]["duplicate_rots"]

    size = gen_settings[gen_num]["size"]
    scaleX = gen_settings[gen_num]["scale_x"]
    scaleY = gen_settings[gen_num]["scale_y"]
    scaleZ = gen_settings[gen_num]["scale_z"]
    tranX = gen_settings[gen_num]["tran_x"]
    tranY = gen_settings[gen_num]["tran_y"]
    tranZ = gen_settings[gen_num]["tran_z"]
    rotX = gen_settings[gen_num]["rot_x"]
    rotY = gen_settings[gen_num]["rot_y"]
    rotZ = gen_settings[gen_num]["rot_z"]


    pivot_pos = cmds.xform(g, q=True, ws=True, rp=True)  # "rp" = rotate pivot
    #cmds.xform(g, cp=True) # moves both rotate and scale pivots

    #if it's the first duplication, put all blocks into dup1
    first_dup = False
    children = cmds.listRelatives(g)
    if ("block" in children[0]):
        first_dup = True
        kids = cmds.listRelatives(children[0])
        basePlane = [c for c in kids if "basePlane" in c][0] 
        px, py, pz = cmds.xform(basePlane, q=True, ws=True, rp=True)   

        dup1_grp = cmds.group(children, name=f"{g}_dup1")
        cx, cy, cz = cmds.xform(dup1_grp, q=True, ws=True, rp=True) 
        cmds.xform(dup1_grp, ws=True, piv=[cx, py, cz]) #move group pivot to base line

    #else, put all existing duplicates into dup1, and increment their names by 1_
    else:
        childrenX = cmds.listRelatives(g, fullPath=True, type="transform", allDescendents=True)
        children = [c for c in childrenX if "block" not in c]

        dup_gen_list = []
        for dup_gen in children:
            dup_gen_name = dup_gen.split("|")[-1]
            pre = dup_gen_name.split("dup")[0]
            post = dup_gen_name.split("dup")[1]
            new_name = pre + "dup1_" + post

            renamed = cmds.rename(dup_gen, new_name) 

            if len(post) <= 1: #if it's one of the main dup groups (dup1, dup2, dup3... not any of their subgroups)
                dup_gen_list.append(renamed)
        
        dup1_grp = cmds.group(empty=True, name=f"{g}_dup1", parent=g)

        for dup in dup_gen_list:
            cmds.parent(dup, dup1_grp)



    for i in range(gen_settings[gen_num]["iterations"]):
        obj = cmds.group(empty=True, name=f"{g}_dup{i+2}", parent=g)

        children = cmds.listRelatives(dup1_grp, type="transform", fullPath=True)

        for grp in children: #duplicate
            if ("block" in grp):
                grp_dup = cmds.duplicate(grp, rr=True)[0]
                cmds.parent(grp_dup, obj)
                cmds.rename(grp_dup, grp_dup[:-1])
        
            else:   
                short = grp.split("|")[-1]
                parts = short.split("_")  # ["GEN1", "GRP", "dup1", "3"]
                parts[2] = "dup" + str(i + 2)
                new_short = "_".join(parts)

                grp_dup = cmds.duplicate(grp, rr=True, name=new_short)[0]

                cmds.parent(grp_dup, obj)

        all_childrenX = cmds.listRelatives(obj, fullPath=True, type="transform", allDescendents=True)
        all_children = [c for c in all_childrenX if "block" not in c]

        for gp in all_children: #rename
            short = gp.split("|")[-1]                     # get short name only
            parts = short.split("_")                      # ["GEN1", "GRP", "dup1", "3"]
            parts[2] = "dup" + str(i + 2) # replace the dup number
            new_short = "_".join(parts)

            cmds.rename(gp, new_short)

        """
        obj_pre_rename = cmds.duplicate(g, rr=True)[0]
        obj = cmds.rename(obj_pre_rename, f"{g}_dup{i+2}")
        """   

        cmds.move(tranX, tranY, tranZ, obj, relative=True)

        #center pivot of gen, but keep it at base line
        px, py, pz = cmds.xform(g, q=True, ws=True, rp=True)    
        cmds.xform(g, cp=True) # moves both the rotate and scale pivots to the geometric center of the object or group
        cx, cy, cz = cmds.xform(g, q=True, ws=True, rp=True)  
        cmds.xform(g, ws=True, piv=[cx, py, cz]) # moves both rotate and scale pivots
     
        #center pivot of main dup groups (direct children of gen), but keep it at base line
        main_dups = cmds.listRelatives(g, fullPath=True)
        for main_dp in main_dups:
            px, py, pz = cmds.xform(main_dp, q=True, ws=True, rp=True)    
            cmds.xform(main_dp, cp=True) 
            cx, cy, cz = cmds.xform(main_dp, q=True, ws=True, rp=True)  
            cmds.xform(main_dp, ws=True, piv=[cx, py, cz]) 



        #scale/rotate by building
        if (gen_settings[gen_num]["per_individual_building"] == True): 
            children = cmds.listRelatives(obj, allDescendents=True, type="transform", fullPath=True) or []
            buildings = [c for c in children if "building" in c]

            for b in buildings:
                short = b.split("|")[-1]
                parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
                grandparent_group = cmds.listRelatives(parent_group, parent=True, fullPath=True)[0]
        
                dup_index = grandparent_group.split("dup")[-1].split("|")[0]
      
                if dup_index not in buildingSizes:
                    buildingSizes[dup_index] = {}
                    buildingRots[dup_index] = {}

                cmds.scale(scaleX * size, scaleY * size, scaleZ * size, b, relative=True)
                cmds.rotate(rotX, rotY, rotZ, b, relative=True)

                buildingSizes[dup_index][short] = [cmds.getAttr(f"{b}.scaleX"), cmds.getAttr(f"{b}.scaleY"), cmds.getAttr(f"{b}.scaleZ")]
                buildingRots[dup_index][short] = [cmds.getAttr(f"{b}.rotateX"), cmds.getAttr(f"{b}.rotateY"), cmds.getAttr(f"{b}.rotateZ")]

        else: 
            #scale/rotate by block
            if (gen_settings[gen_num]["per_individual_block"] == True):
                children = cmds.listRelatives(obj, allDescendents=True, type="transform", fullPath=True) or []
                block_groups = [c for c in children if "block" in c and c.split("|")[-1].endswith("_GRP")]

                for grp in block_groups:
                    short = grp.split("|")[-1]
                    parent_group = cmds.listRelatives(grp, parent=True, fullPath=True)[0]
    
                    dup_index = parent_group.split("dup")[-1].split("|")[0]

                    if dup_index not in blockSizes:
                        blockSizes[dup_index] = {}
                        blockRots[dup_index] = {}
                    
                    cmds.scale(scaleX * size, scaleY * size, scaleZ * size, grp, relative=True)
                    cmds.rotate(rotX, rotY, rotZ, grp, relative=True)

                    blockSizes[dup_index][short] = [cmds.getAttr(f"{grp}.scaleX"), cmds.getAttr(f"{grp}.scaleY"), cmds.getAttr(f"{grp}.scaleZ")]
                    blockRots[dup_index][short] = [cmds.getAttr(f"{grp}.rotateX"), cmds.getAttr(f"{grp}.rotateY"), cmds.getAttr(f"{grp}.rotateZ")]

            else:
                #scale/rotate by dup gens
                if (gen_settings[gen_num]["per_individual_dup"] == True):
                    direct_children = cmds.listRelatives(obj, fullPath=True) or []
                    children = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []

                    duplicates = []
                    for c in direct_children:
                        if "block" in c and c.split("|")[-1].endswith("_GRP"): #obj is dup2/dup3/... and its child is a block group
                            duplicates.append(obj)
                            break
                    
                    if len(duplicates) == 0: #obj is dup2/dup3/... and its child is a dup2_1/...
                        for c in children: 
                            child = cmds.listRelatives(c)
                            if child:
                                first_child = child[0]
                                if "block" in first_child and first_child.split("|")[-1].endswith("_GRP"): #if it's one of the last depth duplicates (i.e. dup2_1_1_2 if u performed 4 duplicates)
                                    duplicates.append(c)

                    for d in duplicates:  
                        """
                        dup_index = d.split("dup")[-1].split("|")[0]
                        
                        if dup_index not in duplicateSizes:
                            duplicateSizes[dup_index] = {}
                            duplicateRots[dup_index] = {}
                        """

                        cmds.scale(scaleX * size, scaleY * size, scaleZ * size, d, relative=True)
                        cmds.rotate(rotX, rotY, rotZ, d, relative=True)

                        """
                        duplicateSizes[dup_index] = [cmds.getAttr(f"{d}.scaleX"), cmds.getAttr(f"{d}.scaleY"), cmds.getAttr(f"{d}.scaleZ")]
                        duplicateRots[dup_index] = [cmds.getAttr(f"{d}.rotateX"), cmds.getAttr(f"{d}.rotateY"), cmds.getAttr(f"{d}.rotateZ")]
                        """

                    """ #would need to indent this whole block backwards of one tab
                    else:
                        #scale/rotate by prior dups
                        if (gen_settings[gen_num]["per_prior_dup"] == True):
                            children = cmds.listRelatives(obj, fullPath=True) or []
                            duplicates = [c for c in children if True]

                            for d in duplicates:
                                cmds.scale(scaleX * size, scaleY * size, scaleZ * size, d, relative=True)
                                cmds.rotate(rotX, rotY, rotZ, d, relative=True)
                    """

                else:
                    #scale/rotate by whole gen
                    cmds.scale(scaleX * size, scaleY * size, scaleZ * size, obj, relative=True)
                    cmds.rotate(rotX, rotY, rotZ, obj, relative=True)

                    """
                    direct_children = cmds.listRelatives(obj, fullPath=True) or []
                    children = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []

                    duplicates = []
                    for c in direct_children:
                        if "block" in c and c.split("|")[-1].endswith("_GRP"): #obj is dup2/dup3/... and its child is a block group
                            duplicates.append(obj)
                            break
                    
                    if len(duplicates) == 0: #obj is dup2/dup3/... and its child is a dup2_1/...
                        for c in children: 
                            child = cmds.listRelatives(c)
                            if child:
                                first_child = child[0]
                                if "block" in first_child and first_child.split("|")[-1].endswith("_GRP"): #if it's one of the last depth duplicates (i.e. dup2_1_1_2 if u performed 4 duplicates)
                                    duplicates.append(c)

                    for d in duplicates:  
                        dup_index = d.split("dup")[-1].split("|")[0]
                        
                        if dup_index not in duplicateSizes:
                            duplicateSizes[dup_index] = {}
                            duplicateRots[dup_index] = {}

                        duplicateSizes[dup_index] = [cmds.getAttr(f"{d}.scaleX"), cmds.getAttr(f"{d}.scaleY"), cmds.getAttr(f"{d}.scaleZ")]
                        duplicateRots[dup_index] = [cmds.getAttr(f"{d}.rotateX"), cmds.getAttr(f"{d}.rotateY"), cmds.getAttr(f"{d}.rotateZ")]

                    duplicateSizes[str(i+2)] = [cmds.getAttr(f"{obj}.scaleX"), cmds.getAttr(f"{obj}.scaleY"), cmds.getAttr(f"{obj}.scaleZ")]
                    duplicateRots[str(i+2)] = [cmds.getAttr(f"{obj}.rotateX"), cmds.getAttr(f"{obj}.rotateY"), cmds.getAttr(f"{obj}.rotateZ")]
                    """

        print(duplicateSizes)

        #0, 5, 10, 15, 20
        if (gen_settings[gen_num]["additive_translate"] == False):
            tranX += gen_settings[gen_num]["tran_x"]
            tranY += gen_settings[gen_num]["tran_y"]
            tranZ += gen_settings[gen_num]["tran_z"]

        #0, 5, 15, 30, 50
        if (gen_settings[gen_num]["additive_translate"] == True):
            tranX += (i+2) * gen_settings[gen_num]["tran_x"]
            tranY += (i+2) * gen_settings[gen_num]["tran_y"]
            tranZ += (i+2) * gen_settings[gen_num]["tran_z"]

        if (gen_settings[gen_num]["multiplicative_scale"]):
            size *= gen_settings[gen_num]["size"]
            scaleX *= gen_settings[gen_num]["scale_x"]
            scaleY *= gen_settings[gen_num]["scale_y"]
            scaleZ *= gen_settings[gen_num]["scale_z"]

        #TODO: !!!
        if (gen_settings[gen_num]["additive_scale"]): 
            size_offset = 1 - gen_settings[gen_num]["size"]
            scale_x_offset = 1 - gen_settings[gen_num]["scale_x"]
            scale_y_offset = 1 - gen_settings[gen_num]["scale_y"]
            scale_z_offset = 1 - gen_settings[gen_num]["scale_z"]

        if (gen_settings[gen_num]["additive_rotate"]):
            rotX += gen_settings[gen_num]["rot_x"]
            rotY += gen_settings[gen_num]["rot_y"]
            rotZ += gen_settings[gen_num]["rot_z"]

        #hide duplicated baseplanes by default
        children = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
        basePlanes = [c for c in children if "basePlane" in c]
        cmds.hide(basePlanes)
        
    

    # get every transform under the gen
    all_desc = cmds.listRelatives(g, allDescendents=True, fullPath=True, type="transform") or []

    # keep only duplicate gen groups (exclude blocks)
    dup_groups = []
    for d in all_desc:
        short = d.split("|")[-1]
        if "_dup" in short and "block" not in short:
            dup_groups.append(d)

    for d in dup_groups:
        short = d.split("|")[-1]
        dup_index = short.split("_dup", 1)[1]

        duplicateSizes[dup_index] = [
            cmds.getAttr(f"{d}.scaleX"),
            cmds.getAttr(f"{d}.scaleY"),
            cmds.getAttr(f"{d}.scaleZ")
        ]

        duplicateRots[dup_index] = [
            cmds.getAttr(f"{d}.rotateX"),
            cmds.getAttr(f"{d}.rotateY"),
            cmds.getAttr(f"{d}.rotateZ")
        ]

    """
    for grp in dup_group_list:
        cmds.parent(grp, g)     
    """
    
    #cmds.xform(g, ws=True, piv=pivot_pos) # moves both rotate and scale pivots



# Modify section ----------------------------
def reset_gen_building_sizes(gen_num, buildingSizes):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        buildings = [c for c in children if "building" in c]

        for b in buildings:
            short = b.split("|")[-1]

            parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
            grandparent_group = cmds.listRelatives(parent_group, parent=True, fullPath=True)[0]
    
            dup_index = grandparent_group.split("dup")[-1].split("|")[0]
            if (not buildingSizes.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.scale(buildingSizes[dup_index][short][0], buildingSizes[dup_index][short][1], buildingSizes[dup_index][short][2], b, absolute=True)

def reset_gen_building_rots(gen_num, buildingRots):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        buildings = [c for c in children if "building" in c]

        for b in buildings:
            short = b.split("|")[-1]

            parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
            grandparent_group = cmds.listRelatives(parent_group, parent=True, fullPath=True)[0]
    
            dup_index = grandparent_group.split("dup")[-1].split("|")[0]
            if (not buildingRots.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.rotate(buildingRots[dup_index][short][0], buildingRots[dup_index][short][1], buildingRots[dup_index][short][2], b, absolute=True)

def reset_gen_block_sizes(gen_num, blockSizes):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        blocks = [c for c in children if "block" in c and c.split("|")[-1].endswith("_GRP")]

        for b in blocks:
            short = b.split("|")[-1]

            parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
    
            dup_index = parent_group.split("dup")[-1].split("|")[0]

            if (not blockSizes.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.scale(blockSizes[dup_index][short][0], blockSizes[dup_index][short][1], blockSizes[dup_index][short][2], b, absolute=True)

def reset_gen_block_rots(gen_num, blockRots):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        blocks = [c for c in children if "block" in c and c.split("|")[-1].endswith("_GRP")]

        for b in blocks:
            short = b.split("|")[-1]

            parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
    
            dup_index = parent_group.split("dup")[-1].split("|")[0]
            if (not blockRots.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.rotate(blockRots[dup_index][short][0], blockRots[dup_index][short][1], blockRots[dup_index][short][2], b, absolute=True)

def reset_gen_duplicate_sizes(gen_num, duplicateSizes):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        dups = [c for c in children if "dup" in c and cmds.listRelatives(c)[0].endswith("_GRP")]

        for d in dups:
            dup_index = d.split("dup")[-1].split("|")[0]

            if (not duplicateSizes.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.scale(duplicateSizes[dup_index][0], duplicateSizes[dup_index][1], duplicateSizes[dup_index][2], d, absolute=True)

def reset_gen_duplicate_rots(gen_num, duplicateRots):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
        dups = [c for c in children if "dup" in c and cmds.listRelatives(c)[0].endswith("_GRP")]

        for d in dups:    
            dup_index = d.split("dup")[-1].split("|")[0]

            if (not duplicateRots.get(dup_index)):
                dup_index = "1"  #default to dup1 if not found

            cmds.rotate(duplicateRots[dup_index][0], duplicateRots[dup_index][1], duplicateRots[dup_index][2], d, absolute=True)

def reset_gen_size(gen_num, globalSizes):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        cmds.scale(globalSizes[0], globalSizes[1], globalSizes[2], grp, absolute=True)

def reset_gen_rot(gen_num, globalRots):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        cmds.rotate(globalRots[0], globalRots[1], globalRots[2], grp, absolute=True)

def mod_per_dup(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["mod_per_individual_duplicate"] = value

def mod_per_block(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["mod_per_individual_block"] = value

def mod_per_building(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["mod_per_individual_building"] = value


def update_gen_scale_global(gen_num, value):
    gen_settings[gen_num]["global_scale"] = float(value)
    update_gen_scales(gen_num)
        
def update_gen_scaleX(gen_num, value):
    gen_settings[gen_num]["global_scaleX"] = float(value)
    update_gen_scales(gen_num)

def update_gen_scaleY(gen_num, value):
    gen_settings[gen_num]["global_scaleY"] = float(value)
    update_gen_scales(gen_num)

def update_gen_scaleZ(gen_num, value):
    gen_settings[gen_num]["global_scaleZ"] = float(value)
    update_gen_scales(gen_num)

def update_gen_scales(gen_num):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        buildingSizes = gen_settings[gen_num]["building_sizes"]
        blockSizes = gen_settings[gen_num]["block_sizes"]
        duplicateSizes = gen_settings[gen_num]["duplicate_sizes"]
        s = gen_settings[gen_num]["global_scale"]
        sx = gen_settings[gen_num]["global_scaleX"]
        sy = gen_settings[gen_num]["global_scaleY"]
        sz = gen_settings[gen_num]["global_scaleZ"]

        if (gen_settings[gen_num]["mod_per_individual_building"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            buildings = [c for c in children if "building" in c]

            for b in buildings:
                short = b.split("|")[-1]

                parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
                grandparent_group = cmds.listRelatives(parent_group, parent=True, fullPath=True)[0]
        
                dup_index = grandparent_group.split("dup")[-1].split("|")[0]
                if (not buildingSizes.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found
                
                cmds.scale(s * sx * buildingSizes[dup_index][short][0], s * sy * buildingSizes[dup_index][short][1], s * sz * buildingSizes[dup_index][short][2], b, absolute=True)

                #cmds.scale(s * sx, s * sy, s * sz, b, absolute=True)
        
        elif (gen_settings[gen_num]["mod_per_individual_block"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            blocks = [c for c in children if "block" in c and c.split("|")[-1].endswith("_GRP")]

            for b in blocks:
                short = b.split("|")[-1]

                parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
        
                dup_index = parent_group.split("dup")[-1].split("|")[0]
                if (not blockSizes.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found

                cmds.scale(s * sx * blockSizes[dup_index][short][0], s * sy * blockSizes[dup_index][short][1], s * sz * blockSizes[dup_index][short][2], b, absolute=True)

        elif (gen_settings[gen_num]["mod_per_individual_duplicate"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            dups = [c for c in children if "dup" in c and cmds.listRelatives(c)[0].endswith("_GRP")]

            for d in dups:
                dup_index = d.split("dup")[-1].split("|")[0]
        
                if (not duplicateSizes.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found
                
                cmds.scale(s * sx * duplicateSizes[dup_index][0], s * sy * duplicateSizes[dup_index][1], s * sz * duplicateSizes[dup_index][2], d, absolute=True)

        else: 
            cmds.scale(s * sx, s * sy, s * sz, grp, absolute=True)
  

def update_gen_rotX(gen_num, value):
    gen_settings[gen_num]["global_rotX"] = float(value)
    update_gen_rots(gen_num)

def update_gen_rotY(gen_num, value):
    gen_settings[gen_num]["global_rotY"] = float(value)
    update_gen_rots(gen_num)

def update_gen_rotZ(gen_num, value):
    gen_settings[gen_num]["global_rotZ"] = float(value)
    update_gen_rots(gen_num)

def update_gen_rots(gen_num):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        buildingRots = gen_settings[gen_num]["building_rots"]
        blockRots = gen_settings[gen_num]["block_rots"]
        duplicateRots = gen_settings[gen_num]["duplicate_rots"]
        rx = gen_settings[gen_num]["global_rotX"]
        ry = gen_settings[gen_num]["global_rotY"]
        rz = gen_settings[gen_num]["global_rotZ"]

        if (gen_settings[gen_num]["mod_per_individual_building"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            buildings = [c for c in children if "building" in c]

            for b in buildings:
                short = b.split("|")[-1]

                parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
                grandparent_group = cmds.listRelatives(parent_group, parent=True, fullPath=True)[0]
        
                dup_index = grandparent_group.split("dup")[-1].split("|")[0]
                if (not buildingRots.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found

                cmds.rotate(rx + buildingRots[dup_index][short][0], ry + buildingRots[dup_index][short][1], rz + buildingRots[dup_index][short][2], b, absolute=True)

        elif (gen_settings[gen_num]["mod_per_individual_block"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            blocks = [c for c in children if "block" in c and c.split("|")[-1].endswith("_GRP")]

            for b in blocks:
                short = b.split("|")[-1]

                parent_group = cmds.listRelatives(b, parent=True, fullPath=True)[0]
        
                dup_index = parent_group.split("dup")[-1].split("|")[0]
                if (not blockRots.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found

                cmds.rotate(rx + blockRots[dup_index][short][0], ry + blockRots[dup_index][short][1], rz + blockRots[dup_index][short][2], b, absolute=True)
        
        elif (gen_settings[gen_num]["mod_per_individual_duplicate"] == True):
            children = cmds.listRelatives(grp, allDescendents=True, type="transform", fullPath=True) or []
            dups = [c for c in children if "dup" in c and cmds.listRelatives(c)[0].endswith("_GRP")]

            for d in dups:
                dup_index = d.split("dup")[-1].split("|")[0]
        
                if (not duplicateRots.get(dup_index)):
                    dup_index = "1"  #default to dup1 if not found
                
                cmds.rotate(rx + duplicateRots[dup_index][0], ry + duplicateRots[dup_index][1], rz + duplicateRots[dup_index][2], d, absolute=True)

        else: 
            cmds.rotate(rx, ry, rz, grp, absolute=True)


def update_gen_tranX(gen_num, value):
    gen_settings[gen_num]["global_tranX"] = float(value)
    update_gen_trans(gen_num)

def update_gen_tranY(gen_num, value):
    gen_settings[gen_num]["global_tranY"] = float(value)
    update_gen_trans(gen_num)

def update_gen_tranZ(gen_num, value):
    gen_settings[gen_num]["global_tranZ"] = float(value)
    update_gen_trans(gen_num)

def update_gen_trans(gen_num):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        mx = gen_settings[gen_num]["global_tranX"]
        my = gen_settings[gen_num]["global_tranY"]
        mz = gen_settings[gen_num]["global_tranZ"]
        cmds.move(mx, my, mz, grp, absolute=True)


def update_hide_base_planes(gen_num, value):
    gen_settings[gen_num]["hide_base_planes"] = bool(value)
    
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(f"GEN{gen_num}_GRP", allDescendents=True, fullPath=True) or []
        basePlanes = [c for c in children if "basePlane" in c]

        if (gen_settings[gen_num]["hide_base_planes"] == True):
            cmds.hide(basePlanes)
        else:
            cmds.showHidden(basePlanes)

#TODO
def reset_base_planes_visibility(gen_num, value):
    grp = generations.get(gen_num)
    if grp and cmds.objExists(grp):
        children = cmds.listRelatives(f"GEN{gen_num}_GRP", allDescendents=True, fullPath=True) or []
        basePlanes = [c for c in children if "basePlane" in c]

        if (value == True):
            cmds.hide(basePlanes)
        else:
            cmds.hide(basePlanes)
            for bp in basePlanes:
                # find all dup indices in the full DAG path
                dup_indices = re.findall(r"_dup(\d+)", bp)

                is_first_line = (
                    not dup_indices or
                    all(i == "1" for i in dup_indices)
                )

                if is_first_line:
                    cmds.showHidden(bp)

            """
            for plane in basePlanes:        
                parent = cmds.listRelatives(plane, parent=True, fullPath=True)[0]
                grandparent = cmds.listRelatives(parent, parent=True)[0]

                if (grandparent == f"GEN{gen_num}_GRP" or grandparent.endswith("1")):
                    cmds.showHidden(plane)
            """


# Duplicate section
def dup_iterations(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["iterations"] = value

def dup_per_prior_dup(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["per_prior_dup"] = value

def dup_per_dup(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["per_individual_dup"] = value

def dup_per_block(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["per_individual_block"] = value

def dup_per_building(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["per_individual_building"] = value


def dup_additive_scale(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["additive_scale"] = value

def dup_multiplicative_scale(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["multiplicative_scale"] = value

def dup_size(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["size"] = value

def dup_scale_x(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["scale_x"] = value

def dup_scale_y(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["scale_y"] = value

def dup_scale_z(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["scale_z"] = value   


def dup_additive_translate(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["additive_translate"] = value

def dup_tran_x(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["tran_x"] = value

def dup_tran_y(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["tran_y"] = value

def dup_tran_z(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["tran_z"] = value


def dup_additive_rotate(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["additive_rotate"] = value

def dup_rot_x(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["rot_x"] = value

def dup_rot_y(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["rot_y"] = value

def dup_rot_z(gen_num, value):
    global gen_settings
    gen_settings[gen_num]["rot_z"] = value



# ------------------------------------- WINDOW LAYOUT ------------------------------------------------
if cmds.window("City-Gen", exists=True):
    cmds.deleteUI("City-Gen")
window = cmds.window("City-Gen", title="City Generator")

main_scroll = cmds.scrollLayout(childResizable=True)
main_column = cmds.columnLayout(adjustableColumn=True, parent=main_scroll)

tabs = cmds.tabLayout()
main_tab = cmds.columnLayout(adj=True)
cmds.tabLayout(tabs, edit=True, tabLabel=(main_tab, "Generator"))

cmds.separator(height=10, style="none")
cmds.text(label="CITY GENERATOR", align="center", height=30, font="boldLabelFont")
cmds.separator(height=15, style="single")  # just blank space

def reset_slider(slider_name, default_value, function_name, *args):
    cmds.floatSliderGrp(slider_name, e=True, value=default_value)
    function_name(default_value)



#presets ------------------------------------
cmds.text(label=" Presets", align="left", font="boldLabelFont", height=20)
cmds.separator(height=4, style="none")

# primitive shapes
cmds.frameLayout(
    label="Primitive Shapes",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)
cmds.columnLayout(adj=True, rowSpacing=2)   # <- reduce spacing here
cmds.button(label='Cube', command=lambda *args: presets("Cube"), bgc = subsub_color)
cmds.button(label='Sphere', command=lambda *args: presets("Sphere"), bgc = subsub_color)
cmds.setParent('..')  # back to main layout
cmds.setParent('..')  # back to main layout

# cities and towns
cmds.frameLayout(
    label="Cities and Towns",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

cmds.columnLayout(adj=True, rowSpacing=2)   # <- reduce spacing here
cmds.button(label='Classic City', command=lambda *args: presets("Default City"), bgc = subsub_color)
cmds.button(label='Small Town', command=lambda *args: presets("Small Town"), bgc = subsub_color)
cmds.button(label='Skyscrapers', command=lambda *args: presets("Skycrapers"), bgc = subsub_color)
cmds.setParent('..')  # back to main layout
cmds.setParent('..')  # columnLayout

# dystopian
cmds.frameLayout(
    label="Dystopian",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

cmds.columnLayout(adj=True, rowSpacing=2)   # <- reduce spacing here
cmds.button(label='Dystopian 1', command=lambda *args: presets("Dystopian1"), bgc = subsub_color)
cmds.button(label='Dystopian 2', command=lambda *args: presets("Dystopian2"), bgc = subsub_color)
cmds.button(label='Dystopian 3', command=lambda *args: presets("Dystopian3"), bgc = subsub_color)
cmds.setParent('..')  # back to main layout
cmds.setParent('..')  # columnLayout

# sky
cmds.frameLayout(
    label="Sky",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

cmds.columnLayout(adj=True, rowSpacing=2)   # <- reduce spacing here
cmds.button(label='Small Clouds', command=lambda *args: presets("Small Clouds"), bgc = subsub_color)
cmds.button(label='Rain', command=lambda *args: presets("Rain"), bgc = subsub_color)
cmds.button(label='Cyber Particles', command=lambda *args: presets("Cyber Particles"), bgc = subsub_color)
cmds.button(label='Cyber Planes', command=lambda *args: presets("Cyber Planes"), bgc = subsub_color)
cmds.setParent('..')  # back to main layout
cmds.setParent('..')  # columnLayout
cmds.separator(height=1, style="none")

# default settings
cmds.button(label='Default Settings', command=lambda *args: presets("Default City"), bgc = sub_color)
cmds.separator(height=10, style="none")  # just blank space
cmds.separator(height=15, style="single")



# settings -----------------------------------
def gen_at_each_modification(value):
    global gen_at_each_modif
    gen_at_each_modif = value

def undo_button(*args):
    if len(gen_undo_settings) < 2:
        print("Nothing to undo")
        return

    max_undo = max(gen_undo_settings)
    max_redo = max(gen_redo_settings) if gen_redo_settings else -1

    # Move current state to redo
    if max_redo == -1 or gen_redo_settings.get(max_redo) != gen_undo_settings[max_undo]:
        gen_redo_settings[max_redo + 1] = gen_undo_settings[max_undo]

    # Delete current state from undo
    del gen_undo_settings[max_undo]

    # Execute previous state
    prev_key = max(gen_undo_settings)
    raw = gen_undo_settings[prev_key]
    exec(raw, globals())
    update_all_sliders()
    generate_city()

def redo_button(*args):
    if not gen_redo_settings:
        print("Nothing to redo")
        return

    max_redo = max(gen_redo_settings)
    max_undo = max(gen_undo_settings) if gen_undo_settings else -1

    # Move redo state back to undo
    if max_undo == -1 or gen_undo_settings.get(max_undo) != gen_redo_settings[max_redo]:
        gen_undo_settings[max_undo + 1] = gen_redo_settings[max_redo]

    # Remove applied redo
    del gen_redo_settings[max_redo]

    # Execute redone state
    raw = gen_undo_settings[max(gen_undo_settings)]
    exec(raw, globals())
    update_all_sliders()
    generate_city()

cmds.rowLayout(numberOfColumns=3, columnWidth3=(122, 130, 122))
cmds.text(label=" Settings", align="left", font="boldLabelFont")
cmds.separator(style="none")   # left empty space
cmds.checkBox(label="Gen at each modification", value=True, changeCommand=gen_at_each_modification, height=22)
cmds.setParent("..")
cmds.separator(height=3, style="none")

cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
cmds.button(label="                           Undo                           ", command=undo_button, height=21)
cmds.button(label="                           Redo                           ", command=redo_button, height=21)
cmds.setParent('..')  # back to main layout

"""
cmds.text(label=" Settings", align="left", font="boldLabelFont")
cmds.separator(height=2, style="none")
cmds.rowLayout(numberOfColumns=3, columnWidth3=(130, 150, 130))
cmds.separator(style="none")   # left empty space
cmds.checkBox(label="Gen at each modification", value=True, changeCommand=gen_at_each_modification, height=22)
cmds.separator(style="none")   # left empty space
cmds.setParent('..')  # back to main layout
cmds.separator(height=2, style="none")

cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
cmds.button(label="                           Undo                           ", command=undo_button, height=21)
cmds.button(label="                           Redo                           ", command=redo_button, height=21)
cmds.setParent('..')  # back to main layout
"""

"""
cmds.text(label=" Settings", align="left", font="boldLabelFont")
cmds.separator(height=8, style="none")
cmds.rowLayout(numberOfColumns=5, adjustableColumn=5)

cmds.separator(style="none", width=10)   # left empty space
cmds.checkBox(label="Gen at each modification", value=True, changeCommand=gen_at_each_modification, height=21)
cmds.separator(style="none", width=90)   # left empty space

cmds.button(label="                           Undo                           ", command=undo_button, height=21, width=70)
cmds.button(label="                           Redo                           ", command=redo_button, height=21, width=70)
cmds.setParent('..')  # back to main layout
"""

global_transform_frame = cmds.frameLayout(
    label="Building Settings",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

def set_undo_redo_and_generate(*args):
    if not args and not gen_at_each_modif: 
        return

    if gen_undo_settings:
        highest_key = max(gen_undo_settings)

        if getCurrentSettings() != gen_undo_settings[highest_key]: #if current settings are different from last saved settings
            gen_undo_settings[highest_key + 1] = getCurrentSettings()
            gen_redo_settings.clear()

    else:
        # first state
        gen_undo_settings[0] = getCurrentSettings()
        gen_redo_settings.clear()

    if not args or args[0] == "Generate":
        generate_city()
    else:
        regenerate_city()

def reset_slider(slider_name, default_value, function_name, *args):
    cmds.floatSliderGrp(slider_name, e=True, value=default_value)
    function_name(default_value)



#shape --------------------------------------
cmds.columnLayout(adj=True, rowSpacing=0)   # <– controls spacing between frames
global_transform_frame = cmds.frameLayout(
    label="Building Shape",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_shape(*args):
    global shape

    index = cmds.radioButtonGrp(shape_selector, query=True, select=True)
    shape = shapes[index-1]

    generate_city() 

cmds.rowLayout(numberOfColumns=6, columnWidth6=(41, 300, 300, 300, 300, 41))
cmds.separator(style="none")  # left empty space

shape_selector = cmds.radioButtonGrp(
    labelArray4=["Cube", "Sphere", "Cylinder", "Torus"],
    numberOfRadioButtons=4,
    select=1, # default selected
    columnWidth4=(80, 80, 80, 80),  # optional to control spacing
    changeCommand=set_shape
)

cmds.separator(style="none")  # right empty space
cmds.setParent('..')  # back to frameLayout
cmds.setParent('..')  # back to main layout

    

#buildings: size -----------------------------
global_transform_frame = cmds.frameLayout(
    label="Building Size",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_min_height(value):
    global min_height
    value = float(value)

    # Clamp min so it can't be greater than max
    if value > max_height:
        value = max_height
    min_height = value
    cmds.floatSliderGrp(slider_min_height, e=True, value=min_height) #new

    set_undo_redo_and_generate()

def set_max_height(value):
    global max_height
    value = float(value)

    # Clamp max so it can't be less than min
    if value < min_height:
        value = min_height
    max_height = value
    cmds.floatSliderGrp(slider_max_height, e=True, value=max_height) #new

    set_undo_redo_and_generate()

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_min_height = cmds.floatSliderGrp(
    label="Building Min Height",
    field=True,
    minValue=0.1,
    maxValue=50,
    value=min_height,
    changeCommand=set_min_height
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_min_height, 8, set_min_height), height=20) #new
cmds.setParent("..")  #new

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_max_height = cmds.floatSliderGrp(
    label="Building Max Height",
    field=True,
    minValue=0.1,
    maxValue=50,
    value=max_height,
    changeCommand=set_max_height
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_max_height, 30, set_max_height), height=20) #new
cmds.setParent("..")  #new

def set_min_width(value):
    global min_width
    value = float(value)

        # Clamp min so it can't be greater than max
    if value > max_width:
        value = max_width
    min_width = value
    cmds.floatSliderGrp(slider_min_width, e=True, value=min_width) #new

    set_undo_redo_and_generate()

def set_max_width(value):
    global max_width
    value = float(value)

    # Clamp max so it can't be less than min
    if value < min_width:
        value = min_width
    max_width = value
    cmds.floatSliderGrp(slider_max_width, e=True, value=max_width) #new

    set_undo_redo_and_generate()

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_min_width = cmds.floatSliderGrp(
    label="Building Min Width",
    field=True,
    minValue=0.1,
    maxValue=20,
    value=min_width,
    changeCommand=set_min_width
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_min_width, 4, set_min_width), height=20) #new
cmds.setParent("..")  #new

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_max_width = cmds.floatSliderGrp(
    label="Building Max Width",
    field=True,
    minValue=0.1,
    maxValue=20,
    value=max_width,
    changeCommand=set_max_width
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_max_width, 4, set_max_width), height=20) #new
cmds.setParent("..")  #new

def set_min_depth(value):
    global min_depth
    value = float(value)

    # Clamp min so it can't be greater than max
    if value > max_depth:
        value = max_depth
    min_depth = value
    cmds.floatSliderGrp(slider_min_depth, e=True, value=min_depth) #new

    set_undo_redo_and_generate()

def set_max_depth(value):
    global max_depth
    value = float(value)

    # Clamp max so it can't be less than min
    if value < min_depth:
        value = min_depth
    max_depth = value
    cmds.floatSliderGrp(slider_max_depth, e=True, value=max_depth) #new

    set_undo_redo_and_generate()

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_min_depth = cmds.floatSliderGrp(
    label="Building Min Depth",
    field=True,
    minValue=0.1,
    maxValue=20,
    value=min_depth,
    changeCommand=set_min_depth
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_min_depth, 3, set_min_depth), height=20) #new
cmds.setParent("..")  #new

cmds.rowLayout(numberOfColumns=2, columnWidth2=(250, 80), adjustableColumn=1) #new

slider_max_depth = cmds.floatSliderGrp(
    label="Building Max Depth",
    field=True,
    minValue=0.1,
    maxValue=20,
    value=max_depth,
    changeCommand=set_max_depth
)

cmds.button(label="⌫", command=lambda x: reset_slider(slider_max_depth, 7, set_max_depth), height=20) #new
cmds.setParent("..")  #new

cmds.setParent('..')  # end frameLayout

#buildings: translate ------------------------
global_transform_frame = cmds.frameLayout(
    label="Building Translate",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_min_tran_X(value):
    global min_tran_X
    value = float(value)
    
    if value > max_tran_X:
        value = max_tran_X
    min_tran_X = value   
    cmds.floatSliderGrp(slider_min_tran_X, e=True, value=min_tran_X) #new

    set_undo_redo_and_generate()

def set_max_tran_X(value):
    global max_tran_X
    value = float(value)

    if value < min_tran_X:
        value = min_tran_X
    max_tran_X = value
    cmds.floatSliderGrp(slider_max_tran_X, e=True, value=max_tran_X) #new

    set_undo_redo_and_generate()

slider_min_tran_X = cmds.floatSliderGrp(
    label="Building Min Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=min_tran_X,
    changeCommand=set_min_tran_X
)

slider_max_tran_X = cmds.floatSliderGrp(
    label="Building Max Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=max_tran_X,
    changeCommand=set_max_tran_X
)   

def set_min_tran_Y(value):
    global min_tran_Y
    value = float(value)

    if value > max_tran_Y:
        value = max_tran_Y
    min_tran_Y = value
    cmds.floatSliderGrp(slider_min_tran_Y, e=True, value=min_tran_Y) #new

    set_undo_redo_and_generate()

def set_max_tran_Y(value):
    global max_tran_Y
    value = float(value)

    if value < min_tran_Y:
        value = min_tran_Y
    max_tran_Y = value    
    cmds.floatSliderGrp(slider_max_tran_Y, e=True, value=max_tran_Y) #new

    set_undo_redo_and_generate()

slider_min_tran_Y = cmds.floatSliderGrp(
    label="Building Min Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=min_tran_Y,
    changeCommand=set_min_tran_Y
)

slider_max_tran_Y = cmds.floatSliderGrp(
    label="Building Max Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=max_tran_Y,
    changeCommand=set_max_tran_Y
)

def set_min_tran_Z(value):
    global min_tran_Z
    value = float(value)

    if value > max_tran_Z:
        value = max_tran_Z
    min_tran_Z = value
    cmds.floatSliderGrp(slider_min_tran_Z, e=True, value=min_tran_Z) #new

    set_undo_redo_and_generate()

def set_max_tran_Z(value):
    global max_tran_Z
    value = float(value)

    if value < min_tran_Z:
        value = min_tran_Z
    max_tran_Z = value
    cmds.floatSliderGrp(slider_max_tran_Z, e=True, value=max_tran_Z) #new

    set_undo_redo_and_generate()

slider_min_tran_Z = cmds.floatSliderGrp(
    label="Building Min Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=min_tran_Z,
    changeCommand=set_min_tran_Z
)

slider_max_tran_Z = cmds.floatSliderGrp(
    label="Building Max Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=max_tran_Z,
    changeCommand=set_max_tran_Z
)

cmds.setParent('..')  # end frameLayout (sub-tab)

#buildings: rotation -------------------------
global_transform_frame = cmds.frameLayout(
    label="Building Rotation",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_min_rot_X(value):
    global min_rot_X
    value = float(value)

    if value > max_rot_X:
        value = max_rot_X   
    min_rot_X = value
    cmds.floatSliderGrp(slider_min_rot_X, e=True, value=min_rot_X) #new

    set_undo_redo_and_generate()

def set_max_rot_X(value):
    global max_rot_X
    value = float(value)

    if value < min_rot_X:
        value = min_rot_X
    max_rot_X = value
    cmds.floatSliderGrp(slider_max_rot_X, e=True, value=max_rot_X) #new

    set_undo_redo_and_generate()

slider_min_rot_X = cmds.floatSliderGrp(
    label="Building Min Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=min_rot_X,
    changeCommand=set_min_rot_X
)

slider_max_rot_X = cmds.floatSliderGrp(
    label="Building Max Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=max_rot_X,
    changeCommand=set_max_rot_X
)

def set_min_rot_Y(value):
    global min_rot_Y
    value = float(value)

    if value > max_rot_Y:
        value = max_rot_Y   
    min_rot_Y = value
    cmds.floatSliderGrp(slider_min_rot_Y, e=True, value=min_rot_Y) #new

    set_undo_redo_and_generate()

def set_max_rot_Y(value):
    global max_rot_Y
    value = float(value)

    if value < min_rot_Y:
        value = min_rot_Y
    max_rot_Y = value 
    cmds.floatSliderGrp(slider_max_rot_Y, e=True, value=max_rot_Y) #new

    set_undo_redo_and_generate()  

slider_min_rot_Y = cmds.floatSliderGrp(
    label="Building Min Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=min_rot_Y,
    changeCommand=set_min_rot_Y
)

slider_max_rot_Y = cmds.floatSliderGrp(
    label="Building Max Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=max_rot_Y,
    changeCommand=set_max_rot_Y
)

def set_min_rot_Z(value):
    global min_rot_Z
    value = float(value)

    if value > max_rot_Z:
        value = max_rot_Z   
    min_rot_Z = value
    cmds.floatSliderGrp(slider_min_rot_Z, e=True, value=min_rot_Z) #new

    set_undo_redo_and_generate()

def set_max_rot_Z(value):
    global max_rot_Z
    value = float(value)

    if value < min_rot_Z:
        value = min_rot_Z
    max_rot_Z = value
    cmds.floatSliderGrp(slider_max_rot_Z, e=True, value=max_rot_Z) #new

    set_undo_redo_and_generate()

slider_min_rot_Z = cmds.floatSliderGrp(
    label="Building Min Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=min_rot_Z,
    changeCommand=set_min_rot_Z
)        

slider_max_rot_Z = cmds.floatSliderGrp(
    label="Building Max Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=max_rot_Z,
    changeCommand=set_max_rot_Z
)

cmds.setParent('..')  # end frameLayout
cmds.setParent('..')  # end frameLayout (tab)
cmds.setParent('..')  # end frameLayout (tab)



global_transform_frame = cmds.frameLayout(
    label="Scatter Settings",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

#blocks: scatter ----------------------------
cmds.columnLayout(adj=True, rowSpacing=0)   # <– controls spacing between frames
global_transform_frame = cmds.frameLayout(
    label="Number of Buildings (per block)",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

#number of buildings
def set_min_num_buildings(value):
    global min_num_buildings
    value = int(value)

    # Clamp min so it can't be greater than max
    if value > max_num_buildings:
        value = max_num_buildings
    min_num_buildings = value
    cmds.intSliderGrp(slider_min_num_buildings, e=True, value=min_num_buildings) #new

    set_undo_redo_and_generate()

slider_min_num_buildings = cmds.intSliderGrp(
    label="Min Number of Buildings",
    field=True,
    minValue=1,
    maxValue=200,
    value=min_num_buildings,
    changeCommand=set_min_num_buildings
)

def set_max_num_buildings(value):
    global max_num_buildings
    value = int(value)

    # Clamp min so it can't be greater than max
    if value < min_num_buildings:
        value = min_num_buildings
    max_num_buildings = value
    cmds.intSliderGrp(slider_max_num_buildings, e=True, value=max_num_buildings) #new

    set_undo_redo_and_generate()

slider_max_num_buildings = cmds.intSliderGrp(
    label="Max Number of Buildings",
    field=True,
    minValue=1,
    maxValue=200,
    value=max_num_buildings,
    changeCommand=set_max_num_buildings
)

cmds.setParent('..')  # end frameLayout

#base plane subdivisions
global_transform_frame = cmds.frameLayout(
    label="Number of Blocks",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

#number of blocks
def set_num_blocks_x(value):
    global num_blocks_x
    num_blocks_x = int(value)

    set_undo_redo_and_generate()

def set_num_blocks_z(value):
    global num_blocks_z
    num_blocks_z = int(value)

    set_undo_redo_and_generate()

slider_num_blocks_x = cmds.intSliderGrp(
    label="Number of Blocks (X)",
    field=True,
    minValue=1,
    maxValue=10,
    value=num_blocks_x,
    changeCommand=set_num_blocks_x
)

slider_num_blocks_z = cmds.intSliderGrp(
    label="Number of Blocks (Z)",
    field=True,
    minValue=1,
    maxValue=10,
    value=num_blocks_z,
    changeCommand=set_num_blocks_z
)

cmds.setParent('..')  # end frameLayout



#blocks: size --------------------------------
global_transform_frame = cmds.frameLayout(
    label="Building Spawn Area (per block)",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_subdiv_w(value):
    global subdiv_w
    subdiv_w = int(value)

    set_undo_redo_and_generate()

def set_subdiv_h(value):
    global subdiv_h
    subdiv_h = int(value)

    set_undo_redo_and_generate()

slider_subdiv_w = cmds.intSliderGrp(
    label="Building Spawns (X)",
    field=True,
    minValue=1,
    maxValue=100,
    value=subdiv_w,
    changeCommand=set_subdiv_w
)

slider_subdiv_h = cmds.intSliderGrp(
    label="Building Spawns (Z)",
    field=True,
    minValue=1,
    maxValue=100,
    value=subdiv_h,
    changeCommand=set_subdiv_h
)

def set_block_size_x(value):
    global block_size_X
    block_size_X = float(value)

    set_undo_redo_and_generate()

def set_block_size_z(value):
    global block_size_Z
    block_size_Z = float(value)

    set_undo_redo_and_generate()

slider_block_size_x = cmds.floatSliderGrp(
    label="Block Base Size (X)",
    field=True,
    minValue=0.1,
    maxValue=100,
    value=block_size_X,
    changeCommand=set_block_size_x
)

slider_block_size_z = cmds.floatSliderGrp(
    label="Block Base Size (Z)",
    field=True,
    minValue=0.1,
    maxValue=100,
    value=block_size_Z,
    changeCommand=set_block_size_z
)

#space between blocks
def set_space_between_blocks_x(value):
    global space_between_blocks_X
    space_between_blocks_X = float(value)

    set_undo_redo_and_generate()

def set_space_between_blocks_z(value):
    global space_between_blocks_Z
    space_between_blocks_Z = float(value)

    set_undo_redo_and_generate()

slider_space_between_blocks_x = cmds.floatSliderGrp(
    label="Space Between Blocks (X)",
    field=True,
    minValue=0,
    maxValue=100,
    value=space_between_blocks_X,
    changeCommand=set_space_between_blocks_x
)

slider_space_between_blocks_z = cmds.floatSliderGrp(
    label="Space Between Blocks (Z)",
    field=True,
    minValue=0,
    maxValue=100,
    value=space_between_blocks_Z,
    changeCommand=set_space_between_blocks_z
)

cmds.setParent('..')  # end frameLayout (sub tab)
cmds.setParent('..')  # end frameLayout (sub tab)
cmds.setParent('..')  # end frameLayout



global_transform_frame = cmds.frameLayout(
    label="Block Settings",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

#blocks: size -----------------------------
cmds.columnLayout(adj=True, rowSpacing=0)   # <– controls spacing between frames

global_transform_frame = cmds.frameLayout(
    label="Block Size",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_block_min_size(value):
    global block_min_size
    value = float(value)
    
    if value > block_max_size:
        value = block_max_size
    block_min_size = value    
    cmds.floatSliderGrp(slider_block_min_size, e=True, value=block_min_size) #new

    set_undo_redo_and_generate()

def set_block_max_size(value):
    global block_max_size
    value = float(value)

    if value < block_min_size:
        value = block_min_size
    block_max_size = value
    cmds.floatSliderGrp(slider_block_max_size, e=True, value=block_max_size) #new

    set_undo_redo_and_generate()

slider_block_min_size = cmds.floatSliderGrp(
    label="Block Min Size",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_min_size,
    changeCommand=set_block_min_size
)

slider_block_max_size = cmds.floatSliderGrp(
    label="Block Max Size",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_max_size,
    changeCommand=set_block_max_size
)   

cmds.setParent('..')  # end frameLayout (sub tab)

#blocks: scale -----------------------------
global_transform_frame = cmds.frameLayout(
    label="Block Scale",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_block_min_scale_X(value):
    global block_min_scale_X
    value = float(value)
    
    if value > block_max_scale_X:
        value = block_max_scale_X
    block_min_scale_X = value    
    cmds.floatSliderGrp(slider_block_min_scale_X, e=True, value=block_min_scale_X) #new

    set_undo_redo_and_generate()

def set_block_max_scale_X(value):
    global block_max_scale_X
    value = float(value)

    if value < block_min_scale_X:
        value = block_min_scale_X
    block_max_scale_X = value
    cmds.floatSliderGrp(slider_block_max_scale_X, e=True, value=block_max_scale_X) #new

    set_undo_redo_and_generate()

slider_block_min_scale_X = cmds.floatSliderGrp(
    label="Block Min Scale (X)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_min_scale_X,
    changeCommand=set_block_min_scale_X
)

slider_block_max_scale_X = cmds.floatSliderGrp(
    label="Block Max Scale (X)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_max_scale_X,
    changeCommand=set_block_max_scale_X
)   

def set_block_min_scale_Y(value):
    global block_min_scale_Y
    value = float(value)

    if value > block_max_scale_Y:
        value = block_max_scale_Y
    block_min_scale_Y = value
    cmds.floatSliderGrp(slider_block_min_scale_Y, e=True, value=block_min_scale_Y) #new

    set_undo_redo_and_generate()

def set_block_max_scale_Y(value):
    global block_max_scale_Y
    value = float(value)

    if value < block_min_scale_Y:
        value = block_min_scale_Y
    block_max_scale_Y = value  
    cmds.floatSliderGrp(slider_block_max_scale_Y, e=True, value=block_max_scale_Y) #new

    set_undo_redo_and_generate()

slider_block_min_scale_Y = cmds.floatSliderGrp(
    label="Block Min Scale (Y)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_min_scale_Y,
    changeCommand=set_block_min_scale_Y
)

slider_block_max_scale_Y = cmds.floatSliderGrp(
    label="Block Max Scale (Y)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_max_scale_Y,
    changeCommand=set_block_max_scale_Y
)

def set_block_min_scale_Z(value):
    global block_min_scale_Z
    value = float(value)

    if value > block_max_scale_Z:
        value = block_max_scale_Z
    block_min_scale_Z = value
    cmds.floatSliderGrp(slider_block_min_scale_Z, e=True, value=block_min_scale_Z) #new

    set_undo_redo_and_generate()

def set_block_max_scale_Z(value):
    global block_max_scale_Z
    value = float(value)

    if value < block_min_scale_Z:
        value = block_min_scale_Z
    block_max_scale_Z = value
    cmds.floatSliderGrp(slider_block_max_scale_Z, e=True, value=block_max_scale_Z) #new

    set_undo_redo_and_generate()

slider_block_min_scale_Z = cmds.floatSliderGrp(
    label="Block Min Scale (Z)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_min_scale_Z,
    changeCommand=set_block_min_scale_Z
)

slider_block_max_scale_Z = cmds.floatSliderGrp(
    label="Block Max Scale (Z)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=block_max_scale_Z,
    changeCommand=set_block_max_scale_Z
)

cmds.setParent('..')  # end frameLayout (sub-tab)

#blocks: translate -----------------------------
global_transform_frame = cmds.frameLayout(
    label="Block Translate",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_block_min_tran_X(value):
    global block_min_tran_X
    value = float(value)
    
    if value > block_max_tran_X:
        value = block_max_tran_X
    block_min_tran_X = value    
    cmds.floatSliderGrp(slider_block_min_tran_X, e=True, value=block_min_tran_X) #new

    set_undo_redo_and_generate()

def set_block_max_tran_X(value):
    global block_max_tran_X
    value = float(value)

    if value < block_min_tran_X:
        value = block_min_tran_X
    block_max_tran_X = value
    cmds.floatSliderGrp(slider_block_max_tran_X, e=True, value=block_max_tran_X) #new

    set_undo_redo_and_generate()

slider_block_min_tran_X = cmds.floatSliderGrp(
    label="Block Min Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_min_tran_X,
    changeCommand=set_block_min_tran_X
)

slider_block_max_tran_X = cmds.floatSliderGrp(
    label="Block Max Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_max_tran_X,
    changeCommand=set_block_max_tran_X
)   

def set_block_min_tran_Y(value):
    global block_min_tran_Y
    value = float(value)

    if value > block_max_tran_Y:
        value = block_max_tran_Y
    block_min_tran_Y = value
    cmds.floatSliderGrp(slider_block_min_tran_Y, e=True, value=block_min_tran_Y) #new

    set_undo_redo_and_generate()

def set_block_max_tran_Y(value):
    global block_max_tran_Y
    value = float(value)

    if value < block_min_tran_Y:
        value = block_min_tran_Y
    block_max_tran_Y = value  
    cmds.floatSliderGrp(slider_block_max_tran_Y, e=True, value=block_max_tran_Y) #new

    set_undo_redo_and_generate()

slider_block_min_tran_Y = cmds.floatSliderGrp(
    label="Block Min Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_min_tran_Y,
    changeCommand=set_block_min_tran_Y
)

slider_block_max_tran_Y = cmds.floatSliderGrp(
    label="Block Max Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_max_tran_Y,
    changeCommand=set_block_max_tran_Y
)

def set_block_min_tran_Z(value):
    global block_min_tran_Z
    value = float(value)

    if value > block_max_tran_Z:
        value = block_max_tran_Z
    block_min_tran_Z = value
    cmds.floatSliderGrp(slider_block_min_tran_Z, e=True, value=block_min_tran_Z) #new

    set_undo_redo_and_generate()

def set_block_max_tran_Z(value):
    global block_max_tran_Z
    value = float(value)

    if value < block_min_tran_Z:
        value = block_min_tran_Z
    block_max_tran_Z = value
    cmds.floatSliderGrp(slider_block_max_tran_Z, e=True, value=block_max_tran_Z) #new

    set_undo_redo_and_generate()

slider_block_min_tran_Z = cmds.floatSliderGrp(
    label="Block Min Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_min_tran_Z,
    changeCommand=set_block_min_tran_Z
)

slider_block_max_tran_Z = cmds.floatSliderGrp(
    label="Block Max Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=block_max_tran_Z,
    changeCommand=set_block_max_tran_Z
)

cmds.setParent('..')  # end frameLayout (sub-tab)

#blocks: rotation ------------------------------
global_transform_frame = cmds.frameLayout(
    label="Block Rotation",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_block_min_rot_X(value):
    global block_min_rot_X
    value = float(value)

    if value > block_max_rot_X:
        value = block_max_rot_X   
    block_min_rot_X = value
    cmds.floatSliderGrp(slider_block_min_rot_X, e=True, value=block_min_rot_X) #new

    set_undo_redo_and_generate()

def set_block_max_rot_X(value):
    global block_max_rot_X
    value = float(value)

    if value < block_min_rot_X:
        value = block_min_rot_X
    block_max_rot_X = value
    cmds.floatSliderGrp(slider_block_max_rot_X, e=True, value=block_max_rot_X) #new

    set_undo_redo_and_generate()

slider_block_min_rot_X = cmds.floatSliderGrp(
    label="Block Min Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_min_rot_X,
    changeCommand=set_block_min_rot_X
)

slider_block_max_rot_X = cmds.floatSliderGrp(
    label="Block Max Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_max_rot_X,
    changeCommand=set_block_max_rot_X
)

def set_block_min_rot_Y(value):
    global block_min_rot_Y
    value = float(value)

    if value > block_max_rot_Y:
        value = block_max_rot_Y   
    block_min_rot_Y = value
    cmds.floatSliderGrp(slider_block_min_rot_Y, e=True, value=block_min_rot_Y) #new

    set_undo_redo_and_generate()

def set_block_max_rot_Y(value):
    global block_max_rot_Y
    value = float(value)

    if value < block_min_rot_Y:
        value = block_min_rot_Y
    block_max_rot_Y = value 
    cmds.floatSliderGrp(slider_block_max_rot_Y, e=True, value=block_max_rot_Y) #new

    set_undo_redo_and_generate() 

slider_block_min_rot_Y = cmds.floatSliderGrp(
    label="Block Min Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_min_rot_Y,
    changeCommand=set_block_min_rot_Y
)

slider_block_max_rot_Y = cmds.floatSliderGrp(
    label="Block Max Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_max_rot_Y,
    changeCommand=set_block_max_rot_Y
)

def set_block_min_rot_Z(value):
    global block_min_rot_Z
    value = float(value)

    if value > block_max_rot_Z:
        value = block_max_rot_Z   
    block_min_rot_Z = value
    cmds.floatSliderGrp(slider_block_min_rot_Z, e=True, value=block_min_rot_Z) #new

    set_undo_redo_and_generate()

def set_block_max_rot_Z(value):
    global block_max_rot_Z
    value = float(value)

    if value < block_min_rot_Z:
        value = block_min_rot_Z
    block_max_rot_Z = value
    cmds.floatSliderGrp(slider_block_max_rot_Z, e=True, value=block_max_rot_Z) #new

    set_undo_redo_and_generate()

slider_block_min_rot_Z = cmds.floatSliderGrp(
    label="Block Min Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_min_rot_Z,
    changeCommand=set_block_min_rot_Z
)        

slider_block_max_rot_Z = cmds.floatSliderGrp(
    label="Block Max Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=block_max_rot_Z,
    changeCommand=set_block_max_rot_Z
)

cmds.setParent('..')  # end frameLayout
cmds.setParent('..')  # end frameLayout (tab)
cmds.setParent('..')  # end frameLayout (sub-tab)



global_transform_frame = cmds.frameLayout(
    label="Global Settings",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

#globals: size -----------------------------
cmds.columnLayout(adj=True, rowSpacing=0)   # <– controls spacing between frames

global_transform_frame = cmds.frameLayout(
    label="Global Size",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_global_min_size(value):
    global global_min_size
    value = float(value)
    
    if value > global_max_size:
        value = global_max_size
    global_min_size = value    
    cmds.floatSliderGrp(slider_global_min_size, e=True, value=global_min_size) #new

    set_undo_redo_and_generate()

def set_global_max_size(value):
    global global_max_size
    value = float(value)

    if value < global_min_size:
        value = global_min_size
    global_max_size = value
    cmds.floatSliderGrp(slider_global_max_size, e=True, value=global_max_size) #new

    set_undo_redo_and_generate()

slider_global_min_size = cmds.floatSliderGrp(
    label="Global Min Size",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_min_size,
    changeCommand=set_global_min_size
)

slider_global_max_size = cmds.floatSliderGrp(
    label="Global Max Size",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_max_size,
    changeCommand=set_global_max_size
)   

cmds.setParent('..')  # end frameLayout (sub tab)

#globals: scale -----------------------------
global_transform_frame = cmds.frameLayout(
    label="Global Scale",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_global_min_scale_X(value):
    global global_min_scale_X
    value = float(value)
    
    if value > global_max_scale_X:
        value = global_max_scale_X
    global_min_scale_X = value    
    cmds.floatSliderGrp(slider_global_min_scale_X, e=True, value=global_min_scale_X) #new

    set_undo_redo_and_generate()

def set_global_max_scale_X(value):
    global global_max_scale_X
    value = float(value)

    if value < global_min_scale_X:
        value = global_min_scale_X
    global_max_scale_X = value
    cmds.floatSliderGrp(slider_global_max_scale_X, e=True, value=global_max_scale_X) #new

    set_undo_redo_and_generate()

slider_global_min_scale_X = cmds.floatSliderGrp(
    label="Global Min Scale (X)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_min_scale_X,
    changeCommand=set_global_min_scale_X
)

slider_global_max_scale_X = cmds.floatSliderGrp(
    label="Global Max Scale (X)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_max_scale_X,
    changeCommand=set_global_max_scale_X
)   

def set_global_min_scale_Y(value):
    global global_min_scale_Y
    value = float(value)

    if value > global_max_scale_Y:
        value = global_max_scale_Y
    global_min_scale_Y = value
    cmds.floatSliderGrp(slider_global_min_scale_Y, e=True, value=global_min_scale_Y) #new

    set_undo_redo_and_generate()

def set_global_max_scale_Y(value):
    global global_max_scale_Y
    value = float(value)

    if value < global_min_scale_Y:
        value = global_min_scale_Y
    global_max_scale_Y = value  
    cmds.floatSliderGrp(slider_global_max_scale_Y, e=True, value=global_max_scale_Y) #new

    set_undo_redo_and_generate()

slider_global_min_scale_Y = cmds.floatSliderGrp(
    label="Global Min Scale (Y)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_min_scale_Y,
    changeCommand=set_global_min_scale_Y
)

slider_global_max_scale_Y = cmds.floatSliderGrp(
    label="Global Max Scale (Y)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_max_scale_Y,
    changeCommand=set_global_max_scale_Y
)

def set_global_min_scale_Z(value):
    global global_min_scale_Z
    value = float(value)

    if value > global_max_scale_Z:
        value = global_max_scale_Z
    global_min_scale_Z = value
    cmds.floatSliderGrp(slider_global_min_scale_Z, e=True, value=global_min_scale_Z) #new

    set_undo_redo_and_generate()

def set_global_max_scale_Z(value):
    global global_max_scale_Z
    value = float(value)

    if value < global_min_scale_Z:
        value = global_min_scale_Z
    global_max_scale_Z = value
    cmds.floatSliderGrp(slider_global_max_scale_Z, e=True, value=global_max_scale_Z) #new

    set_undo_redo_and_generate()

slider_global_min_scale_Z = cmds.floatSliderGrp(
    label="Global Min Scale (Z)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_min_scale_Z,
    changeCommand=set_global_min_scale_Z
)

slider_global_max_scale_Z = cmds.floatSliderGrp(
    label="Global Max Scale (Z)",
    field=True,
    minValue=-50,
    maxValue=50,
    value=global_max_scale_Z,
    changeCommand=set_global_max_scale_Z
)

cmds.setParent('..')  # end frameLayout (sub-tab)

#globals: translate -----------------------------
global_transform_frame = cmds.frameLayout(
    label="Global Translate",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_global_min_tran_X(value):
    global global_min_tran_X
    value = float(value)
    
    if value > global_max_tran_X:
        value = global_max_tran_X
    global_min_tran_X = value    
    cmds.floatSliderGrp(slider_global_min_tran_X, e=True, value=global_min_tran_X) #new

    set_undo_redo_and_generate()

def set_global_max_tran_X(value):
    global global_max_tran_X
    value = float(value)

    if value < global_min_tran_X:
        value = global_min_tran_X
    global_max_tran_X = value
    cmds.floatSliderGrp(slider_global_max_tran_X, e=True, value=global_max_tran_X) #new

    set_undo_redo_and_generate()

slider_global_min_tran_X = cmds.floatSliderGrp(
    label="Global Min Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_min_tran_X,
    changeCommand=set_global_min_tran_X
)

slider_global_max_tran_X = cmds.floatSliderGrp(
    label="Global Max Translate (X)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_max_tran_X,
    changeCommand=set_global_max_tran_X
)   

def set_global_min_tran_Y(value):
    global global_min_tran_Y
    value = float(value)

    if value > global_max_tran_Y:
        value = global_max_tran_Y
    global_min_tran_Y = value
    cmds.floatSliderGrp(slider_global_min_tran_Y, e=True, value=global_min_tran_Y) #new

    set_undo_redo_and_generate()

def set_global_max_tran_Y(value):
    global global_max_tran_Y
    value = float(value)

    if value < global_min_tran_Y:
        value = global_min_tran_Y
    global_max_tran_Y = value  
    cmds.floatSliderGrp(slider_global_max_tran_Y, e=True, value=global_max_tran_Y) #new

    set_undo_redo_and_generate()

slider_global_min_tran_Y = cmds.floatSliderGrp(
    label="Global Min Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_min_tran_Y,
    changeCommand=set_global_min_tran_Y
)

slider_global_max_tran_Y = cmds.floatSliderGrp(
    label="Global Max Translate (Y)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_max_tran_Y,
    changeCommand=set_global_max_tran_Y
)

def set_global_min_tran_Z(value):
    global global_min_tran_Z
    value = float(value)

    if value > global_max_tran_Z:
        value = global_max_tran_Z
    global_min_tran_Z = value
    cmds.floatSliderGrp(slider_global_min_tran_Z, e=True, value=global_min_tran_Z) #new

    set_undo_redo_and_generate()

def set_global_max_tran_Z(value):
    global global_max_tran_Z
    value = float(value)

    if value < global_min_tran_Z:
        value = global_min_tran_Z
    global_max_tran_Z = value
    cmds.floatSliderGrp(slider_global_max_tran_Z, e=True, value=global_max_tran_Z) #new

    set_undo_redo_and_generate()

slider_global_min_tran_Z = cmds.floatSliderGrp(
    label="Global Min Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_min_tran_Z,
    changeCommand=set_global_min_tran_Z
)

slider_global_max_tran_Z = cmds.floatSliderGrp(
    label="Global Max Translate (Z)",
    field=True,
    minValue=-100,
    maxValue=100,
    value=global_max_tran_Z,
    changeCommand=set_global_max_tran_Z
)

cmds.setParent('..')  # end frameLayout (sub-tab)

#globals: rotation ------------------------------
global_transform_frame = cmds.frameLayout(
    label="Global Rotation",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = subsub_color,
    mw=5, mh=5
)

def set_global_min_rot_X(value):
    global global_min_rot_X
    value = float(value)

    if value > global_max_rot_X:
        value = global_max_rot_X   
    global_min_rot_X = value
    cmds.floatSliderGrp(slider_global_min_rot_X, e=True, value=global_min_rot_X) #new

    set_undo_redo_and_generate()

def set_global_max_rot_X(value):
    global global_max_rot_X
    value = float(value)

    if value < global_min_rot_X:
        value = global_min_rot_X
    global_max_rot_X = value
    cmds.floatSliderGrp(slider_global_max_rot_X, e=True, value=global_max_rot_X) #new

    set_undo_redo_and_generate()

slider_global_min_rot_X = cmds.floatSliderGrp(
    label="Global Min Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_min_rot_X,
    changeCommand=set_global_min_rot_X
)

slider_global_max_rot_X = cmds.floatSliderGrp(
    label="Global Max Rotation (X)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_max_rot_X,
    changeCommand=set_global_max_rot_X
)

def set_global_min_rot_Y(value):
    global global_min_rot_Y
    value = float(value)

    if value > global_max_rot_Y:
        value = global_max_rot_Y   
    global_min_rot_Y = value
    cmds.floatSliderGrp(slider_global_min_rot_Y, e=True, value=global_min_rot_Y) #new

    set_undo_redo_and_generate()

def set_global_max_rot_Y(value):
    global global_max_rot_Y
    value = float(value)

    if value < global_min_rot_Y:
        value = global_min_rot_Y
    global_max_rot_Y = value 
    cmds.floatSliderGrp(slider_global_max_rot_Y, e=True, value=global_max_rot_Y) #new

    set_undo_redo_and_generate() 

slider_global_min_rot_Y = cmds.floatSliderGrp(
    label="Global Min Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_min_rot_Y,
    changeCommand=set_global_min_rot_Y
)

slider_global_max_rot_Y = cmds.floatSliderGrp(
    label="Global Max Rotation (Y)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_max_rot_Y,
    changeCommand=set_global_max_rot_Y
)

def set_global_min_rot_Z(value):
    global global_min_rot_Z
    value = float(value)

    if value > global_max_rot_Z:
        value = global_max_rot_Z   
    global_min_rot_Z = value
    cmds.floatSliderGrp(slider_global_min_rot_Z, e=True, value=global_min_rot_Z) #new

    set_undo_redo_and_generate()

def set_global_max_rot_Z(value):
    global global_max_rot_Z
    value = float(value)

    if value < global_min_rot_Z:
        value = global_min_rot_Z
    global_max_rot_Z = value
    cmds.floatSliderGrp(slider_global_max_rot_Z, e=True, value=global_max_rot_Z) #new

    set_undo_redo_and_generate()

slider_global_min_rot_Z = cmds.floatSliderGrp(
    label="Global Min Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_min_rot_Z,
    changeCommand=set_global_min_rot_Z
)        

slider_global_max_rot_Z = cmds.floatSliderGrp(
    label="Global Max Rotation (Z)",
    field=True,
    minValue=-180,
    maxValue=180,
    value=global_max_rot_Z,
    changeCommand=set_global_max_rot_Z
)

cmds.setParent('..')  # end frameLayout
cmds.setParent('..')  # end frameLayout (tab)
cmds.setParent('..')  # end frameLayout (sub-tab)



#base planes: hide ---------------------------
global_transform_frame = cmds.frameLayout(
    label="Base Plane Settings",
    collapsable=True,
    collapse=True,        # set False if you want it open by default
    bgc = sub_color,
    mw=5, mh=5
)

cmds.rowLayout(numberOfColumns=3, columnWidth3=(150, 150, 150))
cmds.separator(style="none")   # left empty space

def set_hide_base_planes(value):
    global hide_base_planes
    hide_base_planes = value

    set_undo_redo_and_generate()

checkbox_hide_base_planes = cmds.checkBox(
    label="Hide Base Plane",
    value=False,
    changeCommand=set_hide_base_planes
)

cmds.separator(style="none")   # right empty space
cmds.setParent("..")
cmds.setParent("..")

cmds.separator(height=1, style="none")  # just blank space



#copy to clipboard ----------------------------
cmds.button(label='Copy Settings to Clipboard', command=copySettings, bgc = sub_color)
cmds.separator(height=2, style="none")  # just blank space

#set settings to previously copied settings
cmds.button(label='Set Settings to previously Copied', command=set_to_copied_settings, bgc = sub_color)
cmds.separator(height=5, style="none")  # just blank space
cmds.separator(height=25, style="single")  # just blank space



#generate buttons -----------------------------
cmds.text(label=" Generate", align="left", font="boldLabelFont")
cmds.separator(height=10, style="none")

cmds.button(label='GENERATE (erases all previous gens)', command=lambda *args: set_undo_redo_and_generate("Generate"), bgc = sub_color)
cmds.separator(height=2, style="none")  # just blank space
cmds.button(label='RE-GENERATE (keeps all previous gens)', command=lambda *args: set_undo_redo_and_generate("Regenerate"), bgc = sub_color)



#afficher la fenêtre
cmds.showWindow()
cmds.window(window, edit=True, widthHeight=(434, 559))
retab_existing_gens()