
# function tags are for troubleshooting later when we need to name each function without having to call the function full name.
# eg.  -----------------------------------[#tagNumber]




import maya.cmds as cmds

# Depending on user's choice in UI, "Biped" or "Quadruped", "Arm" or "Leg", we will check if the controllers actually exists in the scene.
controller_dict = {
    "Biped": {
        "Arm": {
            "L": {
                "IK":["L_shoulder_IK_ctrl", "L_elbow_IK_ctrl", "L_wrist_IK_ctrl"],
                "FK":["L_shoulder_FK_ctrl", "L_elbow_FK_ctrl", "L_wrist_FK_ctrl"]
            },
            "R": {
                "IK":["R_shoulder_IK_ctrl", "R_elbow_IK_ctrl", "R_wrist_IK_ctrl"],
                "FK":["R_shoulder_FK_ctrl", "R_elbow_FK_ctrl", "R_wrist_FK_ctrl"]
            }
        },
        "Leg": {
            "L": {
                "IK":["L_hip_IK_ctrl", "L_knee_IK_ctrl", "L_ankle_IK_ctrl"],
                "FK":["L_hip_FK_ctrl", "L_knee_FK_ctrl", "L_ankle_FK_ctrl"]
            },
            "R": {
                "IK":["R_hip_IK_ctrl", "R_knee_IK_ctrl", "R_ankle_IK_ctrl"],
                "FK":["R_hip_FK_ctrl", "R_knee_FK_ctrl", "R_ankle_FK_ctrl"]
            }
        }
    },

    "Quadruped": {
        "Front": {
            "L": {
                "IK":["L_humerus_IK_ctrl", "L_radius_IK_ctrl", "L_carpus_IK_ctrl", "L_metacarpus_IK_ctrl"],
                "FK":["L_humerus_FK_ctrl", "L_radius_FK_ctrl", "L_carpus_FK_ctrl", "L_metacarpus_FK_ctrl"]
            },
            "R": {
                "IK":["R_humerus_IK_ctrl", "R_radius_IK_ctrl", "R_carpus_IK_ctrl", "R_metacarpus_IK_ctrl"],
                "FK":["R_humerus_FK_ctrl", "R_radius_FK_ctrl", "R_carpus_FK_ctrl", "R_metacarpus_FK_ctrl"]
            }
        },
        "Rear": {
            "L": {
                "IK":["L_femur_IK_ctrl", "L_tibia_IK_ctrl", "L_tarsus_IK_ctrl", "L_metatarsus_IK_ctrl"],
                "FK":["L_femur_FK_ctrl", "L_tibia_FK_ctrl", "L_tarsus_FK_ctrl", "L_metatarsus_FK_ctrl"]
            },
            "R": {
                "IK":["R_femur_IK_ctrl", "R_tibia_IK_ctrl", "R_tarsus_IK_ctrl", "R_metatarsus_IK_ctrl"],
                "FK":["R_femur_FK_ctrl", "R_tibia_FK_ctrl", "R_tarsus_FK_ctrl", "R_metatarsus_FK_ctrl"]
            }
        }
    }
}
# Full joint chain for quadruped:
# Front
#   humerus -> radius -> carpus -> metacarpus -> phalanges
# Rear
#   femur -> tibia -> tarsus -> metatarsus -> phalanges






                                        # UI Functions #

