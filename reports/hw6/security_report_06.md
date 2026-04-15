# * Демонстрация XSS

![1776289224737](image/1/1776289224737.png)

![1776289247131](image/1/1776289247131.png)

![1776289350439](image/security_report_06/1776289350439.png)


![1776289367477](image/security_report_06/1776289367477.png)

## 2. Санитизация

Использована библиотека bleach.

```python
def sanitize_html(text: str) -> str:
    return bleach.clean(
        text,
        tags=['b', 'i', 'u', 'em', 'strong'],
        attributes={},
        strip=True
    )
```

## 3. CSP

Добавлен заголовок:

Content-Security-Policy:

default-src 'self'; script-src 'self'; style-src 'self'

![1776289390116](image/security_report_06/1776289390116.png)


## 4. Блокировка атаки

Браузер блокирует inline-скрипты.

![1776289416124](image/security_report_06/1776289416124.png)
