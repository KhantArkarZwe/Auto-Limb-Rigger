

# Naming Convention — metaTools Auto Limb Rigger v0.2

This document explains the expected naming convention for the Auto Limb Rigger.

The tool relies on strict object names because it checks joints, controllers, and switch attributes before building the rig.

## Side Prefix

Every limb root and controller must start with one of these side prefixes:

| Side | Prefix |
|---|---|
| Left | `L_` |
| Right | `R_` |

Example:

```text
L_shoulder
R_hip
L_wrist_IK_ctrl
R_knee_FK_ctrl
```

## Biped Source Joint Naming

### Biped Arm

The selected root joint must end with:

```text
_shoulder
```

Expected chain:

```text
L_shoulder
└── L_elbow
    └── L_wrist
```

Right side:

```text
R_shoulder
└── R_elbow
    └── R_wrist
```

### Biped Leg

The selected root joint must end with:

```text
_hip
```

Expected source chain:

```text
L_hip
└── L_knee
    └── L_ankle
        └── L_foot
            └── L_tiptoe
```

Right side:

```text
R_hip
└── R_knee
    └── R_ankle
        └── R_foot
            └── R_tiptoe
```

## Quadruped Source Joint Naming

### Quadruped Front Limb

The selected root joint must end with:

```text
_humerus
```

Expected chain:

```text
L_humerus
└── L_radius
    └── L_carpus
        └── L_metacarpus
            └── L_phalanges
```

Right side:

```text
R_humerus
└── R_radius
    └── R_carpus
        └── R_metacarpus
            └── R_phalanges
```

### Quadruped Rear Limb

The selected root joint must end with:

```text
_femur
```

Expected chain:

```text
L_femur
└── L_tibia
    └── L_tarsus
        └── L_metatarsus
            └── L_phalanges
```

Right side:

```text
R_femur
└── R_tibia
    └── R_tarsus
        └── R_metatarsus
            └── R_phalanges
```

## Biped Controller Names

### Biped Arm — Left

```text
L_shoulder_IK_ctrl
L_elbow_IK_ctrl
L_wrist_IK_ctrl

L_shoulder_FK_ctrl
L_elbow_FK_ctrl
L_wrist_FK_ctrl

L_Arm_IKFKswitch_ctrl
```

### Biped Arm — Right

```text
R_shoulder_IK_ctrl
R_elbow_IK_ctrl
R_wrist_IK_ctrl

R_shoulder_FK_ctrl
R_elbow_FK_ctrl
R_wrist_FK_ctrl

R_Arm_IKFKswitch_ctrl
```

### Biped Leg — Left

```text
L_hip_IK_ctrl
L_knee_IK_ctrl
L_ankle_IK_ctrl

L_hip_FK_ctrl
L_knee_FK_ctrl
L_ankle_FK_ctrl

L_Leg_IKFKswitch_ctrl
```

### Biped Leg — Right

```text
R_hip_IK_ctrl
R_knee_IK_ctrl
R_ankle_IK_ctrl

R_hip_FK_ctrl
R_knee_FK_ctrl
R_ankle_FK_ctrl

R_Leg_IKFKswitch_ctrl
```

## Quadruped Controller Names

### Quadruped Front — Left

```text
L_humerus_IK_ctrl
L_radius_IK_ctrl
L_carpus_IK_ctrl
L_metacarpus_IK_ctrl

L_humerus_FK_ctrl
L_radius_FK_ctrl
L_carpus_FK_ctrl
L_metacarpus_FK_ctrl

L_Front_IKFKswitch_ctrl
```

### Quadruped Front — Right

```text
R_humerus_IK_ctrl
R_radius_IK_ctrl
R_carpus_IK_ctrl
R_metacarpus_IK_ctrl

R_humerus_FK_ctrl
R_radius_FK_ctrl
R_carpus_FK_ctrl
R_metacarpus_FK_ctrl

R_Front_IKFKswitch_ctrl
```

### Quadruped Rear — Left

```text
L_femur_IK_ctrl
L_tibia_IK_ctrl
L_tarsus_IK_ctrl
L_metatarsus_IK_ctrl

L_femur_FK_ctrl
L_tibia_FK_ctrl
L_tarsus_FK_ctrl
L_metatarsus_FK_ctrl

L_Rear_IKFKswitch_ctrl
```

### Quadruped Rear — Right

```text
R_femur_IK_ctrl
R_tibia_IK_ctrl
R_tarsus_IK_ctrl
R_metatarsus_IK_ctrl

R_femur_FK_ctrl
R_tibia_FK_ctrl
R_tarsus_FK_ctrl
R_metatarsus_FK_ctrl

R_Rear_IKFKswitch_ctrl
```

## FK Offset Group Naming

Each FK controller, except the root FK controller, is expected to have an offset group named:

```text
<FK_controller_name>_off
```

Example:

```text
L_elbow_FK_ctrl_off
L_wrist_FK_ctrl_off
```

The tool parents child FK offset groups under the previous FK controller to form the FK hierarchy.

## IK/FK Switch Attribute

Each IK/FK switch controller must contain this attribute:

```text
IKFKswitch
```

Requirements:

| Requirement | Value |
|---|---|
| Attribute name | `IKFKswitch` |
| Type | float or double |
| Minimum | `0` |
| Maximum | `1` |
| IK mode | `0` |
| FK mode | `1` |

Example controller:

```text
L_Arm_IKFKswitch_ctrl.IKFKswitch
```

## Generated Names

The tool creates new joints by adding suffixes to the source joint names.

### Biped

```text
<source_joint>_IK
<source_joint>_FK
```

### Quadruped

```text
<source_joint>_driver
<source_joint>_IK
<source_joint>_FK
```

The tool will stop if a generated joint name already exists.