# ---------------------------------------------------------------------------------------------------[0.0]
def openUI():
    # Notes:
    # The Limb Type dropdown should change based on the Rig Type selection.
    # If the user selects Biped, the Limb Type dropdown should show Arm and Leg.
    # If the user selects Quadruped, the Limb Type dropdown should show Front and Rear.
    # But the limb side dropdown will always show L and R, because both biped and quadruped have left and right limbs.

    # If window already exists, close it and create a new one.
    if cmds.window("rigging_tool_window", exists=True):
        cmds.deleteUI("rigging_tool_window")

    window = cmds.window(
        "rigging_tool_window",
        title="metaTools Auto Rigger v0.2",
        width=260,
        height=140,
        sizeable=False
    )

    # Main vertical stack with left/right margins
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6,
        columnAttach=("both", 10)
    )

    # Heading
    cmds.separator(height=6, style="none")

    cmds.text(
        label="< metaTools Auto Limb Rigger v0.2 >",
        align="center",
        height=10
    )

    cmds.separator(height=8, style="single")

    cmds.text(
        label="This tool automates the IK/FK blended system for Bipedal and Quadrupedal Rigs.",
        align="center",
        height=20
    )
    cmds.text(
        label="* The tool does not generate controllers for user *",
        align="center",
        height=20
    )

    # Separator
    cmds.separator(height=8, style="single")

    # Rig Type dropdown
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(12, 216, 12),
        adjustableColumn=2
    )
    cmds.text(label="")

    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(65, 120),
        columnAlign2=("left", "left"),
        adjustableColumn=2
    )
    cmds.text(label="Rig Type :")
    cmds.optionMenu("rig_type_menu", width=120, changeCommand=update_ui_options)
    cmds.menuItem(label="Biped")
    cmds.menuItem(label="Quadruped")
    cmds.setParent("..")

    cmds.text(label="")
    cmds.setParent("..")

    # Limb Type dropdown
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(12, 216, 12),
        adjustableColumn=2
    )
    cmds.text(label="")

    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(65, 120),
        columnAlign2=("left", "left"),
        adjustableColumn=2
    )
    cmds.text(label="Limb Type :")
    cmds.optionMenu("limb_type_menu", width=120)
    cmds.menuItem(label="Arm")
    cmds.menuItem(label="Leg")
    cmds.setParent("..")

    cmds.text(label="")
    cmds.setParent("..")

    # Limb Side dropdown
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(12, 216, 12),
        adjustableColumn=2
    )
    cmds.text(label="")

    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(65, 120),
        columnAlign2=("left", "left"),
        adjustableColumn=2
    )
    cmds.text(label="Limb Side :")
    cmds.optionMenu("limb_side_menu", width=120)
    cmds.menuItem(label="L")
    cmds.menuItem(label="R")
    cmds.setParent("..")

    cmds.text(label="")
    cmds.setParent("..")

    # Separator
    cmds.separator(height=10, style="single")

    # Build Rig button
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(28, 180, 28),
        adjustableColumn=2
    )
    cmds.text(label="")
    cmds.button(
        label="Build Rig",
        width=150,
        height=30,
        command=building_rig_router
    )
    cmds.text(label="")
    cmds.setParent("..")

    # Note to self:
    # Here I didn't write building_rig_router() with parentheses because I want to pass the function itself as a callback, not the result of the function call.
    # If I put parentheses, it will execute the function immediately when the button is created, which is not what I want.
    # I want the function to execute only when the button is clicked.

    cmds.separator(height=4, style="none")
    cmds.text(label="Contact: khantarkarzwe@gmail.com", align="center")
    cmds.separator(height=6, style="none")

    cmds.showWindow(window)


# ---------------------------------------------------------------------------------------------------[0.1]
def update_ui_options(*args):
    rig_type = cmds.optionMenu("rig_type_menu", query=True, value=True)
    old_items = cmds.optionMenu("limb_type_menu", query=True, itemListLong=True) or []

    for item in old_items:
        cmds.deleteUI(item)

    if rig_type == "Biped":
        cmds.menuItem(label="Arm", parent="limb_type_menu")
        cmds.menuItem(label="Leg", parent="limb_type_menu")

    elif rig_type == "Quadruped":
        cmds.menuItem(label="Front", parent="limb_type_menu")
        cmds.menuItem(label="Rear", parent="limb_type_menu")

    else:
        cmds.error(f"Unsupported rig type: {rig_type}")


# ---------------------------------------------------------------------------------------------------[0.2]
def checking_UI_selection():
    # This function is closely connected to the UI.
    # We will be using dropdown menus for the user input data.
    # This function will check if the user has made valid selections in the UI. If not, it will raise an error.
    
    # Get user selections from the UI
    rig_type = cmds.optionMenu("rig_type_menu", query=True, value=True)
    limb_type = cmds.optionMenu("limb_type_menu", query=True, value=True)
    limb_side = cmds.optionMenu("limb_side_menu", query=True, value=True)

    # As Biped arm has finger joints branching from the wrist, max_joint will be limited to 3 for arm to prevent the finger joints from being included in the chain. For Biped leg and Quadruped limbs, max_joint will be 5 as there is no branching joint in the main limb chain.
    if rig_type == "Biped":
        if limb_type == "Arm":  # We will use fingers joints from bind joint system
            total_source_joints = 3
            total_blend_joints = 3
        elif limb_type == "Leg":  
            total_source_joints = 5
            total_blend_joints = 3
        else:
            cmds.error(f"Unsupported limb type for Biped: {limb_type}")

    elif rig_type == "Quadruped":
        total_source_joints = 5
        total_blend_joints = 4
    else:
        cmds.error(f"Unsupported rig type: {rig_type}")

    return rig_type, limb_type, limb_side, total_source_joints, total_blend_joints






                                        # Main Router Function #

