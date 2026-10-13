# Операции SmartPDF — параметры

Файл собирается из описания API (`operations.json` портала) — не правьте вручную. Скрипту параметры передаются как
`-p имя=значение` (массивы, объекты и числа — JSON), REST — полями JSON рядом с `file_id` (`file_ids` у операций над
несколькими файлами), MCP — аргументами инструмента рядом с `file_url` (`file_urls`). Цена запроса — за каждую начатую единицу
(10 МБ входа, N страниц или N фото — берётся большее), сумма — на https://dev.smartpdf.ru/docs/billing.

## В PDF

### Word в PDF — `word-to-pdf`

Конвертирует документ Word в PDF: шрифты, таблицы и кириллица сохраняются.

- REST: `POST https://api.smartpdf.ru/v1/pdf/word-to-pdf` · MCP: `word_to_pdf`
- Вход: DOC, DOCX, ODT, RTF → результат: PDF
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
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP — от 1 до 10 файлов → результат: PDF
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `order` | `integer[]` | Порядок страниц — индексы file_ids от 0, каждый ровно один раз. Без него — порядок file_ids. |
| `fit` | `string` | auto — страница по размеру изображения; portrait и landscape — лист A4 с полями в выбранной ориентации. Значения: `"auto"`, `"portrait"`, `"landscape"`. По умолчанию: `"auto"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py jpg-to-pdf scan-1.jpg scan-2.jpg -p fit=portrait
```

### Фото в PDF — `photo-to-pdf`

Собирает фото с телефона в PDF: каждое фото — лист A4 в его ориентации, файл легче за счёт уменьшения. Режим «Скан документа» находит лист на фото, выравнивает перспективу и делает белый фон.

- REST: `POST https://api.smartpdf.ru/v1/pdf/photo-to-pdf` · MCP: `photo_to_pdf`
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: PDF
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `order` | `integer[]` | Порядок страниц — индексы file_ids от 0, каждый ровно один раз. Без него — порядок file_ids. |
| `page` | `string` | a4 — лист A4 в ориентации фото; photo — страница по размеру фото. Значения: `"a4"`, `"photo"`. По умолчанию: `"a4"`. |
| `compact` | `boolean` | Уменьшить фото до 2000 пикселей по длинной стороне и убрать EXIF и геометку. По умолчанию: `true`. |
| `grayscale` | `boolean` | Оттенки серого. По умолчанию: `false`. |
| `mode` | `string` | scan — «Скан документа»: лист выравнивается во весь A4; page, compact и grayscale тогда не действуют. Значения: `"photo"`, `"scan"`. По умолчанию: `"photo"`. |
| `scan_color` | `string` | Для mode: scan — bw: чёрно-белый как со сканера; color: цветной с белым фоном. Значения: `"bw"`, `"color"`. По умолчанию: `"bw"`. |
| `corners` | `array \| null` | Для mode: scan — углы листа на каждом фото в порядке file_ids: [[x, y] × 4] долями кадра (левый верхний, правый верхний, правый нижний, левый нижний) или null — найти автоматически. Без параметра — у всех автоматически. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py photo-to-pdf scan-1.jpg scan-2.jpg -p page=a4 -p compact=true
```

### Excel в PDF — `xlsx-to-pdf`

Конвертирует таблицу Excel в PDF. Листы, область и масштаб берутся из параметров печати файла.

- REST: `POST https://api.smartpdf.ru/v1/pdf/xlsx-to-pdf` · MCP: `xlsx_to_pdf`
- Вход: XLS, XLSX, ODS → результат: PDF
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
- Вход: PPT, PPTX, ODP → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pptx-to-pdf slides.pptx
```

### DjVu в PDF — `djvu-to-pdf`

Конвертирует книгу или скан DjVu в PDF. Текстовый слой DjVu не переносится — для поиска по тексту распознайте результат операцией OCR.

- REST: `POST https://api.smartpdf.ru/v1/pdf/djvu-to-pdf` · MCP: `djvu_to_pdf`
- Вход: DjVu → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py djvu-to-pdf book.djvu
```

### FB2 в PDF — `fb2-to-pdf`

Конвертирует книгу FB2 в PDF: главы — закладки, автор и название — в свойствах файла.

- REST: `POST https://api.smartpdf.ru/v1/pdf/fb2-to-pdf` · MCP: `fb2_to_pdf`
- Вход: FB2 → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `page` | `string` | Формат страницы: a5 — как книга, a4 — для печати. Значения: `"a5"`, `"a4"`. По умолчанию: `"a5"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py fb2-to-pdf book.fb2 -p page=a5
```

