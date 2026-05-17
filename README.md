# metaTools Auto Limb Rigger v0.2

A Maya Python tool that automates IK/FK limb setup for biped and quadruped rigs.

The tool was built to reduce repetitive rigging work, keep limb rig structures consistent, and make it faster to create IK/FK blended limb systems inside Maya.


## Main Features

- Builds IK and FK duplicate joint systems from a selected bind/source limb chain.
- Supports biped arms and legs.
- Supports quadruped front and rear limbs.
- Creates IK handles for biped limbs.
- Creates a quadruped IK setup using spring, RP, and SC IK handles.
- Connects FK controls to FK joints.
- Creates IK/FK blend setup using matrix nodes, decomposeMatrix nodes, and pairBlend nodes.
- Connects the IK/FK switch attribute to IK and FK controller visibility.
- Performs validation before building the rig.

## Software / Environment

- Autodesk Maya 2025
- Python 3
- maya.cmds

## What This Tool Does

The tool takes an existing limb joint chain and existing controllers, then builds the IK/FK rig system around them.

For a biped limb, it creates:

- IK joint chain
- FK joint chain
- IK handle
- FK controller constraints
- IK/FK blend nodes
- IK/FK controller visibility switching

For a quadruped limb, it creates:

- driver joint chain
- IK joint chain
- FK joint chain
- spring solver IK handle
- RP solver IK handle
- SC solver IK handles
- FK controller constraints
- IK/FK blend nodes
- IK/FK controller visibility switching

## What This Tool Does Not Do

- It does not create controllers.
- It does not create the original bind/source skeleton.
- It does not skin the character.
- It does not create the IK/FK switch controller.
- It does not add the `IKFKswitch` attribute.
- It does not automatically decide which branch to follow when a joint has multiple children.
- It does not currently provide an undo/cleanup tool for deleting generated rig systems.

## How to Use

1. Open Maya.
2. Open the script in the Script Editor or load it into Maya's Python environment.
3. Run:

```python
metaTools_AutoLimbRigger_v02.openUI()
```

4. In the UI, choose:
   - Rig Type: `Biped` or `Quadruped`
   - Limb Type:
     - Biped: `Arm` or `Leg`
     - Quadruped: `Front` or `Rear`
   - Limb Side: `L` or `R`
5. Select the root joint of the limb chain.
6. Press **Build Rig**.

## Required Scene Setup

Before running the tool, the scene must already contain:

- A clean source/bind limb joint chain.
- IK controllers with the expected names.
- FK controllers with the expected names.
- FK controller offset groups named with `_off` suffix.
- An IK/FK switch controller.
- A numeric `IKFKswitch` attribute on the switch controller.

The `IKFKswitch` attribute must:

- Be named exactly `IKFKswitch`.
- Be on a controller named like `L_Arm_IKFKswitch_ctrl`.
- Be a float/double attribute.
- Have a value range of `0` to `1`.

Current switch meaning:

| Value | Mode |
|---:|---|
| `0` | IK |
| `1` | FK |

## Supported Limb Types

| Rig Type | Limb Type | Source Chain Length | Blend Joint Count |
|---|---|---:|---:|
| Biped | Arm | 3 | 3 |
| Biped | Leg | 5 | 3 |
| Quadruped | Front | 5 | 4 |
| Quadruped | Rear | 5 | 4 |

The biped leg reads 5 source joints so the foot/toe chain can be included for IK handle creation, but only 3 main limb joints are blended by the IK/FK system.

## Generated Joint Systems

### Biped

The tool creates:

```text
source_joint_IK
source_joint_FK
```

Example:

```text
L_shoulder
L_shoulder_IK
L_shoulder_FK
```

### Quadruped

The tool creates:

```text
source_joint_driver
source_joint_IK
source_joint_FK
```

Example:

```text
L_humerus
L_humerus_driver
L_humerus_IK
L_humerus_FK
```

## IK/FK Blending Method

For each blended bind/source joint, the tool creates:

- an offset group named `sourceJoint_IKFK_off`
- IK `multMatrix`
- IK `decomposeMatrix`
- FK `multMatrix`
- FK `decomposeMatrix`
- `pairBlend` node

The IK and FK joint transforms are converted into the local space of the blend offset group. Their translate and rotate outputs are then blended through a `pairBlend` node. The blend offset group drives the original source/bind joint through a parentConstraint.

The `pairBlend.rotInterpolation` is set to quaternion mode.

## Important Assumptions

- The selected root joint must match the UI side and limb type.
- Left side names must start with `L_`.
- Right side names must start with `R_`.
- Biped arm root must end with `_shoulder`.
- Biped leg root must end with `_hip`.
- Quadruped front root must end with `_humerus`.
- Quadruped rear root must end with `_femur`.
- Existing controllers must already be aligned to the joints.
- FK controller offset groups must use the `_off` suffix.
- Generated node names must not already exist in the scene.
- The first child joint is used when a joint has multiple children.

## Current Limitations

- Built with `maya.cmds` only.
- The tool currently expects strict naming conventions.
- Controllers must already exist before running the tool.
- FK controller alignment issues are intentionally exposed because FK constraints use `maintainOffset=False`.
- Branching joint chains are not interactively selectable yet; the tool warns and follows the first child.
- Existing generated joints or nodes with the same names will stop the build.
- The code is currently stored mostly in one script file.
- There is no automatic rollback if the build fails halfway.
- There is no dedicated UI for deleting or rebuilding an existing generated limb rig yet.

## Author

Kang — Rigging / Technical Artist
