import smtplib                                      # Импортируем библиотеку по работе с SMTP
from random import randint
from hashlib import sha256
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage              # Изображения

addr_from = "FNovik92@gmail.com"                 # Адресат
# addr_to   = "fb@mail.ru"                   # Получатель
password  = "eTpg7U4Omq"                                  # Пароль

def reset_password(addr_to):
  secret = str(randint(10**6, 10**7))
  for i in range(randint(1, 20)):
    secret = sha256(secret.encode('utf-8')).hexdigest()

  msg = MIMEMultipart()                               # Создаем сообщение
  msg['From']    = addr_from                          # Адресат
  msg['To']      = addr_to                            # Получатель
  msg['Subject'] = 'Восстановление пароля'                   # Тема сообщения

  # body = "Текст сообщения"
  # msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст
  html = """\
  <html>
    <head></head>
    <body>
      <label>Reset password</label>
      <p>"""+ str(secret) + """</p>
    </body>
  </html>
  """
  msg.attach(MIMEText(html, 'html', 'utf-8'))         # Добавляем в сообщение HTML-фрагмент

  server = smtplib.SMTP('smtp.gmail.com', 587)        # Создаем объект SMTP
  # server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
  server.starttls()                                   # Начинаем шифрованный обмен по TLS
  server.login(addr_from, password)                   # Получаем доступ
  server.send_message(msg)                            # Отправляем сообщение
  server.quit()                                       # Выходим
  return secret