# ---------------------------------------------------------------------------------------------------[1.0]
def building_rig_router(*args):
    # This function will be the main router that calls other functions in the correct order. It will also pass the necessary data between functions.

    rig_type, limb_type, limb_side, total_source_joints, total_blend_joints = checking_UI_selection()
    joint_root = checking_joint_selection(rig_type, limb_type, limb_side)
    checking_controllers(rig_type, limb_type, limb_side)
    chain = hierarchy_forming(joint_root, total_source_joints)
    created_joint_systems = creating_joints(chain, rig_type, total_source_joints)
    if rig_type == "Biped":
        connecting_fk_controls_biped_quadruped(created_joint_systems, rig_type, limb_type, limb_side)
        creating_ik_handles_biped(chain, rig_type, limb_type, limb_side)
        blending_IKFK_biped(chain, created_joint_systems, total_blend_joints, rig_type, limb_type, limb_side)
    elif rig_type == "Quadruped":
        connecting_fk_controls_biped_quadruped(created_joint_systems, rig_type, limb_type, limb_side)
        creating_ik_handles_quadruped(chain, rig_type, limb_type, limb_side)
        blending_IKFK_quadruped(chain, created_joint_systems, total_blend_joints, rig_type, limb_type, limb_side)
    else:
        cmds.error(f"Unsupported rig type: {rig_type}")






                                        # Validation Functions #

# ---------------------------------------------------------------------------------------------------[2.0]
def checking_joint_selection(rig_type, limb_type, limb_side):
    # Check current selection and return the root joint.
    # Assumption:
    #       User selects at least one joint
    #       The first selected joint is treated as the root

    selected_joints = cmds.ls(sl=True, type="joint") or []

    if not selected_joints:
        cmds.error("Please select the root joint to start the rigging process")
        
    joint_root = selected_joints[0]

    # Check limb side prefix for Biped and Quadruped
    if limb_side == "L":
        if joint_root[:2] == "L_":
            pass
        else:
            cmds.error(f"Selected root joint: {joint_root} does not have the expected limb side prefix (L_) that matches the UI selection: {limb_side}")
    elif limb_side == "R":
        if joint_root[:2] == "R_":
            pass
        else:
            cmds.error(f"Selected root joint: {joint_root} does not have the expected limb side prefix (R_) that matches the UI selection: {limb_side}")
    else:
        cmds.error(f"Selected root joint: {joint_root} does not have the expected limb side prefix (L_ or R_) that matches the UI selection: {limb_side}")

    # Check limb type suffix matching and name for Biped
    if rig_type == "Biped":
        if limb_type == "Arm" and joint_root[-9:] == "_shoulder":
            pass
        elif limb_type == "Leg" and joint_root[-4:] == "_hip":
            pass
        else:
            cmds.error(f"Selected root joint: {joint_root} does not have expected limb type suffix (_shoulder or _hip) that matches the UI selection: {limb_type}")

    # Check limb type suffix matching and name for Quadruped
    if rig_type == "Quadruped":
        if limb_type == "Front" and joint_root[-8:] == "_humerus":
            pass
        elif limb_type == "Rear" and joint_root[-6:] == "_femur":
            pass
        else:
            cmds.error(f"Selected root joint: {joint_root} does not have expected limb type suffix (_humerus or _femur) that matches the UI selection: {limb_type}")
    
    return joint_root


