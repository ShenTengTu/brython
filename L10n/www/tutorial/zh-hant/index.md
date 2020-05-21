本教學講解了如何使用Python程式語言開發在瀏覽器中運行的應用程式。 我們將以編寫一個計算機為例。

您將需要一個文本編輯器，當然還需要一個可以訪問網際網路的瀏覽器。

本教學的內容假定了您至少具有HTML（通用的頁面結構，最常用的標籤），樣式表（CSS）和Python語言的基本知識。

在文本編輯器中，創建一個包含以下內容的HTML頁面：

```xml
<!doctype html>
<html>

<head>
    <meta charset="utf-8">
    <script type="text/javascript"
        src="https://cdn.jsdelivr.net/npm/brython@{implementation}/brython.min.js">
    </script>
</head>

<body onload="brython()">

<script type="text/python">
from browser import document

document <= "Hello !"
</script>


</body>

</html>
```

在一個空目錄中，將此頁面另存為 __`index.html`__。要在瀏覽器中閱覽它，您有兩種選擇：

- 使用“檔案/開啟”選單：這是最簡單的解決方案。 它為進階運用帶來了[一些限制](/static_doc/zh-hant/file_or_http.html)，但它在本教學中完美地運作。
- 啟動一個網路伺服器： 舉例來說, 如果您的機器上有python.org提供的Python直釋器，則在檔案目錄中運行`python -m http.server`，然後在瀏覽器網址列中輸入_localhost:8000/index.html_ 。

當打開頁面時，您應該會看到訊息 “Hello !”打印在瀏覽器視窗上。

頁面結構
=======
讓我們看一下頁面內容。在`<head>`區域，我們載入腳本__`brython.js`__： 它是Brython引擎，該程式將查找並執行頁面中包含的Python腳本。在此範例中，我們從CDN獲得它，因此無需在PC上安裝任何軟體。注意版本號碼 (`brython@{implementation}`) ： 它可以被更新為每個新的Brython版本。

標籤`<body>` 具有一個屬性 `onload="brython()"`。 這意味著當頁面載入完成後，瀏覽器必須調用函式`brython()`，該函式在已載入至頁面的Brython引擎中定義。該函式搜尋所有具有屬性`type="text/python"`的`<script>`標籤並執行它們。

我們的 __`index.html`__ 頁面嵌入了以下腳本：

```python
from browser import document

document <= "Hello !"
```

這是一個標準的Python程式，從導入模組開始，__`browser`__ （在這種情況下，Brython引擎__`brython.js`__附帶了一個模組） 該模組具有`document`屬性，該屬性參照瀏覽器視窗中顯示的內容。

要將文本添加到`document`中－具體來說是在瀏覽器中顯示文本－Brython使用的語法是

```python
document <= "Hello !"
```

您可以將`<=`視為左箭頭：`document` “接收”一個新元素，此處為字符串“ Hello！”。 稍後您將會看到，總是可以使用標準化的DOM語法來與頁面進行交互，Brython提供了一些捷徑來使代碼不再那麼冗長。

使用HTML標籤的文本格式化
======================
HTML標籤允許文本格式化，例如以粗體字母（`<B>`標籤），斜體（`<I>`）等書寫。

對於Brython，這些標籤可用作 __`browser`__ 套件的 __`html`__ 模組中定義的函式。使用方法如下：

```python
from browser import document, html

document <= html.B("Hello !")
```

標籤可以被嵌套：

```python
document <= html.B(html.I("Hello !"))
```

標籤也可以彼此添加，以及字符串：

```python
document <= html.B("Hello, ") + "world !"
```

標籤函式的第一個參數可以是字符串，數字，另一個標籤。它也可以是Python的“iterable” （list、comprehension、generator）：在這種情況下，將在迭代中生成的所有元素被添加到標籤中：

```python
document <= html.UL(html.LI(i) for i in range(5))
```

