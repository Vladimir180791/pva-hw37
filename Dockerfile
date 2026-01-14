FROM python:3.11-slim

# Установка необходимых системных зависимостей для Selenium и Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    # Для Chrome
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libxtst6 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    # Для headless Chrome
    xvfb \
    # Утилиты
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver через WebDriver Manager (будет установлен автоматически при запуске)
# Но также можно установить фиксированную версию:
# RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) \
#     && wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" \
#     && CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE_${CHROME_VERSION}) \
#     && wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
#     && unzip chromedriver_linux64.zip \
#     && mv chromedriver /usr/local/bin/ \
#     && rm chromedriver_linux64.zip LATEST_RELEASE_${CHROME_VERSION}

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем необходимые директории
RUN mkdir -p \
    logs \
    reports/allure-results \
    reports/html \
    screenshots \
    downloads

# Настройка прав для директорий
RUN chmod -R 755 /app/logs /app/reports /app/screenshots /app/downloads

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app \
    DISPLAY=:99 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/bin/google-chrome \
    # Headless режим по умолчанию
    HEADLESS=true \
    # Настройки для контейнера
    NO_SANDBOX=true \
    DISABLE_DEV_SHM=true \
    # Allure
    ALLURE_RESULTS_DIR=/app/reports/allure-results \
    # Пути
    SCREENSHOTS_DIR=/app/screenshots \
    DOWNLOADS_DIR=/app/downloads

# Создаем пользователя для безопасности (не root)
RUN useradd -m -u 1000 jenkins && \
    chown -R jenkins:jenkins /app

USER jenkins

# Команда по умолчанию - запуск тестов
CMD ["python", "-m", "pytest", "tests/", \
     "--alluredir=reports/allure-results", \
     "--html=reports/html/report.html", \
     "--self-contained-html", \
     "-v"]