# ---------------------------------------------------------------------------------------------------[2.1]
def checking_controllers(rig_type, limb_type, limb_side):
    # This loop will check if each controller exists in the scene
    for system_temp in ["IK", "FK"]:
        for ctrl in controller_dict[rig_type][limb_type][limb_side][system_temp]:
            if not cmds.objExists(ctrl):
                cmds.error(f"Controller does not exist: {ctrl}")

    # This part will check if the IKFK switch controller exists and has the expected attribute with the expected range. This is important because the blending function relies on this controller and attribute to work properly.
    
    # Check if the IKFK switch controller exists
    ikfk_switch_ctrl = limb_side + "_" + limb_type + "_IKFKswitch_ctrl" # e.g. L_Arm_IKFKswitch_ctrl (Name of IKFK switch controller in the scene)
    
    if not cmds.objExists(ikfk_switch_ctrl):
        cmds.error(f"Controller does not exist: {ikfk_switch_ctrl}")

    # Check if the switch attribute exists
    if not cmds.attributeQuery("IKFKswitch", node=ikfk_switch_ctrl, exists=True):
        cmds.error(f"Controller {ikfk_switch_ctrl} does not have the expected attribute: IKFKswitch")

    # Check attribute type
    ikfk_switch_attr_type = cmds.getAttr(f"{ikfk_switch_ctrl}.IKFKswitch", type=True)
    if ikfk_switch_attr_type not in ["float", "double"]:
        cmds.error(
            f"Attribute {ikfk_switch_ctrl}.IKFKswitch is not a float type. "
            f"Current data type: {ikfk_switch_attr_type}"
        )

    # Check that both min and max exist
    if not cmds.attributeQuery("IKFKswitch", node=ikfk_switch_ctrl, rangeExists=True):
        cmds.error(f"Attribute {ikfk_switch_ctrl}.IKFKswitch does not have a full 0 to 1 range defined")

    # Get both values at once
    min_value, max_value = cmds.attributeQuery("IKFKswitch", node=ikfk_switch_ctrl, range=True)

    # Validate expected range
    if min_value != 0.0 or max_value != 1.0:
        cmds.error(
            f"Attribute {ikfk_switch_ctrl}.IKFKswitch does not have the expected value range of 0 to 1. "
            f"Current range: {min_value} to {max_value}"
        )






                                        # Builder Functions #

# ---------------------------------------------------------------------------------------------------[3.0]
def hierarchy_forming(joint_root, total_source_joints):
    # Build a *single-path* joint chain starting from the given root.
    #
    # Why single-path?
    # A biped leg often has extra joints branching from the ankle (foot/toe).
    # A biped arm often has extra joints branching from the wrist (knuckles/fingers).
    # Using `ad=True` (all descendants) can pull in those extras and confuse downstream logic.
    #
    # Args:
    #     joint_root (str): root joint of the limb chain (e.g., L_hip)
    #     total_source_joints (int): the total number of joints to include in the chain
    #                      (biped arm/leg is typically 3: hip->knee->ankle)
    #
    # Returns:
    #     List[str]: ordered joint chain from root -> end, length == max_joints
    #
    # Raises:
    #     Maya error if the chain cannot reach total_source_joints.
    if total_source_joints < 1:
        cmds.error(f"Invalid total_source_joints value: {total_source_joints}.")
    # Above state is safeguard to prevent potential UX issues and user error
    # If the user ever has to input total source joint count, this safeguard will prevent 0 (null) values and wrong execution

    chain = [joint_root]
    current = joint_root

    while len(chain) < total_source_joints:
        children = cmds.listRelatives(current, children=True, type="joint") or []
        # children=True returns all adjacent child (or) children but ad=True returns all children, grandchildren, great grandchildren
        # We are checking if there are more than one adjacent child that is under each joint that goes through here.
        # We are checking if there is branching (eg. Wrist to fingers)
        if not children:
            cmds.error(
                f"Joint chain too short. Reached {len(chain)} joint(s), expected {total_source_joints}. "
                f"Stopped at: {current}"
            )

        if len(children) > 1:
            # We deliberately pick a deterministic path for v02.
            # Later we can add validation/UI to choose which branch to follow.
            cmds.warning(
                f"Multiple joint children under {current}: {children}. "
                f"Using the first child: {children[0]}"
            )

        current = children[0]
        chain.append(current)
        # When it reaches here, every time the input passes here, the root joint gets each joint (the first being its child) as its append
    return chain # e.g. [L_hip, L_knee, L_ankle] / [L_shoulder, L_elbow, L_wrist]


def debugging_print_chain(total_source_joints):
    pass

