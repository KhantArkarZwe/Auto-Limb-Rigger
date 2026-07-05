# metaTools Auto Limb Rigger v0.2

二足・四足リグのIK/FKリムセットアップを自動化する、Maya Pythonツールです。

このツールは、繰り返し発生するリギング作業を減らし、リムリグ構造を一定に保ち、Maya内でIK/FKブレンドリムシステムをより早く作成するために制作しました。

## 主な機能

- 選択したバインド／ソースリムチェーンから、IK用・FK用の複製ジョイントシステムを作成します。
- 二足キャラクターの腕と脚に対応しています。
- 四足キャラクターの前脚と後脚に対応しています。
- 二足リム用のIKハンドルを作成します。
- 四足リム用に、spring、RP、SC IKハンドルを使用したIKセットアップを作成します。
- FKコントローラーをFKジョイントへ接続します。
- matrixノード、decomposeMatrixノード、pairBlendノードを使用してIK/FKブレンドセットアップを作成します。
- IK/FKスイッチ属性をIK・FKコントローラーの表示切り替えに接続します。
- リグ作成前に必要な検証を行います。

## ソフトウェア／環境

- Autodesk Maya 2025
- Python 3
- maya.cmds

## このツールが行うこと

このツールは、既存のリムジョイントチェーンと既存のコントローラーを使用し、その周囲にIK/FKリグシステムを構築します。

二足リムの場合、以下を作成します。

- IKジョイントチェーン
- FKジョイントチェーン
- IKハンドル
- FKコントローラーのコンストレイント
- IK/FKブレンド用ノード
- IK/FKコントローラーの表示切り替え

四足リムの場合、以下を作成します。

- driverジョイントチェーン
- IKジョイントチェーン
- FKジョイントチェーン
- spring solver IKハンドル
- RP solver IKハンドル
- SC solver IKハンドル
- FKコントローラーのコンストレイント
- IK/FKブレンド用ノード
- IK/FKコントローラーの表示切り替え

## このツールが行わないこと

- コントローラーは作成しません。
- 元となるバインド／ソーススケルトンは作成しません。
- キャラクターのスキニングは行いません。
- IK/FKスイッチコントローラーは作成しません。
- `IKFKswitch` 属性は追加しません。
- 1つのジョイントに複数の子ジョイントがある場合、どの分岐を使用するかを自動判定しません。
- 現時点では、生成されたリグシステムを削除するためのUndo／Cleanup専用ツールはありません。

## 使用方法

1. Mayaを開きます。
2. スクリプトをScript Editorで開く、またはMayaのPython環境へロードします。
3. 以下を実行します。

```python
metaTools_AutoLimbRigger_v02.openUI()
```

4. UIで以下を選択します。
   - Rig Type: `Biped` または `Quadruped`
   - Limb Type:
     - Biped: `Arm` または `Leg`
     - Quadruped: `Front` または `Rear`
   - Limb Side: `L` または `R`
5. リムチェーンのルートジョイントを選択します。
6. **Build Rig** を押します。

## 必要なシーンセットアップ

ツールを実行する前に、シーン内に以下が既に存在している必要があります。

- クリーンなソース／バインド用リムジョイントチェーン
- 想定された名前のIKコントローラー
- 想定された名前のFKコントローラー
- `_off` サフィックス付きのFKコントローラー用オフセットグループ
- IK/FKスイッチコントローラー
- スイッチコントローラー上の数値属性 `IKFKswitch`

`IKFKswitch` 属性は以下を満たす必要があります。

- 属性名は正確に `IKFKswitch` であること
- `L_Arm_IKFKswitch_ctrl` のような名前のコントローラー上に存在すること
- floatまたはdouble属性であること
- 値の範囲が `0` から `1` であること

現在のスイッチの意味は以下です。

| Value | Mode |
|---:|---|
| `0` | IK |
| `1` | FK |

## 対応リムタイプ

| Rig Type | Limb Type | Source Chain Length | Blend Joint Count |
|---|---|---:|---:|
| Biped | Arm | 3 | 3 |
| Biped | Leg | 5 | 3 |
| Quadruped | Front | 5 | 4 |
| Quadruped | Rear | 5 | 4 |

二足脚では、IKハンドル作成のために足・つま先を含む5つのソースジョイントを読み込みますが、IK/FKシステムでブレンドされるのは主要な3ジョイントのみです。

## 生成されるジョイントシステム

### Biped

ツールは以下を作成します。

```text
source_joint_IK
source_joint_FK
```

例:

```text
L_shoulder
L_shoulder_IK
L_shoulder_FK
```

### Quadruped

ツールは以下を作成します。

```text
source_joint_driver
source_joint_IK
source_joint_FK
```

例:

```text
L_humerus
L_humerus_driver
L_humerus_IK
L_humerus_FK
```

## IK/FKブレンド方式

ブレンド対象の各バインド／ソースジョイントに対して、ツールは以下を作成します。

- `sourceJoint_IKFK_off` という名前のオフセットグループ
- IK用 `multMatrix`
- IK用 `decomposeMatrix`
- FK用 `multMatrix`
- FK用 `decomposeMatrix`
- `pairBlend` ノード

IKジョイントとFKジョイントのトランスフォームは、ブレンド用オフセットグループのローカル空間へ変換されます。そのtranslateとrotate出力を `pairBlend` ノードでブレンドします。ブレンド用オフセットグループはparentConstraintを通して元のソース／バインドジョイントを駆動します。

`pairBlend.rotInterpolation` はクォータニオンモードに設定されます。

## 重要な前提条件

- 選択したルートジョイントは、UIで選択したsideとlimb typeに一致している必要があります。
- 左側の名前は `L_` で始まる必要があります。
- 右側の名前は `R_` で始まる必要があります。
- 二足腕のルートは `_shoulder` で終わる必要があります。
- 二足脚のルートは `_hip` で終わる必要があります。
- 四足前脚のルートは `_humerus` で終わる必要があります。
- 四足後脚のルートは `_femur` で終わる必要があります。
- 既存のコントローラーはジョイントに合わせて配置されている必要があります。
- FKコントローラーのオフセットグループは `_off` サフィックスを使用する必要があります。
- 生成されるノード名は、シーン内に既に存在していてはいけません。
- 1つのジョイントに複数の子がある場合、最初の子ジョイントを使用します。

## 現在の制限事項

- `maya.cmds` のみで構築されています。
- 現在のツールは厳密な命名規則を前提としています。
- コントローラーはツール実行前に既に存在している必要があります。
- FKコンストレイントでは `maintainOffset=False` を使用するため、FKコントローラーのアライメント問題は意図的に露出します。
- 分岐のあるジョイントチェーンは、まだインタラクティブに選択できません。ツールは警告を出し、最初の子を使用します。
- 同名の生成済みジョイントまたはノードが既に存在する場合、ビルドは停止します。
- コードは現在、主に1つのスクリプトファイル内に保存されています。
- ビルドが途中で失敗した場合の自動ロールバックはありません。
- 生成済みリムリグを削除または再構築するための専用UIはまだありません。

## Author

KhantArkarZwe — Rigging / Technical Artist\
Gmail: khantarkarzwe@gmail.com
