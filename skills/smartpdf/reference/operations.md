# Операции SmartPDF — параметры

Файл собирается из описания API (`operations.json` портала) — не правьте вручную. Скрипту параметры передаются как
`-p имя=значение` (массивы и числа — JSON), REST — полями JSON рядом с `file_id` (`file_ids` у объединения и JPG в
PDF), MCP — аргументами инструмента рядом с `file_url` (`file_urls`). Цена запроса — за каждую начатую единицу
(10 МБ входа или N страниц — берётся большее), сумма — на https://dev.smartpdf.ru/docs/billing.

## В PDF

### Word в PDF — `word-to-pdf`

Конвертирует документ Word в PDF: шрифты, таблицы и кириллица сохраняются.

- REST: `POST https://api.smartpdf.ru/v1/pdf/word-to-pdf` · MCP: `word_to_pdf`
- Вход: DOC, DOCX → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py word-to-pdf document.docx
```

### JPG в PDF — `jpg-to-pdf`

Собирает PDF из изображений: каждое — отдельная страница.

- REST: `POST https://api.smartpdf.ru/v1/pdf/jpg-to-pdf` · MCP: `jpg_to_pdf`
- Вход: JPG, PNG, WEBP — от 1 до 10 файлов → результат: PDF
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `order` | `integer[]` | Порядок страниц — индексы file_ids от 0, каждый ровно один раз. Без него — порядок file_ids. |
| `fit` | `string` | auto — страница по размеру изображения; portrait и landscape — лист A4 с полями в выбранной ориентации. Значения: `"auto"`, `"portrait"`, `"landscape"`. По умолчанию: `"auto"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py jpg-to-pdf scan-1.jpg scan-2.jpg -p fit=portrait
```

### Excel в PDF — `xlsx-to-pdf`

Конвертирует таблицу Excel в PDF. Листы, область и масштаб берутся из параметров печати файла.

- REST: `POST https://api.smartpdf.ru/v1/pdf/xlsx-to-pdf` · MCP: `xlsx_to_pdf`
- Вход: XLS, XLSX → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py xlsx-to-pdf table.xlsx
```

### PowerPoint в PDF — `pptx-to-pdf`

Конвертирует презентацию PowerPoint в PDF: слайд — страница.

- REST: `POST https://api.smartpdf.ru/v1/pdf/pptx-to-pdf` · MCP: `pptx_to_pdf`
- Вход: PPT, PPTX → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pptx-to-pdf slides.pptx
```

### HTML в PDF — `html-to-pdf`

Превращает HTML-файл в PDF. Внешние ресурсы не загружаются: картинки и шрифты — только встроенные (data:), стили — в самом файле.

- REST: `POST https://api.smartpdf.ru/v1/pdf/html-to-pdf` · MCP: `html_to_pdf`
- Вход: HTML → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `page_size` | `string` | Формат страницы. Значения: `"A4"`, `"A3"`, `"Letter"`. По умолчанию: `"A4"`. |
| `orientation` | `string` | Ориентация страницы. Значения: `"portrait"`, `"landscape"`. По умолчанию: `"portrait"`. |
| `margin` | `string` | Поля страницы. Значения: `"standard"`, `"narrow"`, `"none"`. По умолчанию: `"standard"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py html-to-pdf page.html -p page_size=A4 -p orientation=portrait
```

## Из PDF

### PDF в Word — `pdf-to-word`

Конвертирует PDF в редактируемый документ Word. Сканы без текстового слоя сначала распознайте (OCR).

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-word` · MCP: `pdf_to_word`
- Вход: PDF → результат: DOCX
- Единица цены: 10 МБ или 50 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-word document.pdf
```

### PDF в JPG — `pdf-to-jpg`

Сохраняет страницы PDF картинками JPG. Результат — ZIP-архив: page-1.jpg, page-2.jpg…

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-jpg` · MCP: `pdf_to_jpg`
- Вход: PDF → результат: ZIP с JPG
- Единица цены: 10 МБ или 50 стр. (300 dpi — 25)

| Параметр | Тип | Описание |
|---|---|---|
| `dpi` | `integer` | Разрешение. В 300 dpi единица цены — каждые 25 страниц. Значения: `72`, `150`, `300`. По умолчанию: `150`. |
| `pages` | `integer[]` | Номера страниц с 1. Без параметра — все страницы; оплачиваются только выбранные. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-jpg document.pdf -p dpi=150
```

### PDF в Excel — `pdf-to-excel`