# ---------------------------------------------------------------------------------------------------[3.1]
def creating_joints(chain, rig_type, total_source_joints):
# In this function, "chain" becomes "source_chain"

    if rig_type == "Biped":
        joint_system_suffixes = ["IK", "FK"]
    if rig_type == "Quadruped":
        joint_system_suffixes = ["driver", "IK", "FK"]

    created_joint_systems = {}

    if len(chain)<total_source_joints:
        cmds.error(
            f"Chain length ({len(chain)}) is shorter than maximum number of joints: {total_source_joints}"
        )
    
    source_chain = chain[:total_source_joints]

    for suffix in joint_system_suffixes:
        new_chain = []
        parent_joint = None

        for source_joint in source_chain:
            new_joint_name = source_joint + "_" + suffix

            if cmds.objExists(new_joint_name):
                cmds.error(f"Joint already exists: {new_joint_name}")

            duplicated_joint = cmds.duplicate(source_joint, parentOnly=True, name=new_joint_name)[0]

            if parent_joint:
                cmds.parent(duplicated_joint, parent_joint)
            
            new_chain.append(duplicated_joint)
            parent_joint=duplicated_joint
        
        created_joint_systems[suffix]=new_chain
    
    return created_joint_systems 
    # e.g. created_joint_systems={
    #           "IK": [L_shoulder_IK, L_elbow_IK, L_wrist_IK],
    #           "FK": [L_shoulder_FK, L_elbow_FK, L_wrist_FK]
    #      }



def debugging_print_created_systems():
    pass

# Later I will check constraints, for future tool that deletes the rig for the user if they no longer need the rig.
def debugging_print_check_constraints():
    pass



# Common module #
# ---------------------------------------------------------------------------------------------------[3.2]
def connecting_fk_controls_biped_quadruped(created_joint_systems, rig_type, limb_type, limb_side):
    
    fk_control = controller_dict[rig_type][limb_type][limb_side]["FK"]
    max_ctrls = len(fk_control)
    
    for i in range(max_ctrls):
        cmds.parentConstraint(fk_control[i], created_joint_systems["FK"][i], w=1, mo=0)
        # maintain offset is set to 0 here, to make user's controller alignment error visible.
        if i>0:
            child_ctrl_offset = fk_control[i] + "_off"
            parent_control = fk_control[i-1]

            if not child_ctrl_offset:
                cmds.error(f"FK controller, {fk_control}, does not have offset node, {child_ctrl_offset}.")

            cmds.parent(child_ctrl_offset, parent_control)

# Biped modules #
# ---------------------------------------------------------------------------------------------------[3.3]
def creating_ik_handles_biped(chain, rig_type, limb_type, limb_side):
    cmds.ikHandle(n=(limb_side + "_" + limb_type + "_RP_ikHandle"), sol="ikRPsolver", sj=(chain[0] + "_IK"), ee=(chain[2] + "_IK"))
    cmds.parent((limb_side + "_" + limb_type + "_RP_ikHandle"), controller_dict[rig_type][limb_type][limb_side]["IK"][2])

    # This lets the IK wrist controller to have control over rotation while in IK mode
    if limb_type == "Arm":
        cmds.orientConstraint(controller_dict[rig_type][limb_type][limb_side]["IK"][2], chain[2] + "_IK", w=1, mo=1)

    # pole vector constraint to the elbow/knee controller
    cmds.poleVectorConstraint(controller_dict[rig_type][limb_type][limb_side]["IK"][1], (limb_side + "_" + limb_type + "_RP_ikHandle"), w=1)


