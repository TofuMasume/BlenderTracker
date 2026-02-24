# Pattern & Version Manager

Blender アドオン。オブジェクトの命名規則でパターンとバージョンを管理する。

---

## 命名規則

```
<BaseName>_Pt.<PtToken>_v.<VToken>
```

| トークン | 形式 | 例 |
|---|---|---|
| `BaseName` | 任意の文字列 | `Chair`, `Wall_A` |
| `PtToken` | `Base`（予約語）または 3桁ゼロ埋め整数 | `Base`, `000`, `001` |
| `VToken` | 3桁ゼロ埋め整数 | `000`, `001`, `012` |

### 例

```
Chair_Pt.Base_v.000   ← ベースパターン
Chair_Pt.000_v.000    ← パターン 0、バージョン 0
Chair_Pt.000_v.001    ← パターン 0、バージョン 1
Chair_Pt.001_v.000    ← パターン 1、バージョン 0
```

---

## 機能

### リネーム

ベース名を入力すると `_Pt.000_v.000` を自動追記する。

- 既存の管理済みサフィックスがある場合、ダイアログにはベース名のみ表示される

### ノーマルコピー

標準の複製（`bpy.ops.object.duplicate` 相当）。名前変換なし。

### パターンコピー

複製し、シーン内の同ベース名オブジェクトの Pt 番号最大値 + 1 を自動付与。バージョンは `000` にリセット。

| コピー元 | シーン内の同ベース | コピー先 |
|---|---|---|
| `Chair_Pt.Base_v.000` | 数値 Pt なし | `Chair_Pt.000_v.000` |
| `Chair_Pt.001_v.003` | 最大 Pt = 001 | `Chair_Pt.002_v.000` |
| `Chair`（管理外） | 数値 Pt なし | `Chair_Pt.000_v.000` |

---

## キーバインド（3D Viewport 内）

| ショートカット | 操作 |
|---|---|
| `Alt + F2` | リネーム |
| `Ctrl + Shift + D` | パターンコピー |

---

## UI

3D Viewport のサイドバー（`N` キー）→ **Pt/Ver** タブ

- アクティブオブジェクトの Base / Pattern / Version を表示
- リネーム・ノーマルコピー・パターンコピーボタン

---

## インストール

1. このリポジトリをダウンロードし、フォルダごと zip 化
2. Blender → `Edit > Preferences > Add-ons > Install`
3. zip ファイルを選択してインストール
4. `Pattern & Version Manager` を有効化

---

## 動作環境

- Blender 4.0 以上