### EPUB в PDF — `epub-to-pdf`

Конвертирует книгу EPUB в PDF: главы из оглавления (toc.ncx) — закладки.

- REST: `POST https://api.smartpdf.ru/v1/pdf/epub-to-pdf` · MCP: `epub_to_pdf`
- Вход: EPUB → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `page` | `string` | Формат страницы: a5 — как книга, a4 — для печати. Значения: `"a5"`, `"a4"`. По умолчанию: `"a5"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py epub-to-pdf book.epub -p page=a5
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

Конвертирует PDF в редактируемый документ Word. Скан без текстового слоя (у загрузки text_layer: false) — с ocr: true: текст распознаётся и собирается в Word абзацами.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-word` · MCP: `pdf_to_word`
- Вход: PDF → результат: DOCX
- Единица цены: 10 МБ или 50 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `ocr` | `boolean` | Скан: сначала распознать текст (русский и английский, до 100 страниц). Вёрстка упрощается — абзацы, каждая страница с новой. Цена — как у OCR: единица за каждые начатые 10 страниц. По умолчанию: `false`. |
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

### PDF в PNG — `pdf-to-png`

Сохраняет страницы PDF картинками PNG без потерь — для схем, чертежей и скриншотов. Результат — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-png` · MCP: `pdf_to_png`
- Вход: PDF → результат: ZIP с PNG
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `dpi` | `integer` | Разрешение. Значения: `72`, `150`, `300`. По умолчанию: `150`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-png document.pdf -p dpi=150
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

### PDF в Markdown — `pdf-to-markdown`

Конвертирует PDF в Markdown для нейросетей, баз знаний и документации: заголовки по размеру шрифта, списки, таблицы, ссылки, жирный и курсив. Номера страниц у края убираются.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-markdown` · MCP: `pdf_to_markdown`
- Вход: PDF → результат: Markdown (.md, UTF-8)
- Единица цены: 10 МБ или 50 стр.

| Параметр | Тип | Описание |
|---|---|---|
| `ocr` | `boolean` | Скан без текстового слоя (у загрузки text_layer: false): сначала распознать текст — русский и английский, до 100 страниц. Цена — как у OCR: единица за каждые начатые 10 страниц. По умолчанию: `false`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py pdf-to-markdown document.pdf
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

## Изображения

### Сжать фото — `compress-image`

Сжимает фото: по уровню или до нужного размера в КБ. Одно фото — файл, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/compress-image` · MCP: `compress_image`
- Вход: JPG, PNG, WEBP, HEIC — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: JPG (PNG с прозрачностью — PNG); несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `level` | `string` | light — высокое качество; medium — до 2560 пикселей по длинной стороне; strong — до 1600. Значения: `"light"`, `"medium"`, `"strong"`. По умолчанию: `"medium"`. |
| `target_kb` | `number` | Сжать до размера, КБ (1 КБ = 1000 байт): от 10 до 50 000. Тогда level не используется; не получилось — наименьший вариант. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py compress-image scan-1.jpg -p level=medium
```

### HEIC в JPG — `heic-to-jpg`

Конвертирует фото HEIC/HEIF с iPhone в JPG с исходными цветами (ICC-профиль сохраняется). Одно фото — JPG, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/heic-to-jpg` · MCP: `heic_to_jpg`
- Вход: HEIC, HEIF — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: JPG; несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `compact` | `boolean` | Уменьшить до 2000 пикселей по длинной стороне. По умолчанию: `false`. |
| `keep_metadata` | `boolean` | Сохранить данные съёмки (EXIF: дата, камера, геометка). По умолчанию: `false`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py heic-to-jpg photo.heic
```

