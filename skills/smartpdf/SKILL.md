---
name: smartpdf
description: >-
  PDF tools by SmartPDF (smartpdf.ru): compress, merge, split, convert PDF to and from Word, Excel, PowerPoint,
  JPG and text, OCR scans (Russian, English, German, French), rotate, delete, extract or reorder pages, add page
  numbers, sign, watermark, password-protect or unlock. Use when the user asks to do any of this with PDF files or
  to turn documents or images into PDF: SmartPDF MCP tools for public links, the bundled script for local files.
  Сжать, объединить, разделить, конвертировать PDF, распознать текст, подписать, водяной знак, пароль на PDF.
---

# SmartPDF

24 операции с PDF через API SmartPDF. Каждая операция — платный запрос с баланса API пользователя в рублях: цена
зависит от размера файла, у распознавания и конвертации из PDF — ещё и от числа страниц. Перед обработкой многих
файлов предупреди пользователя, что каждый файл — отдельный запрос.

## Как обработать файл

| Где файл | Как |
|---|---|
| Публичная ссылка (http или https, без входа, до 100 МБ) и подключены инструменты MCP SmartPDF (`compress_pdf`, `merge_pdfs`, …) | Вызови инструмент: `file_url`, у объединения и JPG в PDF — `file_urls`. В ответе `download_url` — ссылка на результат, действует час |
| Файл на диске; ссылка на `localhost` или во внутренней сети; инструментов MCP нет | Скрипт `scripts/smartpdf.py` — REST API, нужен Python 3 |

Если доступны инструменты MCP, передавай им ссылку — не скачивай файл, чтобы загрузить его скриптом.

## Ключ

Скрипту нужна переменная окружения `SMARTPDF_API_KEY` (`sk_live_…`). Ключ, сохранённый в настройках MCP-клиента
или плагина, скрипт не видит.

Если переменной нет, попроси пользователя создать ключ в личном кабинете — https://smartpdf.ru/dashboard/api-keys
(после подтверждения почты на балансе 300 ₽) — и задать переменную в своём терминале или профиле оболочки.
Не проси прислать ключ в чат и не записывай его в файлы проекта.

## Скрипт

Путь — от папки этого навыка. Результат сохраняется рядом с первым файлом как `<имя>_smartpdf.<расширение>`
(или в папку `-o`), путь к нему печатается в stdout; ход работы и ошибки — в stderr.

```bash
python3 scripts/smartpdf.py compress report.pdf -p level=high
python3 scripts/smartpdf.py merge january.pdf february.pdf march.pdf
python3 scripts/smartpdf.py pdf-to-word contract.pdf
python3 scripts/smartpdf.py ocr scan.pdf -p 'languages=["rus","eng"]'
python3 scripts/smartpdf.py split book.pdf -p mode=ranges -p 'ranges=[[1,10],[11,20]]'
python3 scripts/smartpdf.py watermark offer.pdf -p text=КОПИЯ -p position=tile
python3 scripts/smartpdf.py protect report.pdf -p user_password=Secret-2026
python3 scripts/smartpdf.py compress big.pdf --link    # ссылка на результат вместо скачивания
python3 scripts/smartpdf.py balance                     # баланс и цена запроса
```

- Параметры — `-p имя=значение`; числа, массивы и `true`/`false` — в JSON, строки — как есть.
- Логотип для водяного знака — `--upload image_file_id=logo.png`, картинка подписи — `--data-uri signature_data=signature.png`.
- Операции над одним файлом — по запросу на файл: для нескольких файлов запусти скрипт для каждого.
- Код выхода: 0 — готово; 1 — ошибка API, текст и подсказка в stderr; 2 — неверный вызов; 3 — файл не обработан,
  причина в stderr, оплата вернулась на баланс.

## Операции

