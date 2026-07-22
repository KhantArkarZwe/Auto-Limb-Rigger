# Naming Convention — metaTools Auto Limb Rigger v0.2

このドキュメントでは、Auto Limb Riggerで想定している命名規則を説明します。

このツールは、リグ作成前にジョイント、コントローラー、スイッチ属性を確認するため、厳密なオブジェクト名に依存しています。

## Side Prefix

全てのリムルートとコントローラーは、以下のいずれかのside prefixで始まる必要があります。

| Side | Prefix |
|---|---|
| Left | `L_` |
| Right | `R_` |

例:

```text
L_shoulder
R_hip
L_wrist_IK_ctrl
R_knee_FK_ctrl
```

## Biped Source Joint Naming

### Biped Arm

選択するルートジョイントは、以下で終わる必要があります。

```text
_shoulder
```

想定チェーン:

```text
L_shoulder
└── L_elbow
    └── L_wrist
```

右側:

```text
R_shoulder
└── R_elbow
    └── R_wrist
```

### Biped Leg

選択するルートジョイントは、以下で終わる必要があります。

```text
_hip
```

想定ソースチェーン:

```text
L_hip
└── L_knee
    └── L_ankle
        └── L_foot
            └── L_tiptoe
```

右側:

```text
R_hip
└── R_knee
    └── R_ankle
        └── R_foot
            └── R_tiptoe
```

## Quadruped Source Joint Naming

### Quadruped Front Limb

選択するルートジョイントは、以下で終わる必要があります。

```text
_humerus
```

想定チェーン:

```text
L_humerus
└── L_radius
    └── L_carpus
        └── L_metacarpus
            └── L_phalanges
```

右側:

```text
R_humerus
└── R_radius
    └── R_carpus
        └── R_metacarpus
            └── R_phalanges
```

### Quadruped Rear Limb

選択するルートジョイントは、以下で終わる必要があります。

```text
_femur
```

想定チェーン:

```text
L_femur
└── L_tibia
    └── L_tarsus
        └── L_metatarsus
            └── L_phalanges
```

右側:

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

ルートFKコントローラーを除き、各FKコントローラーには以下の名前のオフセットグループが必要です。

```text
<FK_controller_name>_off
```

例:

```text
L_elbow_FK_ctrl_off
L_wrist_FK_ctrl_off
```

ツールは、子FKオフセットグループを前のFKコントローラーの下にペアレントし、FK階層を形成します。

## IK/FK Switch Attribute

各IK/FKスイッチコントローラーには、以下の属性が必要です。

```text
IKFKswitch
```

要件:

| Requirement | Value |
|---|---|
| Attribute name | `IKFKswitch` |
| Type | float or double |
| Minimum | `0` |
| Maximum | `1` |
| IK mode | `0` |
| FK mode | `1` |

コントローラー例:

```text
L_Arm_IKFKswitch_ctrl.IKFKswitch
```

## Generated Names

ツールは、ソースジョイント名にサフィックスを追加して新しいジョイントを作成します。

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

生成されるジョイント名が既に存在する場合、ツールは停止します。