標籤屬性作為關鍵字參數傳遞給函式：

```python
html.A("Brython", href="http://brython.info")
```

繪製計算機
=========
我們可以將計算機繪製為HTML表格。

第一行由結果區域組成，其次是一個重置按鈕。 接下來的3行是計算機的觸鍵，數字和運算符。

```python
from browser import document, html

calc = html.TABLE()
calc <= html.TR(html.TH(html.DIV("0", id="result"), colspan=3) +
                html.TH("C", id="clear"))
lines = ["789/",
         "456*",
         "123-",
         "0.=+"]

calc <= (html.TR(html.TD(x) for x in line) for line in lines)

document <= calc
```

請注意使用Python生成器來減小程式大小，同時保持可讀性。

讓我們在樣式表中將樣式添加到`<TD>`標籤，以使計算機看起來更好：

```xml
<style>
*{
    font-family: sans-serif;
    font-weight: normal;
    font-size: 1.1em;
}
td{
    background-color: #ccc;
    padding: 10px 30px 10px 30px;
    border-radius: 0.2em;
    text-align: center;
    cursor: default;
}
#result{
    border-color: #000;
    border-width: 1px;
    border-style: solid;
    padding: 10px 30px 10px 30px;
    text-align: right;
}
</style>
```

事件處理
=======
下一步是當使用者按下計算機觸鍵時觸發動作：

- 對於數字和運算符：在結果區域中打印數字或運算。
- 對於`=`符號：執行運算並打印結果，如果輸入無效，則顯示錯誤訊息。
- 對於`C`字母：重置結果區域。

要處理打印在頁面中的元素，程式首先需要獲得對它們的參照。 按鈕已被創建為`<TD>`標籤； 為了獲得所有這些標籤的引用，語法是

```python
document.select("td")
```
傳遞給`select()`方法的參數是一個 _CSS選擇器_ 。 最常用的是：標籤名稱（“ td”），元素的`id`屬性（“ #result”）或其屬性“ class”（“ .classname”）。`select()` 的輸出結果始終是元素列表。

頁面元素上可能發生的事件具有標準化名稱：當用戶單擊按鈕時，將觸發名為“click”的事件。在程式中，此事件會觸發函式的執行。 元素，事件和函式的之間的關聯由語法定義。

```python
element.bind("click", action)
```

對於計算機，我們可以通過以下方式將相同的函式與所有按鈕上的“ click”事件相關聯：

```python
for button in document.select("td"):
    button.bind("click", action)
```

為了符合Python語法，必須在程式之前的某個位置定義`action()` 函式。 這樣的“回調”函式採用單個參數，即一個表示事件的物件。

完成程式
=======
這是管理最小版本計算器的代碼。最重要的部分是`action(event)`函式。 

```python
from browser import document, html

# Construction de la calculatrice
calc = html.TABLE()
calc <= html.TR(html.TH(html.DIV("0", id="result"), colspan=3) +
                html.TD("C"))
lines = ["789/", "456*", "123-", "0.=+"]

calc <= (html.TR(html.TD(x) for x in line) for line in lines)

document <= calc

result = document["result"] # direct acces to an element by its id

def action(event):
    """Handles the "click" event on a button of the calculator."""
    # The element the user clicked on is the attribute "target" of the
    # event object
    element = event.target
    # The text printed on the button is the element's "text" attribute
    value = element.text
    if value not in "=C":
        # update the result zone
        if result.text in ["0", "error"]:
            result.text = value
        else:
            result.text = result.text + value
    elif value == "C":
        # reset
        result.text = "0"
    elif value == "=":
        # execute the formula in result zone
        try:
            result.text = eval(result.text)
        except:
            result.text = "error"

# Associate function action() to the event "click" on all buttons
for button in document.select("td"):
    button.bind("click", action)
```

結果
====
<iframe width="800", height="400" src="/gallery/calculator.html"></iframe>