# ---------------------------------------------------------------------------------------------------[3.4]
def blending_IKFK_biped(chain, created_joint_systems, total_blend_joints, rig_type, limb_type, limb_side):

    # This blending function assumes that there is a seperate IKFK switch control with a float attribute named "IKFKswitch" that goes from 0 (full IK) to 1 (full FK).
    limb_name = limb_side + "_" + limb_type

    switch_ctrl = limb_name + "_IKFKswitch_ctrl"
    switch_attr = switch_ctrl + ".IKFKswitch"

    reverse_node = cmds.createNode("reverse", n=limb_name + "_IKFK_reverse")
    cmds.connectAttr(switch_attr, reverse_node + ".inputX", f=True)

    for i in range(total_blend_joints):
        bind_joint = chain[i]
        ik_joint = created_joint_systems["IK"][i]   # e.g. L_knee_IK
        fk_joint = created_joint_systems["FK"][i]   # e.g. L_knee_FK

        # 1) Create offset group for blended result
        ikfk_off = cmds.group(em=True, n=bind_joint + "_IKFK_off")
        cmds.matchTransform(ikfk_off, bind_joint)

        # 2) Matrix nodes for IK
        multMatrix_ik = cmds.shadingNode("multMatrix", au=True, n=ik_joint + "_multMatrix")
        decomposeMatrix_ik = cmds.shadingNode("decomposeMatrix", au=True, n=ik_joint + "_decomposeMatrix")

        # 3) Matrix nodes for FK
        multMatrix_fk = cmds.shadingNode("multMatrix", au=True, n=fk_joint + "_multMatrix")
        decomposeMatrix_fk = cmds.shadingNode("decomposeMatrix", au=True, n=fk_joint + "_decomposeMatrix")

        # 4) PairBlend node
        pairBlend = cmds.createNode("pairBlend", n=bind_joint + "_IKFK_pairBlend")
        cmds.setAttr(pairBlend + ".rotInterpolation", 1)  # Quaternion

        # ----- IK world -> local space of offset
        cmds.connectAttr(ik_joint + ".worldMatrix[0]", multMatrix_ik + ".matrixIn[0]", f=True)
        cmds.connectAttr(ikfk_off + ".parentInverseMatrix[0]", multMatrix_ik + ".matrixIn[1]", f=True)
        cmds.connectAttr(multMatrix_ik + ".matrixSum", decomposeMatrix_ik + ".inputMatrix", f=True)

        # ----- FK world -> local space of offset
        cmds.connectAttr(fk_joint + ".worldMatrix[0]", multMatrix_fk + ".matrixIn[0]", f=True)
        cmds.connectAttr(ikfk_off + ".parentInverseMatrix[0]", multMatrix_fk + ".matrixIn[1]", f=True)
        cmds.connectAttr(multMatrix_fk + ".matrixSum", decomposeMatrix_fk + ".inputMatrix", f=True)

        # ----- Feed pairBlend
        cmds.connectAttr(decomposeMatrix_ik + ".outputTranslate", pairBlend + ".inTranslate1", f=True)
        cmds.connectAttr(decomposeMatrix_ik + ".outputRotate", pairBlend + ".inRotate1", f=True)

        cmds.connectAttr(decomposeMatrix_fk + ".outputTranslate", pairBlend + ".inTranslate2", f=True)
        cmds.connectAttr(decomposeMatrix_fk + ".outputRotate", pairBlend + ".inRotate2", f=True)

        cmds.connectAttr(switch_attr, pairBlend + ".weight", f=True)

        # ----- Output blended motion to offset group
        cmds.connectAttr(pairBlend + ".outTranslate", ikfk_off + ".translate", f=True)
        cmds.connectAttr(pairBlend + ".outRotate", ikfk_off + ".rotate", f=True)

        # ----- Offset drives bind joint
        cmds.parentConstraint(ikfk_off, bind_joint, w=1, mo=1)

    # Visibility switching
    for ctrl in controller_dict[rig_type][limb_type][limb_side]["IK"]:
            cmds.connectAttr(reverse_node + ".outputX", ctrl + ".visibility", f=True)
    for ctrl in controller_dict[rig_type][limb_type][limb_side]["FK"]:
            cmds.connectAttr(switch_attr, ctrl + ".visibility", f=True)
    


