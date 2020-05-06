
> 這個分叉專案主要致力於[Brython]文檔的中文翻譯。歡迎對Brython及文檔翻譯有興趣的貢獻者參與。
>
> [原作者希望核心的Brython項目僅保有法語，英語和西班牙語](https://github.com/brython-dev/brython/pull/1380#issuecomment-623877881)，所以中文文檔採用分叉專案進行開發但不合併到原始專案。
>
> 歡迎對Brython及文檔翻譯有興趣的貢獻者參與。
>
> 如果您想為Brython中文文檔做貢獻，請先閱讀本專案的[貢獻指南](https://github.com/ShenTengTu/brython/blob/master/CONTRIBUTING.md)。


# Brython

**[Brython]（Browser Python）** 是在瀏覽器中運行的Python 3的實現，具有與DOM元素和事件的介面。

這是運行Python的HTML簡單範例：

```xml
    <html>

        <head>
            <script type="text/javascript" src="/path/to/brython.js"></script>
        </head>

        <body onload="brython()">

            <script type="text/python">
            from browser import document, alert

            def echo(event):
                alert(document["zone"].value)

            document["mybutton"].bind("click", echo)
            </script>

            <input id="zone"><button id="mybutton">click !</button>

        </body>

    </html>
```

要使用[Brython]，要做的就是：
1. 載入JavaScript腳本[brython.js](http://brython.info/src/brython.js "Brython from the site brython.info")
2. 在頁面載入時運行`brython()`，例如`<body onload="brython”>`。
3. 在`<script type="text/python">`內編寫Python代碼。

# 文檔
- [English](http://brython.info/static_doc/en/intro.html)
- [French](http://brython.info/static_doc/fr/intro.html)
- [Spanish](http://brython.info/static_doc/es/intro.html)
- [繁體中文]

社群貢獻
========
**Brython**
- 回報Brython錯誤/問題，或者建議新功能，請到原始專案的[Issues頁面](https://github.com/brython-dev/brython/issues)。
- 如果您想為Brython做貢獻，請先閱讀原始專案的[貢獻指南](https://github.com/brython-dev/brython/blob/master/CONTRIBUTING.md)。
- [brython - Google網上論壇](https://groups.google.com/forum/?fromgroups=#!forum/brython)


**中文文檔**
- 回報中文文檔的錯誤/問題，或者建議，請到本專案的[Issues頁面](https://github.com/ShenTengTu/brython/issues)。
- 如果您想為Brython中文文檔做貢獻，請先閱讀本專案的[貢獻指南](https://github.com/ShenTengTu/brython/blob/master/CONTRIBUTING.md)。



[Brython]: https://github.com/brython-dev/brython
