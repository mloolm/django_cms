// your_app/static/your_plugin/plugin.js
tinymce.PluginManager.add('add_from_gallery', function(editor, url) {
  // Добавление кнопки на панель инструментов
  editor.ui.registry.addButton('add_from_gallery', {
    text: 'Вставить из галереи',
    icon: 'image', // Можете использовать другие иконки TinyMCE
    onAction: function() {
      // Открытие диалогового окна
      editor.windowManager.open({
        title: 'Галерея изображений',
        body: {
          type: 'panel',
          items: [
            {
              type: 'htmlpanel',
              html: '<iframe src="/admin-gallery/" style="width: 500px; height: 400px;"></iframe>'
            }
          ]
        },
        buttons: [
          {
            text: 'Закрыть',
            type: 'cancel',
            onclick: 'close'
          }
        ]
      });
    }
  });

  // Добавление пункта меню (опционально)
  editor.ui.registry.addMenuItem('add_from_gallery', {
    text: 'Вставить из галереи',
    icon: 'image',
    context: 'insert',
    onAction: function() {
      editor.execCommand('add_from_gallery');
    }
  });

  // Возвращение информации о плагине
  return {
    getMetadata: function() {
      return  {
        name: "Add from gallery",
        url: "http://yourwebsite.com"
      };
    }
  };
});