Извлекает таблицы из PDF в Excel.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-excel` · MCP: `pdf_to_excel`
- Вход: PDF → результат: XLSX
- Единица цены: 10 МБ или 50 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `layout` | `string` | per-table — каждая таблица на своём листе; single-sheet — все таблицы на одном листе подряд. Значения: `"per-table"`, `"single-sheet"`. По умолчанию: `"per-table"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-excel document.pdf -p layout=per-table
```

### PDF в PowerPoint — `pdf-to-pptx`

Конвертирует PDF в презентацию PowerPoint: каждая страница — отдельный слайд.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-pptx` · MCP: `pdf_to_pptx`
- Вход: PDF → результат: PPTX
- Единица цены: 10 МБ или 50 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-pptx document.pdf
```

### PDF в текст — `pdf-to-txt`

Извлекает текст из PDF в файл TXT (UTF-8).

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-txt` · MCP: `pdf_to_txt`
- Вход: PDF → результат: TXT
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `mode` | `string` | text — простой текст постранично; blocks — по абзацам и колонкам; words — каждое слово с координатами. Значения: `"text"`, `"blocks"`, `"words"`. По умолчанию: `"text"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-txt document.pdf -p mode=text
```

## Управление

### Сжать PDF — `compress`

Уменьшает размер PDF. Результат никогда не больше исходного файла.

- REST: `POST https://api.smartpdf.ru/v1/pdf/compress` · MCP: `compress_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `level` | `string` | low — без потерь качества; medium — изображения 150 dpi; high — 100 dpi, наибольшее сжатие. Значения: `"low"`, `"medium"`, `"high"`. По умолчанию: `"medium"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py compress document.pdf -p level=medium
```

### Объединить PDF — `merge`

Объединяет несколько PDF в один. Цена — по суммарному размеру файлов.

- REST: `POST https://api.smartpdf.ru/v1/pdf/merge` · MCP: `merge_pdfs`
- Вход: PDF — от 2 файлов (до 10 на бесплатном тарифе, 20 на Про, 50 на Бизнесе) → результат: PDF
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `order` | `integer[]` | Порядок файлов — индексы file_ids от 0, каждый ровно один раз. Без него — порядок file_ids. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py merge part-1.pdf part-2.pdf
```

### Разделить PDF — `split`

Разделяет PDF на части. Результат — ZIP-архив с PDF-файлами.

- REST: `POST https://api.smartpdf.ru/v1/pdf/split` · MCP: `split_pdf`
- Вход: PDF → результат: ZIP с PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `mode` | `string` | every-page — по одной странице; ranges — по диапазонам; half — на две половины. Значения: `"every-page"`, `"ranges"`, `"half"`. По умолчанию: `"every-page"`. |
| `ranges` | `[integer, integer][]` | Диапазоны страниц с 1, включительно: [[1, 3], [5, 5]]. Обязателен при mode = ranges. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py split document.pdf -p mode=ranges -p 'ranges=[[1,3],[4,6]]'
```

### Распознать текст — `ocr`

Распознаёт текст в сканах и добавляет невидимый текстовый слой: PDF можно искать и копировать. До 100 страниц за раз.

- REST: `POST https://api.smartpdf.ru/v1/pdf/ocr` · MCP: `ocr_pdf`
- Вход: PDF до 100 страниц → результат: PDF
- Единица цены: 10 МБ или 10 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `languages` | `string[]` | Языки документа: от 1 до 4. Значения: `"rus"`, `"eng"`, `"deu"`, `"fra"`. По умолчанию: `["rus","eng"]`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py ocr document.pdf -p 'languages=["rus","eng"]'
```

### Сгладить PDF — `flatten`

Впечатывает поля форм и пометки в страницы: документ выглядит так же, но его нельзя отредактировать.

- REST: `POST https://api.smartpdf.ru/v1/pdf/flatten` · MCP: `flatten_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py flatten document.pdf
```

## Страницы

### Удалить страницы — `delete-pages`

Удаляет страницы из PDF — полностью, вместе с их содержимым.

- REST: `POST https://api.smartpdf.ru/v1/pdf/delete-pages` · MCP: `delete_pages`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `pages` (обязательный) | `integer[]` | Номера страниц с 1. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py delete-pages document.pdf -p 'pages=[2,3]'
```

### Извлечь страницы — `extract-pages`

Сохраняет выбранные страницы в новый PDF в указанном порядке.

- REST: `POST https://api.smartpdf.ru/v1/pdf/extract-pages` · MCP: `extract_pages`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `pages` (обязательный) | `integer[]` | Номера страниц с 1 — в нужном порядке. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py extract-pages document.pdf -p 'pages=[1,4,5]'
```

### Повернуть страницы — `rotate`

Поворачивает страницы PDF.

- REST: `POST https://api.smartpdf.ru/v1/pdf/rotate` · MCP: `rotate_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `pages` | `integer[] \| "all"` | Номера страниц с 1 или "all" — все страницы. По умолчанию: `"all"`. |
| `angle` | `integer` | Угол поворота по часовой стрелке. Значения: `90`, `180`, `270`. По умолчанию: `90`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py rotate document.pdf -p pages=all -p angle=90
```

### Порядок страниц — `reorder-pages`

Меняет порядок страниц. Неуказанные страницы добавляются в конец в исходном порядке.

- REST: `POST https://api.smartpdf.ru/v1/pdf/reorder-pages` · MCP: `reorder_pages`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `new_order` (обязательный) | `integer[]` | Номера страниц с 1 в новом порядке: [3, 1, 2]. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py reorder-pages document.pdf -p 'new_order=[3,1,2]'
```

### Нумерация страниц — `add-page-numbers`

Добавляет номера страниц.

- REST: `POST https://api.smartpdf.ru/v1/pdf/add-page-numbers` · MCP: `add_page_numbers`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `position` | `string` | Где ставить номер. Значения: `"bottom-center"`, `"bottom-right"`, `"top-center"`, `"top-right"`. По умолчанию: `"bottom-center"`. |
| `start_from` | `integer` | С какого числа начинать нумерацию, от 1. По умолчанию: `1`. |
| `prefix` | `string` | Текст перед номером, например "Стр. ". По умолчанию: `""`. |
| `font_size` | `integer` | Размер шрифта: от 6 до 72. По умолчанию: `12`. |
| `pages` | `integer[] \| "all"` | Какие страницы нумеровать: номера с 1 или "all". По умолчанию: `"all"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py add-page-numbers document.pdf -p position=bottom-right -p 'prefix=Стр. '
```