### Фото в текст — `image-to-text`

Распознаёт текст на фото и картинках: текст всех фото — в один файл, каждое фото с новой страницы.

- REST: `POST https://api.smartpdf.ru/v1/pdf/image-to-text` · MCP: `image_to_text`
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: TXT или DOCX
- Единица цены: 10 МБ суммы файлов или 10 фото

| Параметр | Тип | Описание |
|---|---|---|
| `languages` | `string[]` | Языки текста: от 1 до 4. Значения: `"rus"`, `"eng"`, `"deu"`, `"fra"`. По умолчанию: `["rus","eng"]`. |
| `format` | `string` | txt — строки как на фото; docx — абзацы. Значения: `"txt"`, `"docx"`. По умолчанию: `"txt"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py image-to-text scan-1.jpg -p 'languages=["rus","eng"]' -p format=txt
```

### PNG в JPG — `png-to-jpg`

Конвертирует картинки PNG в JPG. Прозрачность — белым фоном. Одна картинка — JPG, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/png-to-jpg` · MCP: `png_to_jpg`
- Вход: PNG — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: JPG; несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py png-to-jpg image.png
```

### JPG в PNG — `jpg-to-png`

Конвертирует картинки JPG в PNG. Без потерь. Одна картинка — PNG, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/jpg-to-png` · MCP: `jpg_to_png`
- Вход: JPG — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: PNG; несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py jpg-to-png scan-1.jpg
```

### WEBP в JPG — `webp-to-jpg`

Конвертирует картинки WEBP в JPG. Прозрачность — белым фоном, у анимации — первый кадр. Одна картинка — JPG, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/webp-to-jpg` · MCP: `webp_to_jpg`
- Вход: WEBP — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: JPG; несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py webp-to-jpg image.webp
```

### Изменить размер фото — `resize-image`

Меняет размер фото в процентах или пикселях, формат сохраняется. Одно фото — файл, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/resize-image` · MCP: `resize_image`
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: Тот же формат (HEIC — JPG); несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `mode` | `string` | percent — масштаб percent; pixels — width и/или height. Значения: `"percent"`, `"pixels"`. По умолчанию: `"percent"`. |
| `percent` | `number` | Масштаб, %: от 1 до 500. По умолчанию: `50`. |
| `width` | `integer` | Ширина, пикселей: до 10 000. |
| `height` | `integer` | Высота, пикселей: до 10 000. |
| `keep_aspect` | `boolean` | Сохранить пропорции: при width и height — по меньшему масштабу. По умолчанию: `true`. |
| `enlarge` | `boolean` | Разрешить увеличение. Без него фото меньше заданного размера не растягиваются. По умолчанию: `false`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py resize-image scan-1.jpg -p mode=pixels -p width=1200
```

### Обрезать фото — `crop-image`

Обрезает фото по рамке, формат сохраняется.

- REST: `POST https://api.smartpdf.ru/v1/pdf/crop-image` · MCP: `crop_image`
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP → результат: Тот же формат (HEIC — JPG)
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `box` (обязательный) | `number[]` | Рамка [x0, y0, x1, y1] долями кадра от 0 до 1, от левого верхнего угла; кадр — уже повёрнутый по EXIF. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py crop-image scan-1.jpg -p 'box=[0.1,0.1,0.9,0.9]'
```

### Повернуть фото — `rotate-image`

Поворачивает и отражает фото, формат сохраняется. Одно фото — файл, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/rotate-image` · MCP: `rotate_image`
- Вход: JPG, PNG, WEBP, HEIC, TIFF, BMP — до 10 файлов на бесплатном тарифе, 20 на Про, 50 на Бизнесе → результат: Тот же формат (HEIC — JPG); несколько — ZIP
- Единица цены: 10 МБ суммы файлов

