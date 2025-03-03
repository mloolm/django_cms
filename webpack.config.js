const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    styles: './src/scss/main.scss', // Точка входа для SCSS
    scripts: './src/scripts/index.js', // Точка входа для JS
  },
  output: {
    path: path.resolve(__dirname, 'app/static/src'), // Общая директория для CSS и JS
    filename: 'js/[name].js', // Имя выходного файла JS (scripts.js), с папкой для JS
    assetModuleFilename: 'fonts/[name][ext]', // Папка для шрифтов
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader, // Извлекает CSS в отдельный файл
          'css-loader',                // Преобразует CSS в CommonJS
          'postcss-loader',            // Опционально: автопрефиксы и минификация
          'sass-loader',               // Компилирует SCSS в CSS
        ],
      },
      {
        test: /\.js$/,
        exclude: /node_modules/, // Исключаем сторонние библиотеки
        use: {
          loader: 'babel-loader', // Для поддержки современного JS
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf|svg)$/, // Обрабатываем шрифты и SVG
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][ext]', // Помещаем файлы в static/src/fonts/
        },
      },
      {
        test: /\.(png|jpe?g|gif|webp|ico)$/, // Обрабатываем изображения
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]', // Помещаем файлы в static/src/images/
        },
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/[name].css', // Имя выходного файла CSS (styles.css), с папкой для CSS
    }),
  ],
  resolve: {
    alias: {
      '@fortawesome/fontawesome-free': path.resolve(__dirname, 'node_modules/@fortawesome/fontawesome-free'),
    },
  },

  devtool: 'source-map',
  mode: 'development',
  watch: true,
};