## Подпись и защита

### Подписать PDF — `sign`

Ставит на страницу визуальную подпись — текст или изображение. Это не электронная подпись (ЭП).

- REST: `POST https://api.smartpdf.ru/v1/pdf/sign` · MCP: `sign_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `signature_data` (обязательный) | `string` | Текст подписи или изображение data:image/png\|jpeg\|webp;base64,… до 2 МБ. |
| `page` | `integer` | Номер страницы с 1. По умолчанию: `1`. |
| `x` | `number` | Левый край блока — доля ширины страницы от левого края: от 0 до 1. По умолчанию: `0.1`. |
| `y` | `number` | Верхний край блока — доля высоты страницы от верхнего края: от 0 до 1. По умолчанию: `0.85`. |
| `width` | `number` | Ширина блока — доля ширины страницы: больше 0, до 1. По умолчанию: `0.2`. |
| `height` | `number` | Высота блока — доля высоты страницы: больше 0, до 1. По умолчанию: `0.05`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py sign document.pdf -p 'signature_data=Иванов И. И.' -p page=1 -p x=0.6 -p y=0.85
```

### Защитить паролем — `protect`

Ставит пароль на открытие PDF (AES-256).

- REST: `POST https://api.smartpdf.ru/v1/pdf/protect` · MCP: `protect_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `user_password` (обязательный) | `string` | Пароль на открытие документа. |
| `owner_password` | `string` | Пароль владельца: без него документ нельзя редактировать и снять ограничения. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py protect document.pdf -p user_password=s3cret
```

### Снять пароль — `unlock`

Снимает пароль с PDF, если пароль известен.

- REST: `POST https://api.smartpdf.ru/v1/pdf/unlock` · MCP: `unlock_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `password` (обязательный) | `string` | Пароль документа. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py unlock protected.pdf -p password=s3cret
```

### Водяной знак — `watermark`

Наносит водяной знак — текст или логотип. Нужен ровно один из параметров text и image_file_id.

- REST: `POST https://api.smartpdf.ru/v1/pdf/watermark` · MCP: `watermark_pdf`
- Вход: PDF; логотип — PNG, JPG или WEBP через POST /v1/upload → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `text` | `string` | Текст знака (кириллица поддерживается). |
| `image_file_id` | `string` | file_id загруженного логотипа вместо текста. Прозрачность PNG сохраняется. |
| `font_size` | `integer` | Размер шрифта текста: от 8 до 200. По умолчанию: `48`. |
| `color` | `string` | Цвет текста — hex, например #0F766E. По умолчанию: `"#FF0000"`. |
| `opacity` | `number` | Непрозрачность: от 0 до 1. По умолчанию: `0.3`. |
| `angle` | `number` | Угол наклона в градусах: от −180 до 180. По умолчанию: `45`. |
| `position` | `string` | center — в центре; tile — плиткой по всей странице; углы — в выбранном углу. Значения: `"center"`, `"tile"`, `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"`. По умолчанию: `"center"`. |
| `pages` | `integer[] \| "all"` | Номера страниц с 1 или "all". По умолчанию: `"all"`. |
| `scale` | `number` | Ширина логотипа — доля ширины страницы: от 0,1 до 2; высота — по пропорциям. По умолчанию: `0.3`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py watermark document.pdf -p text=КОПИЯ -p opacity=0.2 -p position=tile
```