| Параметр | Тип | Описание |
|---|---|---|
| `angle` | `integer` | Угол поворота по часовой стрелке. Значения: `0`, `90`, `180`, `270`. По умолчанию: `90`. |
| `flip` | `string \| null` | Отражение после поворота: horizontal — слева направо, vertical — сверху вниз. Значения: `"horizontal"`, `"vertical"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py rotate-image scan-1.jpg -p angle=90
```

### Word в JPG — `word-to-jpg`

Сохраняет страницы документа Word картинками JPG. Одна страница — JPG, несколько — ZIP-архив.

- REST: `POST https://api.smartpdf.ru/v1/pdf/word-to-jpg` · MCP: `word_to_jpg`
- Вход: DOC, DOCX, ODT, RTF → результат: JPG; несколько страниц — ZIP
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `dpi` | `integer` | Разрешение. Значения: `72`, `150`, `300`. По умолчанию: `150`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py word-to-jpg document.docx -p dpi=150
```

## Управление

### Редактор PDF — `edit`

Добавляет на страницы текст, подпись, картинку, закрашивание (текст под ним удаляется из файла), пометки и фигуры, заменяет строки текста. Объекты впечатываются в страницы.

- REST: `POST https://api.smartpdf.ru/v1/pdf/edit` · MCP: `edit_pdf`
- Вход: PDF; картинки и подпись картинкой — PNG, JPG, WEBP, HEIC через POST /v1/upload → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `objects` (обязательный) | `object[]` | Объекты по порядку, последний — сверху; до 500, картинок — до 20. Координаты — доли видимой страницы от 0 до 1 от левого верхнего угла (чуть за край можно), размеры — в пунктах. У каждого page (с 1) и type: text — box, text (переносится по ширине box) или lines (готовые строки), size (12), font (sans, serif, mono), bold, italic, color (#RRGGBB); signature — box и lines (до 3 строк рукописным шрифтом) или file_id картинки, size, color; image — box, file_id; whiteout (закрасить), highlight, rect, ellipse, check, cross — box, color, width, fill; line, arrow, ink — points [[x, y], …], color, width; replace_text — box и baseline исходной строки, x — начало новой, text (пустой — удалить строку), font, size, color. Подпись через API не входит в лимит подписей сайта. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py edit document.pdf -p 'objects=[{"type":"text","page":1,"box":[0.1,0.03,0.9,0.08],"text":"Согласовано","size":14}]'
```

### Сжать PDF — `compress`

Уменьшает размер PDF. Результат никогда не больше исходного файла.

- REST: `POST https://api.smartpdf.ru/v1/pdf/compress` · MCP: `compress_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `level` | `string` | low — без потерь качества; medium — изображения 150 dpi; high — 100 dpi, наибольшее сжатие. Значения: `"low"`, `"medium"`, `"high"`. По умолчанию: `"medium"`. |
| `target_mb` | `number` | Сжать до размера: лимит в МБ (1 МБ = 1 000 000 байт), от 0,1 до 500. Берётся самое мягкое сжатие, при котором файл укладывается в лимит (изображения — не ниже 100 dpi); level тогда не используется. Не уложились — наименьший результат, его размер — output_file_size в статусе задачи. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py compress document.pdf -p level=medium
```

### PDF в ч/б — `grayscale`

Переводит PDF в оттенки серого — для печати и требований «только ч/б». Текст остаётся текстом: искать и копировать можно.

- REST: `POST https://api.smartpdf.ru/v1/pdf/grayscale` · MCP: `grayscale_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py grayscale document.pdf
```

### PDF в PDF/A — `to-pdfa`

Конвертирует PDF в PDF/A — формат долговременного хранения для архивов, судов и госорганов. Документ с электронной подписью не конвертируется: подпись перестала бы действовать.

- REST: `POST https://api.smartpdf.ru/v1/pdf/to-pdfa` · MCP: `pdf_to_pdfa`
- Вход: PDF → результат: PDF/A
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `version` | `string` | 1 — PDF/A-1b, 2 — PDF/A-2b, 3 — PDF/A-3b. Значения: `"1"`, `"2"`, `"3"`. По умолчанию: `"2"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py to-pdfa document.pdf -p version=2
```

### Восстановить PDF — `repair`

Восстанавливает повреждённый PDF, который не открывается или открывается с ошибкой. Если восстановить нечего — ошибка без списания.

- REST: `POST https://api.smartpdf.ru/v1/pdf/repair` · MCP: `repair_pdf`
- Вход: PDF, в том числе повреждённый → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py repair document.pdf
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

### Обрезать PDF — `crop`

Обрезает страницы PDF по рамке или убирает белые поля автоматически. Содержимое за краем остаётся в файле — чтобы скрыть данные, используйте redact.

- REST: `POST https://api.smartpdf.ru/v1/pdf/crop` · MCP: `crop_pdf`
- Вход: PDF → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `mode` | `string` | box — по рамке box; auto — белые поля каждой страницы. Значения: `"box"`, `"auto"`. По умолчанию: `"box"`. |
| `box` | `number[] \| null` | Для mode: box — рамка [x0, y0, x1, y1] долями видимой страницы от 0 до 1, от левого верхнего угла. |
| `pages` | `integer[] \| "all"` | Номера страниц с 1 или "all". По умолчанию: `"all"`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py crop document.pdf -p mode=auto
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

### Скрыть персональные данные — `redact`

Скрывает персональные данные: находит их сама (find) и/или берёт области (areas) и удаляет из файла — под чёрными прямоугольниками текста и пикселей больше нет. Ничего не нашлось и областей нет — ошибка без списания.

- REST: `POST https://api.smartpdf.ru/v1/pdf/redact` · MCP: `redact_pdf`
- Вход: PDF с текстовым слоем (скан — сначала OCR или areas) → результат: PDF
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `areas` | `object[]` | Области вручную: [{"page": 1, "box": [x0, y0, x1, y1]}] долями видимой страницы — например, boxes из find-personal-data. До 5000. По умолчанию: `[]`. |
| `find` | `object \| null` | Найти и скрыть тем же запросом: {"kinds": [...], "words": [...]} — как у find-personal-data. Нужно areas, find или оба. |
| `clean` | `boolean` | Убрать скрытые данные файла: автора и свойства, XMP, комментарии, вложения, скрипты, миниатюры. По умолчанию: `true`. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py redact personal.pdf -p 'find={"kinds":["phone","email","snils","inn"],"words":["Иванов Иван Иванович"]}'
```

### Найти персональные данные — `find-personal-data`

Находит персональные данные в PDF, файл не меняет. Результат — JSON: {"pages": [{"page", "items": [{"kind", "text", "boxes"}]}], "scanned": [страницы-сканы без текста], "total"}; boxes — [x0, y0, x1, y1] долями страницы, их можно передать в redact как areas.

- REST: `POST https://api.smartpdf.ru/v1/pdf/find-personal-data` · MCP: `find_personal_data`
- Вход: PDF с текстовым слоем → результат: JSON
- Единица цены: 10 МБ

| Параметр | Тип | Описание |
|---|---|---|
| `kinds` | `string[]` | Что искать: passport — паспорт, snils — СНИЛС, inn — ИНН, phone — телефоны, email — почта, card — номера карт, account — счета физлиц. СНИЛС, ИНН и карты проверяются контрольными суммами. Значения: `"passport"`, `"snils"`, `"inn"`, `"phone"`, `"email"`, `"card"`, `"account"`. По умолчанию: `["passport","snils","inn","phone","email","card","account"]`. |
| `words` | `string[]` | Свои слова — ФИО, адрес, название: до 50, каждое от 3 символов. Ищутся целыми словами без учёта регистра. |
| `webhook_url` | `string` | https-адрес: по завершении SmartPDF отправит на него POST с результатом и подписью — вместо опроса статуса (раздел «Вебхуки»). |

```bash
python3 scripts/smartpdf.py find-personal-data personal.pdf -p 'kinds=["phone","email","snils"]'
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