<!-- operations:start -->
| Операция | Скрипт | Инструмент MCP | Параметры (* — обязательный) |
|---|---|---|---|
| Word в PDF | `word-to-pdf` | `word_to_pdf` | — |
| JPG в PDF | `jpg-to-pdf` | `jpg_to_pdf` | `order`, `fit` |
| Excel в PDF | `xlsx-to-pdf` | `xlsx_to_pdf` | — |
| PowerPoint в PDF | `pptx-to-pdf` | `pptx_to_pdf` | — |
| HTML в PDF | `html-to-pdf` | `html_to_pdf` | `page_size`, `orientation`, `margin` |
| PDF в Word | `pdf-to-word` | `pdf_to_word` | — |
| PDF в JPG | `pdf-to-jpg` | `pdf_to_jpg` | `dpi`, `pages` |
| PDF в Excel | `pdf-to-excel` | `pdf_to_excel` | `layout` |
| PDF в PowerPoint | `pdf-to-pptx` | `pdf_to_pptx` | — |
| PDF в текст | `pdf-to-txt` | `pdf_to_txt` | `mode` |
| Сжать PDF | `compress` | `compress_pdf` | `level` |
| Объединить PDF | `merge` | `merge_pdfs` | `order` |
| Разделить PDF | `split` | `split_pdf` | `mode`, `ranges` |
| Распознать текст | `ocr` | `ocr_pdf` | `languages` |
| Сгладить PDF | `flatten` | `flatten_pdf` | — |
| Удалить страницы | `delete-pages` | `delete_pages` | `pages`* |
| Извлечь страницы | `extract-pages` | `extract_pages` | `pages`* |
| Повернуть страницы | `rotate` | `rotate_pdf` | `pages`, `angle` |
| Порядок страниц | `reorder-pages` | `reorder_pages` | `new_order`* |
| Нумерация страниц | `add-page-numbers` | `add_page_numbers` | `position`, `start_from`, `prefix`, `font_size`, `pages` |
| Подписать PDF | `sign` | `sign_pdf` | `signature_data`*, `page`, `x`, `y`, `width`, `height` |
| Защитить паролем | `protect` | `protect_pdf` | `user_password`*, `owner_password` |
| Снять пароль | `unlock` | `unlock_pdf` | `password`* |
| Водяной знак | `watermark` | `watermark_pdf` | `text`, `image_file_id`, `font_size`, `color`, `opacity`, `angle`, `position`, `pages`, `scale` |

У всех операций есть `webhook_url` — https-адрес для уведомления о готовности вместо ожидания. Баланс — `get_balance` в MCP или `python3 scripts/smartpdf.py balance`.
<!-- operations:end -->

Параметры подробно — [reference/operations.md](reference/operations.md).

## Ошибки

- `402` — не хватает баланса или исчерпан лимит ключа, ничего не списано. Скажи пользователю и дай ссылку
  https://smartpdf.ru/dashboard/api-keys.
- `413` — файл больше лимита тарифа (бесплатный — 50 МБ, Про — 200 МБ, Бизнес — 500 МБ): предложи сжать или разделить.
- `422` — ошибка в параметрах. Распознавание — не больше 100 страниц за раз: раздели файл (`split`) и распознай части.
- `429` — скрипт сам подождёт и повторит; с инструментами MCP подожди и повтори.
- Файл не обработан (код 3 или ошибка инструмента) — в тексте понятная причина: неверный пароль, повреждённый PDF.
  Перескажи её пользователю; оплата вернулась на баланс.

## Важно

- `sign` ставит на страницу изображение или текст подписи — это не электронная подпись (не ЭП и не КЭП).
- Загруженные файлы удаляются через час, результат хранится по тарифу. На бесплатном тарифе ссылку на результат
  выдают один раз — скачай файл сразу.
- HTML в PDF — только из загруженного HTML-файла, адреса страниц не принимаются.
- Документация: https://dev.smartpdf.ru/docs · для агентов: https://dev.smartpdf.ru/llms.txt
