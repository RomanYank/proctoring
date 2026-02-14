FROM php:8.1-fpm

RUN apt-get update && apt-get install -y \
    libzip-dev zip unzip git \
    && docker-php-ext-install pdo pdo_mysql zip

WORKDIR /var/www

RUN chown -R www-data:www-data /var/www

EXPOSE 9000
CMD ["php-fpm"]
