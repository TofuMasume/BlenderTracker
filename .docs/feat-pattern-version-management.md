# feat: Pattern & Version Management Addon

作成日: 2026-02-24

---

## 概要

Blender オブジェクト/コレクションに対して、パターンとバージョンを命名規則で管理するアドオン。

---

## 命名規則

### フォーマット

```
<BaseName>_Pt.<PtToken>_v.<VToken>
```

| トークン | 形式 | 例 |
|---|---|---|
| `BaseName` | 任意の文字列 | `Chair`, `Wall_A` |
| `PtToken` | `Base` または 3桁ゼロ埋め整数 | `Base`, `000`, `001` |
| `VToken` | 3桁ゼロ埋め整数 | `000`, `001`, `012` |

### 例

```
Chair_Pt.Base_v.000   ← ベースパターン（予約語）
Chair_Pt.000_v.000    ← パターン0, バージョン0
Chair_Pt.000_v.001    ← パターン0, バージョン1
Chair_Pt.001_v.000    ← パターン1, バージョン0
```

### 予約語

- `Pt.Base`: ベースパターン専用。数値として扱わない。
  - コピーや比較では数値 Pt とは別扱い。

---

## 機能仕様

### 1. Alt+F2 リネーム

- 対象: アクティブオブジェクト
- 動作:
  1. ダイアログを表示（ベース名のみ入力、既存サフィックスは除去して表示）
  2. 確定時に `_Pt.000_v.000` を自動追記
- 既存管理名がある場合: サフィックスを除いたベース名をダイアログに表示

### 2. ノーマルコピー

- `bpy.ops.object.duplicate(linked=False)` と同等
- 名前変換なし（Blender のデフォルト命名に従う）

### 3. パターンコピー

- 対象: アクティブオブジェクト
- 動作:
  1. コピー元のベース名を特定
  2. シーン内の同ベース名オブジェクトの Pt 番号最大値を取得
  3. `next_pt = max(max_pt + 1, 1)` で次の番号を決定
  4. 複製し `<BaseName>_Pt.<next_pt>_v.000` を付与

#### 管理外オブジェクトのコピー時

- フルオブジェクト名をベース名として使用
- コピー結果は `<FullName>_Pt.001_v.000` になる（シーンに管理済みオブジェクトがない場合）

---

## モジュール構成

```
managemant_PatternVersion/
  __init__.py    # bl_info, register/unregister
  naming.py      # 命名ユーティリティ（bpy 依存なし）
  operators.py   # Operator クラス群
  panels.py      # N パネル
  keymaps.py     # キーバインド管理
```

### `naming.py` API

| 関数 | シグネチャ | 説明 |
|---|---|---|
| `parse_name` | `(str) -> ParsedName \| None` | 名前をパース |
| `build_name` | `(str, str, str) -> str` | 名前を構築 |
| `build_name_from_int` | `(str, int, int) -> str` | 整数から名前を構築 |
| `strip_suffix` | `(str) -> str` | ベース名を返す |
| `max_pt_number_for_base` | `(str, iterable) -> int` | 最大 Pt 番号を返す（-1 if none） |

---

## 設計上の決定事項

- `Pt.Base` から `Pt.000` へのコピー: `max_pt_number_for_base` は Base トークンを無視するため、数値最大値のみを返す。`Pt.Base_v.000` のみ存在する場合は `-1` → next_pt = 1 となり `Pt.001_v.000` が生成される。

- ベース名の非貪欲マッチ: 正規表現 `.+?` を使用し、アンダースコアを含むベース名も正しくパースする。`_Pt.` の直前までがベース名。

- 複製タイミングとスキャン順序: パターンコピーでは `bpy.ops.object.duplicate` 呼び出し前にシーンスキャンを行い、新オブジェクトがスキャン結果に混入しないようにする。

---

## 今後の拡張候補

- コレクションへの対応
- バージョンインクリメントコピー（Pt 固定、v+1）
- 管理済みオブジェクト一覧パネル
- 名前バリデーション（重複チェック等）
