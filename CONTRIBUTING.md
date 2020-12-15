# 貢獻指南
> 如果您想為Brython做貢獻，請閱讀原始專案的[貢獻指南](https://github.com/brython-dev/brython/blob/master/CONTRIBUTING.md)。

這個分叉專案主要致力於[Brython]文檔的中文翻譯。[原作者希望核心的Brython項目僅保有法語，英語和西班牙語](https://github.com/brython-dev/brython/pull/1380#issuecomment-623877881)，所以中文文檔採用分叉專案進行開發但不合併到原始專案。

希望參與翻譯的貢獻者能保持追踪原始專案的動態。

## 分支架構
`up-mirror`: Brython原始專案`master`分支的鏡像
`master`:本分叉專案主分支
`develop`: 本分叉專案主開發分支
`l10n-zh-hant`: 本分叉專案繁體中文文檔開發分支

## 存儲庫佈局
除了下列描述的資料夾及檔案，基本上目錄架構與Brython原始專案相似：
- `L10n`: 翻譯工作區資料夾
  - `tools`: 翻譯工作輔助腳本資料夾
  - `www`: 翻譯原始文檔及網頁原始碼資料夾，與原始專案的`www`相似
  - `.editorconfig`
- `docs`: GitHub Page發布源資料夾

## 代碼格式
有一些約定如下。

### 編輯器
使用“[EditorConfig]”保持一致，規則在`.editorconfig`中聲明。在編寫腳本之前，需要配置編輯器以使EditorConfig起作用。

[EditorConfig]: https://editorconfig.org/

### Python
遵循“[Black]”樣式和`pyproject.toml`中的選項以保持代碼格式一致。在發出拉取請求之前，請執行`black`格式化代碼。

[Black]: https://black.readthedocs.io/en/stable/

## 入門
- 在GitHub上分叉這個專案的存儲庫。 使用git克隆您分叉的存儲庫。
- 強烈建議使用`pipenv`創建虛擬環境來安裝開發需求：
```console
$ pipenv install --dev
```

將開發需求安裝到單獨的虛擬環境中，您可以通過運行以下命令終端激活虛擬環境：
```console
$ pipenv shell
```

## 做出更動
基本上工作區域會在`L10n`資料夾及`docs`資料夾。

從您想作為工作基礎的位置創建一個主題分支，建議以`develop`分支為基礎創建主題分支：
```console
$ git checkout -b topic-branch develop
```

-  依照原始專案的文檔(`*.md`)進行翻譯。
-  在遵循原始專案的風格的前提下調整網頁架構。

## 開發工具`L10n.tools`
- 生成文檔網頁：
```console
python -m L10n.tools.mk_doc
```

- 生成stdlib列表：
```console
python -m L10n.tools.mk_stdlib_list
```

- 將需要的原始專案的源代碼(`www/src`)複製到(`L10n/www/src`)：
```
python -m L10n.tools.src_copy
```

- 將需要的原始專案的HTML檔案(`www/*`)複製到(`L10n/www/*`)：
```
python -m L10n.tools.html_copy
```

## 預覽文檔網頁
1. 使用Python建立的Server。要看見變動，需使用瀏覽器的刊發人員工具將storage及cache並重載頁面。
```
$ python -m L10n.tools.server
```
2. 如果使用`VS Code`，可以使用具有實時瀏覽器重新加載功能的[Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)延伸模組。