# Quadruped modules #
# ---------------------------------------------------------------------------------------------------[3.5]
def creating_ik_handles_quadruped(chain, rig_type, limb_type, limb_side):
    if not cmds.pluginInfo("ikSpringSolver", q=1, l=1):                                                                                             # [MODULE] Quad IK setup
        cmds.loadPlugin("ikSpringSolver")

    if limb_type == "Front":
        j0 = "humerus"
        j1 = "radius"
        j2 = "carpus"
        j3 = "metacarpus"
        j4 = "phalanges"
    
    if limb_type == "Rear":
        j0 = "femur"
        j1 = "tibia"
        j2 = "tarsus"
        j3 = "metatarsus"
        j4 = "phalanges"

    # [1] Spring solver for the driver joint system
    cmds.ikHandle(n=(limb_side + "_" + limb_type + "_" + j0 + "_" + j3 + "_driver_SS_ikHandle"), sol="ikSpringSolver", sj=(chain[0] + "_driver"), ee=(chain[3] + "_driver"))

    # [2] RP solver for the IK (or bind in old version)joint system, for both Knee PV and control over hock
    cmds.ikHandle(n=(limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_ikHandle"), sol="ikRPsolver", sj=(chain[0] + "_IK"), ee=(chain[2] + "_IK"))

    # [3] SC solver for the IK (or bind in old version) joint system, for the control over the tarsus/carpus joint.
    cmds.ikHandle(n=(limb_side + "_" + limb_type + "_" + j2 + "_" + j3 + "_IK_SC_ikHandle"), sol="ikSCsolver", sj=(chain[2] + "_IK"), ee=(chain[3] + "_IK"))

    # [4] SC solver for the IK (or bind in old version) joint system, for stabilising the phalanges tip joint
    cmds.ikHandle(n=(limb_side + "_" + limb_type + "_" + j3 + "_" + j4 + "_IK_SC_ikHandle"), sol="ikSCsolver", sj=(chain[3] + "_IK"), ee=(chain[4] + "_IK"))


    # Parenting

    # [1] and [4] are parented under the j3 (metacarpus/metatarsus) Control
    cmds.parent((limb_side + "_" + limb_type + "_" + j0 + "_" + j3 + "_driver_SS_ikHandle"), (limb_side + "_" + limb_type + "_" + j3 + "_" + j4 + "_IK_SC_ikHandle"), controller_dict[rig_type][limb_type][limb_side]["IK"][3])

    # [3] is parented under the j3 (metacarpus/metatarsus) joint
    cmds.parent((limb_side + "_" + limb_type + "_" + j2 + "_" + j3 + "_IK_SC_ikHandle"), (chain[3] + "_driver"))

                                                                                                                                                        # [MODULE] Quad IK setup
    # [2] is parented under a group node that is placed at the j3 (metacarpus/metatarsus) joint

    # Just a group node, because I dont want the RPikHandle to be parented under it yet
    cmds.group(em=1, n=(limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"))
    # Match the group node transformation to the j3 (metacarpus/metatarsus) joint, to actually place the node there
    cmds.matchTransform((limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"), (chain[3] + "_driver"))
    cmds.makeIdentity((limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"), a=1, t=1, r=1, s=0)
    # Find the j3 (metacarpus/metatarsus) joint location in worldSpace so I can place the offset node's pivot there
    J3_JointLoc = cmds.xform(chain[3] + "_driver", q=1, ws=1, piv=True)
    # Place the pivot there
    cmds.xform((limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"), ws=1, piv=(J3_JointLoc[0], J3_JointLoc[1], J3_JointLoc[2]))

    # Now I can finally have the RPikHandle parented under the j2 (carpus/tarsus) offset node I just played with
    cmds.parent((limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_ikHandle"), (limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"))
    cmds.parent((limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"), (chain[3] + "_driver"))


    # j2 (carpus/tarsus) control creation
    cmds.group(em=1, n=(limb_side + "_" + limb_type + "_" + j2 + "_IK_off"))
    # Place the j2 (carpus/tarsus) control group node at the j3 (metacarpus/metatarsus) joint where it will rotate the joint
    cmds.matchTransform((limb_side + "_" + limb_type + "_" + j2 + "_IK_off"), (chain[3] + "_driver"))
    cmds.makeIdentity((limb_side + "_" + limb_type + "_" + j2 + "_IK_off"), a=1, t=1, r=1, s=0)

    # parent them
    cmds.parent(controller_dict[rig_type][limb_type][limb_side]["IK"][2], (limb_side + "_" + limb_type + "_" + j2 + "_IK_off"))
    # parent it under the paw Ctrl
    cmds.parent((limb_side + "_" + limb_type + "_" + j2 + "_IK_off"), controller_dict[rig_type][limb_type][limb_side]["IK"][3])


    # Time to constraint the controllers
    # Given that the pole vector controller (kneeControlName / L_Rear_tibia_ctrl already has its offset node with its curve node from the outset)
    cmds.poleVectorConstraint(controller_dict[rig_type][limb_type][limb_side]["IK"][1], (limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_ikHandle"), w=1)
    # Constrain the hock offset node to its controller
    cmds.parentConstraint(controller_dict[rig_type][limb_type][limb_side]["IK"][2], (limb_side + "_" + limb_type + "_" + j0 + "_" + j2 + "_IK_RP_off"), w=1, mo=1)                                                 # [MODULE] Quad IK setup


# ----------------------------------------------------------------------------------------------------[3.6]
def blending_IKFK_quadruped(chain, created_joint_systems, total_blend_joints, rig_type, limb_type, limb_side):

    # This blending function assumes that there is a seperateIKFK switch control with a float attribute named "IKFKswitch" that goes from 0 (full IK) to 1 (full FK).
    limb_name = limb_side + "_" + limb_type

    switch_ctrl = limb_name + "_IKFKswitch_ctrl"
    switch_attr = switch_ctrl + ".IKFKswitch"

    reverse_node = cmds.createNode("reverse", n=limb_name + "_IKFK_reverse")
    cmds.connectAttr(switch_attr, reverse_node + ".inputX", f=True)

    for i in range(total_blend_joints):
        bind_joint = chain[i]
        ik_joint = created_joint_systems["IK"][i]   # e.g. L_shoulder_IK
        fk_joint = created_joint_systems["FK"][i]   # e.g. L_shoulder_FK

        # 1) Create offset group for blended result
        ikfk_off = cmds.group(em=True, n=bind_joint + "_IKFK_off")
        cmds.matchTransform(ikfk_off, bind_joint)

        # 2) Matrix nodes for IK
        multMatrix_ik = cmds.shadingNode("multMatrix", au=True, n=ik_joint + "_multMatrix")
        decomposeMatrix_ik = cmds.shadingNode("decomposeMatrix", au=True, n=ik_joint + "_decomposeMatrix")

        # 3) Matrix nodes for FK
        multMatrix_fk = cmds.shadingNode("multMatrix", au=True, n=fk_joint + "_multMatrix")
        decomposeMatrix_fk = cmds.shadingNode("decomposeMatrix", au=True, n=fk_joint + "_decomposeMatrix")

        # 4) PairBlend node
        pairBlend = cmds.createNode("pairBlend", n=bind_joint + "_IKFK_pairBlend")
        cmds.setAttr(pairBlend + ".rotInterpolation", 1)  # Quaternion

        # ----- IK world -> local space of offset
        cmds.connectAttr(ik_joint + ".worldMatrix[0]", multMatrix_ik + ".matrixIn[0]", f=True)
        cmds.connectAttr(ikfk_off + ".parentInverseMatrix[0]", multMatrix_ik + ".matrixIn[1]", f=True)
        cmds.connectAttr(multMatrix_ik + ".matrixSum", decomposeMatrix_ik + ".inputMatrix", f=True)

        # ----- FK world -> local space of offset
        cmds.connectAttr(fk_joint + ".worldMatrix[0]", multMatrix_fk + ".matrixIn[0]", f=True)
        cmds.connectAttr(ikfk_off + ".parentInverseMatrix[0]", multMatrix_fk + ".matrixIn[1]", f=True)
        cmds.connectAttr(multMatrix_fk + ".matrixSum", decomposeMatrix_fk + ".inputMatrix", f=True)

        # ----- Feed pairBlend
        cmds.connectAttr(decomposeMatrix_ik + ".outputTranslate", pairBlend + ".inTranslate1", f=True)
        cmds.connectAttr(decomposeMatrix_ik + ".outputRotate", pairBlend + ".inRotate1", f=True)

        cmds.connectAttr(decomposeMatrix_fk + ".outputTranslate", pairBlend + ".inTranslate2", f=True)
        cmds.connectAttr(decomposeMatrix_fk + ".outputRotate", pairBlend + ".inRotate2", f=True)

        cmds.connectAttr(switch_attr, pairBlend + ".weight", f=True)

        # ----- Output blended motion to offset group
        cmds.connectAttr(pairBlend + ".outTranslate", ikfk_off + ".translate", f=True)
        cmds.connectAttr(pairBlend + ".outRotate", ikfk_off + ".rotate", f=True)

        # ----- Offset drives bind joint
        cmds.parentConstraint(ikfk_off, bind_joint, w=1, mo=1)

    # Visibility switching
    for ctrl in controller_dict[rig_type][limb_type][limb_side]["IK"]:
            cmds.connectAttr(reverse_node + ".outputX", ctrl + ".visibility", f=True)
    for ctrl in controller_dict[rig_type][limb_type][limb_side]["FK"]:
            cmds.connectAttr(switch_attr, ctrl + ".visibility", f=True)

# [End]
