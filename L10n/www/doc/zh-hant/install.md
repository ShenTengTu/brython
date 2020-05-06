首次安裝
--------

安裝 Brython：
- 如果您的電腦有CPython和pip，經由下方指令安裝套件`brython`：
```console
pip install brython
```

> 然後在一個空目錄下運行
>```console
>brython-cli --install
>```

- 如果無法使用此方法，請前往Github的[發行版本頁面](https://github.com/brython-dev/brython/releases)，選擇最新版本，下載並解壓縮 __Brython-x.y.z.zip__.

在這兩種情況下，目錄都有以下檔案：

- __brython.js__ : Brython引擎，需在HTML頁面中引用。
- __brython_stdlib.js__ : 集合了Brython支援的部分Python標準庫的所有模組和套件。
- __demo.html__ : 包含一些如何使用Brython進行客戶端開發範例的頁面。

__brython.js__ 包含非常常用的模組： `browser, browser.html, javascript`.

如果您的應用程序使用標準分發的模組，除 __brython.js__ 之外則需要引用 __brython_stdlib.js__ ：

```xml
<script type="text/javascript" src="brython.js"></script>
<script type="text/javascript" src="brython_stdlib.js"></script>
```

更新
----
當發布新版本的Brython時，可以經由常用命令完成更新：
```console
pip install brython --upgrade
```

然後在應用程序目錄中, 您可以經由下方指令更新Brython檔案
(__brython.js__ 及 __brython_stdlib.js__)：

```console
brython-cli --update
```

安裝CPython套件
---------------
由`pip`安裝的CPython套件可以經由命令`--add_package <package name>`安裝到Brython應用程序中。例如：
```console
pip install attrs
brython-cli --add_package attrs
```

套件中的所有檔案當然必須可供Brython使用；例如，這不包括用C編寫的檔案。

其他命令
--------

`-- modules`

> 創建特定於應用程序的分發，以較小的檔案替換 __`brython_stdlib.js`__ 。
> 參見“[import實現](import.html)”章節。

`-- make_dist`

> 生成適用於PyPI分發的CPython套件，以安裝Brython應用程序。
> 參見“[部署Brython應用程序](deploy.html)”章節。

`-- make_package`

> 生成“ Brython套件”, 允許以非常直接的方式分發模組或套件。
> 參見“[包裝Brython](brython-packages.html)”章節。

網路伺服器
---------
可以在瀏覽器中打開HTML檔案，但是建議在應用程序目錄中啟動Web服務器。

最簡單的方法是在CPython標準分發中使用 **http.server** 模組：

```console
python -m http.server
```

默認連接埠是8000。要選擇另一個連接埠：
```console
python -m http.server 8001
```

然後，您可以經由在瀏覽器地址欄中輸入 _http://localhost:8001/demo.html_ 來訪問頁面。
